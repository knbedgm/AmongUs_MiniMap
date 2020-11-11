import asyncio

from scapy.packet import Raw
from scapy.scapypipes import WiresharkSink

from AmongUsData import AUPackets, Hazel, AUGame

from web_test import *

game = AUGame(log=True)


@game.event("movement")
def move(pkt: AUPackets.GPMovement):
    asyncio.run(send(pkt))


async def send(pkt):
    await sio.emit("movement", data={"id": pkt.player_number, "count": pkt.Counter, "x": pkt.XPos, "y": pkt.YPos}, room="map")


# @game.event("unknown")
def unk_log(pkt: Raw):
    pass
    # fl = pkt.firstlayer()
    # # if not fl[Hazel.HazelPacket].fromServer() and fl[Hazel.HazelPacket].header == Hazel.HazelPacket.header.s2i["Unreliable"]:
    # #     fl[AUPackets.INPBase].printPkt()
    # if fl[Hazel.HazelPacket].header == 8:
    #     fl[AUPackets.INPBase].printPkt()


# wss = WiresharkSink()
# game.scapy_output_pipe > wss

game.start()  # start game interceptor (nonblocking)
run()  # start webserver (nonblocking)
print("running")
input()
game.stop()
