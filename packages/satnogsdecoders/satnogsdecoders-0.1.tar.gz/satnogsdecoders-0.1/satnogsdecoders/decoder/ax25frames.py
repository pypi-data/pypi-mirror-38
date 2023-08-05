# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
from kaitaistruct import __version__ as ks_version, KaitaiStruct, KaitaiStream, BytesIO


if parse_version(ks_version) < parse_version('0.7'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.7 or later is required, but you have %s" % (ks_version))

class Ax25frames(KaitaiStruct):
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
            self.ax25_header = self._root.Ax25Header(self._io, self, self._root)
            _on = (self.ax25_header.ctl & 19)
            if _on == 0:
                self.payload = self._root.IFrame(self._io, self, self._root)
            elif _on == 3:
                self.payload = self._root.UiFrame(self._io, self, self._root)
            elif _on == 19:
                self.payload = self._root.UiFrame(self._io, self, self._root)
            elif _on == 16:
                self.payload = self._root.IFrame(self._io, self, self._root)
            elif _on == 18:
                self.payload = self._root.IFrame(self._io, self, self._root)
            elif _on == 2:
                self.payload = self._root.IFrame(self._io, self, self._root)


    class DestCallsign(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.dest_callsign = (self._io.read_bytes(6)).decode(u"ASCII")


    class Ax25Header(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.dest_callsign_raw = self._root.DestCallsignRaw(self._io, self, self._root)
            self.dest_ssid_raw = self._io.read_u1()
            self.src_callsign_raw = self._root.SrcCallsignRaw(self._io, self, self._root)
            self.src_ssid_raw = self._io.read_u1()
            self.ctl = self._io.read_u1()
            self.pid = self._io.read_u1()

        @property
        def src_ssid(self):
            if hasattr(self, '_m_src_ssid'):
                return self._m_src_ssid if hasattr(self, '_m_src_ssid') else None

            self._m_src_ssid = ((self.src_ssid_raw & 15) >> 1)
            return self._m_src_ssid if hasattr(self, '_m_src_ssid') else None

        @property
        def dest_ssid(self):
            if hasattr(self, '_m_dest_ssid'):
                return self._m_dest_ssid if hasattr(self, '_m_dest_ssid') else None

            self._m_dest_ssid = ((self.dest_ssid_raw & 15) >> 1)
            return self._m_dest_ssid if hasattr(self, '_m_dest_ssid') else None


    class UiFrame(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.pid = self._io.read_u1()
            self.ax25_info = self._io.read_bytes_full()


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


    class IFrame(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.pid = self._io.read_u1()
            self.ax25_info = self._io.read_bytes_full()


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



