import json
import json.decoder
import threading

from twisted.internet import task
from twisted.protocols.basic import LineReceiver

from volcano.general.stdsvcdef import IMsgOStream


#    Базовый класс для многопоточных клиентов на базе Twisted.
#    Реализует внутренние очереди сообщений
class VolcanoTwistedClientMT(LineReceiver, IMsgOStream):
    delimiter = b'\n'

    def __init__(self, log):
        super().__init__()
        self.log = log
        self.outbox_ = []  # list of msgs
        self.lock_ = threading.Lock()
        self.looping_call_handler_ = None

    def on_msg_rcvd_mt(self, msg: dict) -> None:
        raise NotImplementedError()

    def connectionMade(self):
        self.looping_call_handler_ = task.LoopingCall(self.looping_call_)  # looping_call_.stop() will stop the looping calls
        self.looping_call_handler_.start(0.01)

    def looping_call_(self):
        self.lock_.acquire()
        try:
            for msg in self.outbox_:
                self.sendLine(json.dumps(msg).encode('utf-8'))
            self.outbox_ = []
        finally:
            self.lock_.release()

    def lineReceived(self, line: bytes) -> None:
        assert isinstance(line, bytes), line

        try:
            line_s = line.decode('utf-8', 'strict').strip()
        except UnicodeDecodeError as ex:
            self.log.error('Error decoding command to utf-8: %s. Command: %s', ex, line)
            self.close_transport_from_mt()
            return

        if not line_s:
            return

        try:
            msg = json.loads(line_s)
        except json.decoder.JSONDecodeError as ex:
            self.log.error('Error processing <%s>: %s', line_s, ex)
            self.close_transport_from_mt()
            return

        try:
            self.on_msg_rcvd_mt(msg)
        except Exception as ex:
            self.log.error('Unexpected error while processing <%s>: %s', line_s, ex)
            raise

    # IMsgOStream
    def push_single_message(self, msg: dict) -> None:
        assert isinstance(msg, dict), msg
        self.lock_.acquire()
        try:
            self.outbox_.append(msg)
        finally:
            self.lock_.release()

    def close_transport_from_mt(self):
        if self.transport:
            self.transport.loseConnection()
