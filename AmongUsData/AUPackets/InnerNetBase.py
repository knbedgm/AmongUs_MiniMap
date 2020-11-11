from scapy.compat import raw
from scapy.fields import LEShortField, ByteField
from scapy.packet import Packet, bind_layers
from scapy.utils import hexstr

from AmongUsData.AUPackets.InnerNetHello import INPHello
from AmongUsData.Hazel import HazelPacket


class INPBase(Packet):
    name = "INPBase"
    fields_desc = [
        LEShortField("len", 0),
        ByteField("type", 5),
    ]

    def printPkt(self):
        print("DEP: use summary")
        print(self.mysummary())

    def mysummary(self):
        out = ""
        fl = self.firstlayer()
        if fl[HazelPacket].fromServer():
            out += f"> INH{self.type:<7} "
        else:
            out += f"< INH{self.type:<7} "
        out += hexstr(raw(self)[3:])
        return out

bind_layers(HazelPacket, INPHello, header=8)  # Must be registered before INPBase
bind_layers(HazelPacket, INPBase)

__all__ = ['INPBase']
