
from twisted.internet.protocol import Protocol, Factory

from .iec_protocol import IECProtocol


class DropProtocol(Protocol):
    def connectionMade(self):
        self.transport.loseConnection()


class IECFactory(Factory):
    drop_protocol = DropProtocol()

    def __init__(self, env, log):
        super().__init__()

        assert env.max_con

        self.env = env
        self.log = log

        self.connections = []

    def buildProtocol(self, addr):
        if len(self.connections) >= self.env.max_con:
            self.log.warning('Max number of connections [{}] reached'.format(self.env.max_con))
            return self.drop_protocol   # to check if possible to return same instance every time

        proto = IECProtocol(self, self.log)
        self.connections.append(proto)
        return proto

    def on_connection_lost(self, proto):
        self.connections.remove(proto)
