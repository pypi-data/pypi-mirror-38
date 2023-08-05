# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
from kaitaistruct import __version__ as ks_version, KaitaiStruct, KaitaiStream, BytesIO


if parse_version(ks_version) < parse_version('0.7'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.7 or later is required, but you have %s" % (ks_version))

class Cubebel1(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.ax25_frame = self._root.Ax25Frame(self._io, self, self._root)

    class Ax25Frame(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.ax25_header = self._root.Ax25Hdr(self._io, self, self._root)
            self.ax25_info = self._root.Ax25Info(self._io, self, self._root)


    class DestCallsign(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.dest_callsign = (self._io.read_bytes(6)).decode(u"ASCII")


    class SrcCallsignRaw(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self._raw__raw_src_callsign_ror = self._io.read_bytes(6)
            self._raw_src_callsign_ror = KaitaiStream.process_rotate_left(self._raw__raw_src_callsign_ror, 8 - (1), 1)
            io = KaitaiStream(BytesIO(self._raw_src_callsign_ror))
            self.src_callsign_ror = self._root.SrcCallsign(io, self, self._root)


    class RfMessage(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.cubebel1_rf_msg = (self._io.read_bytes((self._parent.cubebel1_header.cubebel1_info_size - 1))).decode(u"ASCII")


    class Ax25Hdr(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.dest_callsign_raw = self._root.DestCallsignRaw(self._io, self, self._root)
            self.dest_ssid = self._io.read_u1()
            self.src_callsign_raw = self._root.SrcCallsignRaw(self._io, self, self._root)
            self.src_ssid = self._io.read_u1()
            self.ctl = self._io.read_u1()
            self.pid = self._io.read_u1()


    class EpsShortTel(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.cubebel1_sys_time = self._io.read_u2le()
            self.cubebel1_adc_correctness = self._io.read_bits_int(2)
            self.cubebel1_t_adc1 = self._io.read_bits_int(12)
            self.cubebel1_t_adc2 = self._io.read_bits_int(12)
            self.cubebel1_stepup_current = self._io.read_bits_int(12)
            self.cubebel1_stetup_voltage = self._io.read_bits_int(12)
            self.cubebel1_afterbq_current = self._io.read_bits_int(12)
            self.cubebel1_battery_voltage = self._io.read_bits_int(12)
            self.cubebel1_sys_voltage_50 = self._io.read_bits_int(12)
            self.cubebel1_sys_voltage_33 = self._io.read_bits_int(12)
            self.cubebel1_eps_uc_current = self._io.read_bits_int(12)
            self.cubebel1_obc_uc_current = self._io.read_bits_int(10)
            self.cubebel1_rf1_uc_current = self._io.read_bits_int(10)
            self.cubebel1_rf2_uc_current = self._io.read_bits_int(12)
            self.cubebel1_solar_voltage = self._io.read_bits_int(12)
            self.cubebel1_side_x_current = self._io.read_bits_int(12)
            self.cubebel1_side_py_current = self._io.read_bits_int(12)
            self.cubebel1_side_ny_current = self._io.read_bits_int(12)
            self.cubebel1_side_pz_current = self._io.read_bits_int(12)
            self.cubebel1_side_nz_current = self._io.read_bits_int(12)


    class RfResponse(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.cubebel1_fec_crc_status = self._io.read_bits_int(1) != 0
            self.cubebel1_rx_msg_state = self._io.read_bits_int(7)
            self._io.align_to_byte()
            self.cubebel1_rssi = self._io.read_u1()


    class EpsFullTel(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.eps_short_tel = self._root.EpsShortTel(self._io, self, self._root)
            self.cubebel1_current_to_gamma = self._io.read_bits_int(12)
            self.cubebel1_current_to_irsensor = self._io.read_bits_int(12)
            self.cubebel1_current_to_extflash = self._io.read_bits_int(12)
            self.cubebel1_current_to_solarsens = self._io.read_bits_int(12)
            self.cubebel1_current_to_magnetcoils = self._io.read_bits_int(12)
            self.cubebel1_current_to_coil_x = self._io.read_bits_int(12)
            self.cubebel1_current_to_coil_y = self._io.read_bits_int(12)
            self.cubebel1_current_to_coil_pz = self._io.read_bits_int(12)
            self.cubebel1_current_to_coil_nz = self._io.read_bits_int(12)
            self.cubebel1_battery1_temp = self._io.read_bits_int(12)
            self.cubebel1_battery2_temp = self._io.read_bits_int(12)
            self._io.align_to_byte()
            self.cubebel1_numb_oc_obc = self._io.read_u1()
            self.cubebel1_numb_oc_out_gamma = self._io.read_u1()
            self.cubebel1_numb_oc_out_rf1 = self._io.read_u1()
            self.cubebel1_numb_oc_out_rf2 = self._io.read_u1()
            self.cubebel1_numb_oc_out_flash = self._io.read_u1()
            self.cubebel1_numb_oc_out_irsens = self._io.read_u1()
            self.cubebel1_numb_oc_coil_x = self._io.read_u1()
            self.cubebel1_numb_oc_coil_y = self._io.read_u1()
            self.cubebel1_numb_oc_coil_pz = self._io.read_u1()
            self.cubebel1_numb_oc_coil_nz = self._io.read_u1()
            self.cubebel1_numb_oc_magnetcoils = self._io.read_u1()
            self.cubebel1_numb_oc_solarsens = self._io.read_u1()
            self.cubebel1_reset_num = self._io.read_u2le()
            self.cubebel1_reset_reason = self._io.read_u1()
            self.cubebel1_pwr_sat = self._io.read_bits_int(1) != 0
            self.cubebel1_pwr_rf1 = self._io.read_bits_int(1) != 0
            self.cubebel1_pwr_rf2 = self._io.read_bits_int(1) != 0
            self.cubebel1_pwr_sunsensor = self._io.read_bits_int(1) != 0
            self.cubebel1_pwr_gamma = self._io.read_bits_int(1) != 0
            self.cubebel1_pwr_irsensor = self._io.read_bits_int(1) != 0
            self.cubebel1_pwr_flash = self._io.read_bits_int(1) != 0
            self.cubebel1_pwr_magnet_x = self._io.read_bits_int(1) != 0
            self.cubebel1_pwr_magnet_y = self._io.read_bits_int(1) != 0
            self.cubebel1_pwr_magnet_z = self._io.read_bits_int(1) != 0


    class Cubebel1Header(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.cubebel1_rf_id = self._io.read_u1()
            self.cubebel1_opr_time = self._io.read_u2le()
            self.cubebel1_reboot_cnt = self._io.read_u1()
            self.cubebel1_mcusr = self._io.read_u1()
            self.cubebel1_pamp_temp = self._io.read_u2le()
            self.cubebel1_pamp_voltage = self._io.read_u1()
            self.cubebel1_tx_attenuator = self._io.read_u1()
            self.cubebel1_battery_voltage = self._io.read_u2le()
            self.cubebel1_system_voltage = self._io.read_u2le()
            self.cubebel1_seq_number = self._io.read_u2le()
            self.cubebel1_pwr_save_state = self._io.read_u1()
            self.cubebel1_modem_on_period = self._io.read_u2le()
            self.cubebel1_obc_can_status = self._io.read_u1()
            self.cubebel1_eps_can_status = self._io.read_u1()
            self.cubebel1_info_size = self._io.read_u1()
            self.cubebel1_data_type = self._io.read_u1()


    class DestCallsignRaw(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self._raw__raw_dest_callsign_ror = self._io.read_bytes(6)
            self._raw_dest_callsign_ror = KaitaiStream.process_rotate_left(self._raw__raw_dest_callsign_ror, 8 - (1), 1)
            io = KaitaiStream(BytesIO(self._raw_dest_callsign_ror))
            self.dest_callsign_ror = self._root.DestCallsign(io, self, self._root)


    class SrcCallsign(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.src_callsign = (self._io.read_bytes(6)).decode(u"ASCII")


    class Ax25Info(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.cubebel1_header = self._root.Cubebel1Header(self._io, self, self._root)
            if self.cubebel1_header.cubebel1_info_size > 0:
                _on = self.cubebel1_header.cubebel1_data_type
                if _on == 1:
                    self.cubebel1_data = self._root.RfResponse(self._io, self, self._root)
                elif _on == 3:
                    self.cubebel1_data = self._root.RfMessage(self._io, self, self._root)
                elif _on == 254:
                    self.cubebel1_data = self._root.EpsFullTel(self._io, self, self._root)
                elif _on == 255:
                    self.cubebel1_data = self._root.EpsShortTel(self._io, self, self._root)




