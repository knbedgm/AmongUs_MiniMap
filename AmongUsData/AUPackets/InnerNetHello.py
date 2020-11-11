from scapy.fields import *
from scapy.packet import Packet, bind_layers
from scapy.utils import hexstr

from AmongUsData.Hazel import HazelPacket


class INPHello(Packet):
    name = "INPHello"
    fields_desc = [
        NBytesField("Unknown", b'\0\x80\xd9\2\3', 5),
        FieldLenField("name_len", 6, length_of="player_name", fmt="B"),
        StrLenField("player_name", "Player", length_from=lambda pkt: pkt.name_len),
    ]

    def printPkt(self):
        print("DEP: use summary")
        print(self.mysummary())

    def mysummary(self):
        out = ""

        if self.firstlayer()[HazelPacket].fromServer():
            out += f"> {'Hello':>10} "
        else:
            out += f"< {'Hello':>10} "

        out += f"N: {self.player_name}"

        if self.Unknown != 12930613248:
            out += f"(new Unk in field: {hexstr(raw(self)[:5])}"
        return out


__all__ = ['INPHello']
