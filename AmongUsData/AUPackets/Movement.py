from scapy.compat import raw
from scapy.fields import NBytesField, ByteField, LEShortField, LESignedShortField
from scapy.packet import Packet, bind_layers
from scapy.utils import hexstr

from AmongUsData.AUPackets import AUPBase


class AUPMovement(Packet):
    name = "AUPMovement"
    fields_desc = [
        NBytesField("Unknown", b'\x00\x05', 2),
        NBytesField("GameCode", b'\0\0\0\0', 4),
        NBytesField("Unknown", b'\x0B\0\1', 3),
        ByteField("PlayerNumber", b'\6'),
        LEShortField("Counter", 0),
        LEShortField("XPos", 0),
        LEShortField("YPos", 0),
        LESignedShortField("XSpd", 0),
        LESignedShortField("YSpd", 0)
    ]

    def printPkt(self):
        print(f"{self.PlayerNumber}: ({self.XPos:5},{self.YPos:5}) @ ({self.XSpd:6},{self.YSpd:6}) {{{hexstr(raw(self)[-4:])}}}")

bind_layers(AUPBase, AUPMovement, header=0x12)

__all__ = ['AUPMovement']
