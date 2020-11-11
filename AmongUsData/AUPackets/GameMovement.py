from scapy.fields import LEShortField, LESignedShortField
from AmongUsData.AUPackets.BitExtendedField import AUBitExtendedField

from scapy.packet import Packet, bind_layers
from scapy.utils import hexstr
from scapy.compat import raw

from AmongUsData.AUPackets.GameBase import GameBase


class GPMovement(Packet):
    name = "GPMovement"
    fields_desc = [
        AUBitExtendedField("player_number", b'\6'),
        LEShortField("Counter", 0),
        LEShortField("XPos", 0),
        LEShortField("YPos", 0),
        LESignedShortField("XSpd", 0),
        LESignedShortField("YSpd", 0)
    ]

    def printPkt(self):
        print("DEP: use summary")
        print(self.mysummary())

    def mysummary(self):
        return f"{self.player_number:>3}: ({self.XPos:5},{self.YPos:5}) @ ({self.XSpd:6},{self.YSpd:6}) {{{hexstr(raw(self)[-4:])}}}"


bind_layers(GameBase, GPMovement, type=1)

__all__ = ['GPMovement']
