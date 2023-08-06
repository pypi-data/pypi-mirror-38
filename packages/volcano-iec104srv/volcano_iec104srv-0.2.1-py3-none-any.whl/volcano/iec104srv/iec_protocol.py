
from twisted.internet.protocol import Protocol, connectionDone


class IECProtocol(Protocol):
    def __init__(self, factory, parent_log):
        self.factory = factory
        self.log = parent_log

    def dataReceived(self, data: bytes):
        assert isinstance(data, bytes), data

        self.log.debug(data)

    def connectionMade(self):
        pass

    def connectionLost(self, reason=connectionDone):
        self.factory.on_connection_lost(self)
