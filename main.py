from AmongUsData import AUPackets
from AmongUsData import AUGame

game = AUGame(log=True)


def move(pkt: AUPackets.AUPMovement):
    print(pkt.XPos)

# game.events.on_movement += move

game.start()
print("running")
input()
game.stop()
