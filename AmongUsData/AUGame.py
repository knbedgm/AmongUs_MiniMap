from events import Events
from scapy.pipetool import PipeEngine
from scapy.scapypipes import SniffSource
from AmongUsData import HazelReliableDrain



class AUGame:
    def __init__(self):
        self.events = Events(("on_disconnect", "on_movement", "on_join", "on_cosmetic"))

        self._packet_source = SniffSource(filter="udp and (port 22023 or port 22123 or port 22223 or port 22323 or port 22423 or port 22523 or port 22623 or port 22723 or port 22823 or port 22923)")
        self._hazel_filter = HazelReliableDrain()
        self._pipe_engine = PipeEngine(self._packet_source)

        self._packet_source > self._hazel_filter


    def start(self):
        self._pipe_engine.start()
        self._hazel_filter.reset()
