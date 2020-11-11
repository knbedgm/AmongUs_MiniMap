from events import Events
from scapy.packet import Raw, Packet, NoPayload, Padding
from scapy.pipetool import PipeEngine, Drain, TransformDrain
from scapy.scapypipes import SniffSource, WiresharkSink
from AmongUsData import HazelFilterDrain
from AmongUsData.AUPackets import *
from AmongUsData.Hazel import HazelPacket


class AUGame:
    def __init__(self, log=False):
        self.log = log

        self.events = Events(
            ("disconnect", "movement", "join", "cosmetic_change", "unknown", "start_game", "end_game", "meeting", "other", "hello",))

        self._packet_source = SniffSource(
            filter="udp and (port 22023 or port 22123 or port 22223 or port 22323 or port 22423 or port 22523 or port 22623 or port 22723 or port 22823 or port 22923)",
            # iface=
        )
        self._hazel_filter = HazelFilterDrain()
        self._pipe_engine = None

        self._packet_source > self._hazel_filter

        self.scapy_output_pipe = Drain()
        self._hazel_filter > self.scapy_output_pipe

        self._hazel_filter > TransformDrain(self._packet_in)

    def event(self, event_name):  # decorator wrapper for events
        def wrap(f):
            e = self.events.__getattr__(event_name)
            e += f  # Im aware this could be a oneliner but my code checker says I cant add to a function call :(
            return f

        return wrap

    def _handle_movement(self, pkt: GPMovement):
        if self.log:
            print(pkt.mysummary())
        self.events.movement(pkt)

    def _handle_unknown(self, pkt: Packet):
        if self.log:
            print(pkt.underlayer.mysummary())
        self.events.unknown(pkt)

    def _handle_hello(self, pkt: INPHello):
        if self.log:
            print(pkt.mysummary())
        self.events.hello(pkt)

    def _handle_other(self, pkt: Packet):
        if self.log:
            pkt.firstlayer().show()
            print("Other")
        self.events.other(pkt)

    def _handle_disconnect(self, pkt: HazelPacket):
        if pkt.header == HazelPacket.header.s2i["Disconnect"]:
            if self.log:
                print(f"{'>' if pkt.fromServer() else '<'} Disconnect")
            self.events.disconnect()

    _handlers = {
        GPMovement: _handle_movement,
        Raw: _handle_unknown,
        INPBase: _handle_unknown,
        INPHello: _handle_hello,
    }

    def _packet_in(self, pkt: Packet):
        try:
            if INPBase in pkt or INPHello in pkt:
                base_payload = pkt.lastlayer()
                if type(base_payload) is Padding:
                    base_payload = base_payload.underlayer
                try:
                    self._handlers[type(base_payload)](self, base_payload)
                except Exception as e:
                    print("Exception:")
                    print(e)
                    base_payload.firstlayer().show()
            elif HazelPacket in pkt and pkt[HazelPacket].header == HazelPacket.header.s2i["Disconnect"]:
                self._handle_disconnect(pkt[HazelPacket])
            else:
                self._handle_other(pkt)
            return pkt
        except Exception as e:
            pkt.show()
            print(e)

    def start(self):
        self._pipe_engine = PipeEngine(self._packet_source)
        self._hazel_filter.reset()
        self._pipe_engine.start()

    def stop(self):
        self._pipe_engine.stop()
