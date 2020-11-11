from scapy.all import *
from scapy.layers.inet import UDP

from AmongUsData import *
from AmongUsData.Hazel import *

# packets = sniff(filter="tcp and port 9000", count=1, iface=conf.route.route('127.0.0.1')[0])
# print(packets.nsummary())

# source = SniffSource(iface=conf.route.route('127.0.0.1')[0])


source = SniffSource(
    filter="udp and (port 22023 or port 22123 or port 22223 or port 22323 or port 22423 or port 22523 or port 22623 or port 22723 or port 22823 or port 22923)")
cons = ConsoleSink()

# wshark = WiresharkSink()


def logger(pkt):
    if not pkt or HazelPacket not in pkt:
        return pkt
    # print("gotpkt")
    # print(HazelPacket.header.i2s[pkt[HazelPacket].header])
    if pkt[HazelPacket].header <= 9:
        if pkt[HazelPacket].fromServer():
            print(f">{HazelPacket.header.i2s[pkt[HazelPacket].header]:>10} ", end="")
        else:
            print(f"<{HazelPacket.header.i2s[pkt[HazelPacket].header]:>10} ", end="")
        print(hexstr(pkt[HazelPacket]))
    return pkt


def logMvmnt(pkt):
    if not pkt or AUPackets.GPMovement not in pkt:
        return
    pkt[AUPackets.GPMovement].printPkt()


def logAU(pkt: Packet):
    if not pkt or AUPackets.INPBase not in pkt:
        return
    try:
        pkt[AUPackets.INPBase].payload.printPkt()
    except:
        pkt[AUPackets.INPBase].printPkt()


def test(pkt: Packet):
    print("packet")

hazelFilter = HazelFilterDrain()

# source > TransformDrain(filterHazel)

source > hazelFilter
# hazelFilter > TransformDrain(test)
# source > wshark
hazelFilter > cons

p = PipeEngine(source)
# source > wshark
p.start()
print("running")
input()
# hazelFilter.reset()
# print('\n\nReset\n')
#
# input()
p.stop()
