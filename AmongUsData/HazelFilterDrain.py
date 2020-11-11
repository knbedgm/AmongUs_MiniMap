from scapy.all import *
from AmongUsData.Hazel import HazelPacket


def _filter(index: int, missed: set, last: int, first: bool) -> (bool, int):
    overwrite = (index + 32768) % 65535  # place overwrite pointer half the buffer away from the last good read
    isNew = False

    # decide if the new packet is new or possibly a duplicate
    if overwrite < last:
        isNew = overwrite >= index or index > last
    else:
        isNew = overwrite >= index > last

    # if this is a new packet or the first packet
    if isNew or first:
        for i in range(last + 1, index):
            missed.add(i)  # mark all packets between this one and the last one we received as missed
        last = index  # this is the new last one we received

        # print(f"{index:3}: New")
        return True, last
    else:
        if index in missed:
            missed.remove(index)
            # print(f"{index:3}: Missed")
            return True, last
        # print(f"{index:3}: Dupe")
    return False, last


class HazelFilterDrain(Drain):

    def __init__(self, name=None):
        Drain.__init__(self, name=name)
        self.clientLast = 0
        self.serverLast = 0
        self.clientMissed = set()
        self.serverMissed = set()
        self.serverFirst = True
        self.clientFirst = True

    def reset(self):
        self.clientLast = 0
        self.serverLast = 0
        self.clientMissed = set()
        self.serverMissed = set()
        self.serverFirst = True
        self.clientFirst = True

    def _doFilter(self, msg: Packet, sendf: Callable[[Packet], None]):
        if HazelPacket in msg:
            if msg[HazelPacket].header == HazelPacket.header.s2i['Disconnect']:
                self.reset()
                # print("Rst")
            if msg[HazelPacket].header == HazelPacket.header.s2i['Ack']:
                # print("ack")
                return
            if msg[HazelPacket].header == HazelPacket.header.s2i['Ping']:
                # print("ping")
                return

            if not msg[HazelPacket].index is None:
                new: bool
                if msg[HazelPacket].fromServer():
                    # print("s", end='')
                    new, self.serverLast = _filter(msg[HazelPacket].index, self.serverMissed, self.serverLast,
                                                   self.serverFirst)
                    self.serverFirst = False
                    if new: sendf(msg)

                else:  # packet from client
                    # print("c", end='')
                    new, self.clientLast = _filter(msg[HazelPacket].index, self.clientMissed, self.clientLast,
                                                   self.clientFirst)
                    self.clientFirst = False
                    if new: sendf(msg)
            else:
                sendf(msg)
        else:
            sendf(msg)

    def push(self, msg):
        self._doFilter(msg, self._send)

    def high_push(self, msg):
        self._doFilter(msg, self._high_send)
