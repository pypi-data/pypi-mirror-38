import json
import json.decoder

from twisted.protocols.basic import LineReceiver

from volcano.general.stdsvcdef import IMsgOStream

#    Базовый класс для однопоточных клиентов на базе Twisted.
class VolcanoTwistedClientST(LineReceiver, IMsgOStream):
    delimiter = b'\n'

    def __init__(self, log):
        super().__init__()
        self.log = log

    def connectionMade(self):
        pass

    # Данный метод не предполагает того, что будет выброшен Exception. Причина в следующем:
    # чтобы разделить ожидаемые Exception от неожиданных (ошибок в программе), приходится
    # оговаривать, какой Exception будет считать ожидаемым, чтобы его маскировать в log.warn()
    # Но в этом случае все равно код внутри должен будет поймать свои Exception и завернуть их в ожидаемый.
    # Тогда нахрена все это надо, если можно просто сделать дисконнект?
    #
    # Вобщем, при необходимости закрыть канал следует вызвать self.close_transport_from_mt()
    # Это правильно, потому что обработчик вызывается в главном потоке.
    def on_msg_rcvd_no_exc(self, msg: dict) -> None:   # Exceptions not expected
        raise NotImplementedError()

    def rawDataReceived(self, data):
        assert False    # we never work in raw mode

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
            self.on_msg_rcvd_no_exc(msg)
        except Exception as ex:
            self.log.error('Unexpected error while processing <%s>: %s', line_s, ex)
            raise

    # IMsgOStream
    def push_single_message(self, msg: dict):
        self.sendLine(json.dumps(msg).encode('utf-8'))

    def close_transport_from_mt(self):
        if self.transport:
            self.transport.loseConnection()
