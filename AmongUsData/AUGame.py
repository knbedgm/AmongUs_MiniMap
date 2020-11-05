from events import Events
from scapy.packet import Raw, Packet
from scapy.pipetool import PipeEngine, Drain, TransformDrain
from scapy.scapypipes import SniffSource
from AmongUsData import HazelReliableDrain
from AmongUsData.AUPackets import *
from AmongUsData.Hazel import HazelPacket


class AUGame:
    def __init__(self, log=False):
        self.log = log

        self.events = Events(("on_disconnect", "on_movement", "on_join", "on_cosmetic", "on_unknown"))

        self._packet_source = SniffSource(
            filter="udp and (port 22023 or port 22123 or port 22223 or port 22323 or port 22423 or port 22523 or port 22623 or port 22723 or port 22823 or port 22923)")
        self._hazel_filter = HazelReliableDrain()
        self._pipe_engine = PipeEngine(self._packet_source)

        self._packet_source > self._hazel_filter

        self.scapy_output_pipe = Drain()
        self._hazel_filter > self.scapy_output_pipe

        self._hazel_filter > TransformDrain(self._packet_in)

    def _handle_movement(self, pkt: AUPMovement):
        if self.log:
            pkt.printPkt()
        self.events.on_movement(pkt)

    def _handle_unknown(self, pkt: Packet):
        if self.log:
            pkt.firstlayer()[AUPBase].printPkt()
        self.events.on_unknown(pkt)

    _handlers = {
        AUPMovement: _handle_movement,
        Raw: _handle_unknown
    }

    def _packet_in(self, pkt):
        if AUPBase in pkt:
            base_payload = pkt[AUPBase].payload
            try:
                self._handlers[type(base_payload)](self, base_payload)
            except Exception as e:
                print(e)
        elif HazelPacket in pkt:
            hazel = pkt[HazelPacket]
            if hazel.header == HazelPacket.header.s2i["Disconnect"]:
                if self.log:
                    print(f"{'>' if hazel.fromServer() else '<'} Disconnect")
                self.events.on_disconnect()
        return pkt

    def start(self):
        self._pipe_engine.start()
        self._hazel_filter.reset()

    def stop(self):
        self._pipe_engine.stop()


