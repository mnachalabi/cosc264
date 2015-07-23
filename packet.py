"""
Defines the packet data structure, along with routines to parse and
serialize it.
"""

from collections import namedtuple
from enum import Enum
from struct import Struct


MAGIC_NUMBER = 0x497E


class Packet(namedtuple('Packet', 'type_ seqno data')):
    struct = Struct('!iiii')

    @classmethod
    def from_bytes(cls, buf):
        """Parse a packet from a bytes object."""
        magicno, type_, seqno, data_len = cls.struct.unpack(buf[:cls.struct.size])
        if magicno != MAGIC_NUMBER:
            raise ValueError('magic number mismatch')
        type_ = PacketType(type_)
        data = buf[cls.struct.size:]
        if len(data) != data_len:
            raise ValueError('data length mismatch')
        return Packet(type_, seqno, data)

    def to_bytes(self):
        """Serialize a packet to a bytes object."""
        header = self.struct.pack(
                MAGIC_NUMBER, self.type_.value, self.seqno, len(self.data))
        return header + self.data


class PacketType(Enum):
    data = 0
    ack = 1
