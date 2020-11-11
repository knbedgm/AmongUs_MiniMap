import asyncio

from scapy.packet import Raw
from scapy.scapypipes import WiresharkSink

from AmongUsData import AUPackets, Hazel, AUGame

from web_test import *

game = AUGame(log=False)

current_map = 0


@game.event("movement")
def move(pkt: AUPackets.GPMovement):
    sendMovement(pkt)


def sendMovement(pkt):
    asyncio.run(sio.emit("movement", data={"id": pkt.player_number, "count": pkt.Counter, "x": pkt.XPos, "y": pkt.YPos}))


def sendMap(map_num):
    asyncio.run(sio.emit("changeMap", data={"id": map_num}))


def sendErase():
    asyncio.run(sio.emit("erase"))


@sio.event
async def connect(sid, environ):
    await sio.emit("changeMap", data={"id": current_map}, to=sid)


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
print("running: http://localhost:8080")
print("\nCommands:\n0:Exit\n1:Skeld\n2:MiraHQ\n3:Polus\n9:Erase\n")
while True:
    try:
        num = int(input("m#: "))
        if 1 <= num <= 3:
            sendMap(num-1)
            current_map = num-1
        elif num == 0:
            break
        elif num == 9:
            sendErase()
        else:
            raise ValueError()
    except ValueError:
        print("invalid")
game.stop()
