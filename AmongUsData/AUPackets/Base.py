from scapy.fields import ByteEnumKeysField
from scapy.layers.inet import UDP
from scapy.packet import Packet, bind_layers
from scapy.utils import hexstr

from AmongUsData.Hazel import *


class AUPBase(Packet):
    name = "AUPBase"
    fields_desc = [
        ByteEnumKeysField("header", 0, {0x12: "Movement", 0x16: "CosmeticChange", 0x36: "SettingsChange"})
    ]

    def printPkt(self):
        if self.header == 0xff:
            return
        fl = self.firstlayer()
        if fl[HazelPacket].fromServer():
            print(f"> {HazelPacket.header.i2s[fl[HazelPacket].header]:>10} ", end="")
        else:
            print(f"< {HazelPacket.header.i2s[fl[HazelPacket].header]:>10} ", end="")
        print(hexstr(self))


bind_layers(HazelPacket, AUPBase)
bind_layers(HazelReliable, AUPBase)

__all__ = ['AUPBase']
