from scapy.all import *
from AmongUsData.Hazel import HazelReliable, HazelPacket


class HazelReliableDrain(Drain):
    def _filter(self, id: int, missed: set, last: int, first: bool) -> (bool, int):
        overwrite = (id + 32768) % 65535  # place overwrite pointer half the buffer away from the last good read
        isNew = False

        # decide if the new packet is new or possibly a duplicate
        if overwrite < last:
            isNew = overwrite >= id or id > last
        else:
            isNew = overwrite >= id > last

        # if this is a new packet or the first packet
        if isNew or first:
            for i in range(last + 1, id):
                missed.add(i)  # mark all packets between this one and the last one we received as missed
            last = id  # this is the new last one we received

            # print(f"{id:3}: New")
            return True, last
        else:
            if id in missed:
                missed.remove(id)
                # print(f"{id:3}: Missed")
                return True, last
            # print(f"{id:3}: Dupe")
        return False, last

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
        if msg[HazelPacket].header == HazelPacket.header.s2i['Disconnect']:
            self.reset()
        if HazelReliable in msg:
            new: bool

            if msg[HazelPacket].fromServer():
                # print("s",end='')
                new, self.serverLast = self._filter(msg[HazelReliable].id, self.serverMissed, self.serverLast, self.serverFirst)
                self.serverFirst = False
                if new: sendf(msg)

            else:  # packet from client
                # print("c", end='')
                new, self.clientLast = self._filter(msg[HazelReliable].id, self.clientMissed, self.clientLast,
                                                    self.clientFirst)
                self.clientFirst = False
                if new: sendf(msg)
        else:
            sendf(msg)

    def push(self, msg):
        self._doFilter(msg, self._send)

    def high_push(self, msg):
        self._doFilter(msg, self._high_send)
