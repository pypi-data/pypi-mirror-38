from volcano.general import variant
from volcano.general.stddef import Quality
from volcano.general.xml_reader import XmlReader

from . import time_tools
from . import base_dev
from . import merk_defs
from . import connected_values
from .merk_nzif_common import ProtocolException

MEASURES_ENERGY = (
    ('Eap', 'Ean', 'Erp', 'Ern', 0x00),
)


class MerkDevice(base_dev.BaseDevice):

    def __init__(self, my_xml_node, proposed_aux_name, parent_log):
        super().__init__(my_xml_node, proposed_aux_name, parent_log)

        p = XmlReader(my_xml_node)

        self.addr_ = p.get_int('slaveNb', min_val=0, max_val=0xff)

        # device type
        self.type_def_ = p.get_dic('type', merk_defs.g_merk_type_defs)

        # password
        pwd_str = p.get_str('pwd', '000000')
        if len(pwd_str) != 6:
            raise Exception('{}: password "{}" is invalid: should be 6 characters long'.format(p.location(), pwd_str))
        self.password_ = bytes([ord(x) for x in pwd_str])

        # timeouts
        self.timeout_general_ = time_tools.Timeout(p.get_time_secs('readPeriod', 5.0, min_val=0.0, max_val=600.0), expired=True)

        # Create values
        self.val_online_ = connected_values.ConnectedValue(self.branch('online'), variant.BoolValue(), True)
        self.values_ = {}
        for n1, n2, n3, n4, *r in MEASURES_ENERGY:      # pylint: disable=unused-variable
            for name in (n1, n2, n3, n4):
                self.values_[name] = connected_values.ConnectedValue(self.branch(name), variant.FloatValue(), False)

    def sync(self, services: dict):
        assert isinstance(services, dict), services
        super().sync(services)
        self.val_online_.sync(services)
        for k, v in self.values_.items():       # pylint: disable=unused-variable
            v.sync(services)

    def on_channel_closed(self):
        self.log().debug('Channel closed and device going offline')
        self.set_offline()

    def set_offline(self):
        self.val_online_.set(False)
        # self.scaling_ = None
        for k, v in self.values_.items():       # pylint: disable=unused-variable
            v.invalidate(Quality.QUALITY_COMM)

    def work(self, ctx):
        log = self.log()

        if not self.timeout_general_.is_expired():
            return

        try:
            self.open_channel(ctx)
        except (ConnectionError, TimeoutError, ProtocolException) as e:
            log.warning(e)
            self.set_offline()
            self.timeout_general_.start()
            return

        self.val_online_.set(True)
        for name, con_val in self.values_.items():  # pylint: disable=unused-variable
            con_val.mark_unread()

        try:
            for n1, n2, n3, n4, arr in MEASURES_ENERGY:
                try:
                    self.read_energy(ctx, arr, 'Read energy {} {} {} {}'.format(n1, n2, n3, n4), (n1, n2, n3, n4))
                except (ConnectionError, TimeoutError, ProtocolException) as e:
                    if ctx.is_open():
                        log.warning(e)
                    else:
                        raise

        except (ConnectionError, TimeoutError, ProtocolException) as e:
            log.warning(e)

        finally:
            for name, con_val in self.values_.items():
                if not con_val.is_read():
                    con_val.invalidate(Quality.QUALITY_COMM)
            self.timeout_general_.start()

    def open_channel(self, ctx):
        # access level
        req = bytes([self.addr_, 0x01, 0x01]) + self.password_

        ctx.send_rcv(req, None, 'Open channel', self.log())

    @staticmethod
    # None => энергия маскирована (не поддерживается)
    # rval: вт*ч
    def parse_energy_4_bytes(d: (bytes, bytearray), off: int) -> (int, None):
        assert isinstance(d, (bytes, bytearray)), d
        assert isinstance(off, int), off
        assert off + 4 <= len(d), (d, off)

        b0 = d[off + 0]
        b1 = d[off + 1]
        b2 = d[off + 2]
        b3 = d[off + 3]

        if b0 == 0xff and b1 == 0xff and b2 == 0xff and b3 == 0xff:
            return None

        return b2 | (b3 << 8) | (b0 << 16) | (b1 << 24)

    def read_energy(self, ctx, array_nb, comment, tpl):
        log = self.log()

        month_nb = 0
        tariff_nb = 0  # 0 - сумма тарифов

        req = bytes([self.addr_, 0x05, (array_nb << 4) | month_nb, tariff_nb])

        ctx.send_rcv(req, 16, comment, log)

        eap_wth = MerkDevice.parse_energy_4_bytes(ctx.data(), 0)
        ean_wth = MerkDevice.parse_energy_4_bytes(ctx.data(), 4)
        erp_wth = MerkDevice.parse_energy_4_bytes(ctx.data(), 8)
        ern_wth = MerkDevice.parse_energy_4_bytes(ctx.data(), 12)

        eap_kwth = 0.0 if eap_wth is None else eap_wth / 1000.0
        ean_kwth = 0.0 if ean_wth is None else ean_wth / 1000.0
        erp_kwth = 0.0 if erp_wth is None else erp_wth / 1000.0
        ern_kwth = 0.0 if ern_wth is None else ern_wth / 1000.0

        log.debug('Eap={} Ean={} Erp={} Ern={} [kwth]'.format(eap_kwth, ean_kwth, erp_kwth, ern_kwth))

        eap_name, ean_name, erp_name, ern_name = tpl

        self.values_[eap_name].set(eap_kwth)
        self.values_[ean_name].set(ean_kwth)
        self.values_[erp_name].set(erp_kwth)
        self.values_[ern_name].set(ern_kwth)
