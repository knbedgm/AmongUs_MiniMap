from scapy.layers.inet import IP

from AmongUsData.Hazel import *
from scapy.all import send

data = "0E 00 05 20 00 00 00 07 00 02 04 0D 04 74 65 73 74"

dip = "192.168.151.182"
sip = "192.168.151.145"
dport = 62846
sport = 22023

pkt = IP(src=sip, dst=dip)/UDP(sport=sport, dport=dport)/HazelPacket(b'\x00')/Raw(bytes.fromhex(data))

#pkt.show()
#pkt.show2()
send(pkt)

# a = sniff(filter="udp and port 22023", count=10)
#
# for i in a:
#     print("\n\n\n\n")
#     i[HazelPacket].show()
#     input()
