from scapy.fields import *
from scapy.packet import Packet, bind_layers
from scapy.utils import hexstr

from AmongUsData.AUPackets import INPBase
from AmongUsData.Hazel import HazelPacket


class GameBase(Packet):
    name = "GameBase"
    fields_desc = [
        XNBytesField("GameCode", b'\0\0\0\0', 4),
        LEShortField("len", 0xB0),
        ByteField("type", 1),
    ]

    def printPkt(self):
        print("DEP: use summary")
        print(self.mysummary())

    def mysummary(self):
        out = ""
        fl = self.firstlayer()
        if fl[HazelPacket].fromServer():
            out += f"> {'GameBase':>10} "
        else:
            out += f"< {'GameBase':>10} "
        out += hexstr(self)
        return out


bind_layers(INPBase, GameBase, type=5)

__all__ = ['GameBase']
