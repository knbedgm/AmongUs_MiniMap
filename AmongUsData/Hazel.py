from scapy.layers.inet import UDP
from scapy.packet import Packet, bind_layers, Raw
from scapy.fields import ByteEnumKeysField, ShortField, ByteField


class HazelPacket(Packet):
    name = "HazelPacket"
    fields_desc = [
        ByteEnumKeysField("header", 0,
                          {0: "Unreliable", 1: "Reliable", 8: "Hello", 9: "Disconnect", 10: "Ack", 12: "Ping"})
    ]

    def hasData(self):
        if self.header <= 9 and Raw in self:
            return True
        else:
            return False

    def fromServer(self):
        sport = self.firstlayer()[UDP].sport
        if sport == 22023:
            return True
        if sport == 22123:
            return True
        if sport == 22223:
            return True
        if sport == 22323:
            return True
        if sport == 22423:
            return True
        if sport == 22523:
            return True
        if sport == 22623:
            return True
        if sport == 22723:
            return True
        if sport == 22823:
            return True
        if sport == 22923:
            return True


for port in (22023, 22123, 22223, 22323, 22423, 22523, 22623, 22723, 22823, 22923):
    bind_layers(UDP, HazelPacket, dport=port)
    bind_layers(UDP, HazelPacket, sport=port)


class HazelReliable(Packet):
    name = "HazelReliable"
    fields_desc = [
        ShortField("id", 41)
    ]


bind_layers(HazelPacket, HazelReliable, header=1)
bind_layers(HazelPacket, HazelReliable, header=8)
bind_layers(HazelPacket, HazelReliable, header=12)


class HazelAck(Packet):
    name = "HazelReliable"
    fields_desc = [
        ShortField("id", 41),
        ByteField("Unknown", 0xff)
    ]


bind_layers(HazelPacket, HazelAck, header=10)

__all__ = ['HazelPacket', 'HazelReliable', 'HazelAck']