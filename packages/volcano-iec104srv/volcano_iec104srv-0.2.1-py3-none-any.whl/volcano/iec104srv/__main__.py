#!/usr/bin/python3

import argparse
import sys
import logging

from twisted.internet import reactor
from twisted.internet.error import CannotListenError

from volcano.general.log import configure_arg_parser_for_log, configure_logger
from volcano.general.xml_reader import LoadException, load_xml_file_le, XmlReader
from volcano.general.stddef import VOLCANO_DEFAULT_TCP_PORT
from volcano.general.stdsvc import SingleThreadAllService

from volcano.twistedclient.twisted_factory import VolcanoTwistedFactory
from volcano.twistedclient.twisted_client_st import VolcanoTwistedClientST

from .iec_server import IECServer
from .iec_factory import IECFactory


def configure_my_args(parser):
    parser.add_argument('--core_host', help='Volcano core host', default='localhost')
    parser.add_argument('--core_port', help='Volcano core port', default=VOLCANO_DEFAULT_TCP_PORT, type=int)
    parser.add_argument('-n', '--name', help='Instance name', default='iec104srv')
    parser.add_argument('-f', '--file', help='Config file', default='iec104srv.xml')
    parser.add_argument('-i', '--iface', help='Listen interface', default='')
    parser.add_argument('-p', '--port', help='Listen port', type=int, default=2000)
    parser.add_argument('-m', '--max_con', help='Max number of connections', type=int, default=2)


class MyVolcanoClient(VolcanoTwistedClientST):
    def __init__(self, server: IECServer, env, log):
        assert isinstance(server, IECServer), server

        super().__init__(log)

        assert self.log

        self.server = server
        self.env = env
        self.all_svc_ = None        # all-in-one service

    def connectionMade(self):
        super().connectionMade()

        self.log.info('Connected to core')

        self.all_svc_ = SingleThreadAllService(transport=self)
        self.all_svc_.salute(self.env.name)

        self.server.sync(find_tag_svc=self.all_svc_, sub_svc=self.all_svc_)

        self.all_svc_.echo(self.sync_complete)

    def sync_complete(self):
        self.log.info('Start listen: iface={} port={}'.format(self.env.iface, self.env.port))
        try:
            reactor.listenTCP(self.env.port, IECFactory(self.env, self.log), interface=self.env.iface)
        except CannotListenError as ex:
            self.log.error(ex)
            reactor.stop()

    def on_msg_rcvd_no_exc(self, msg: dict):
        assert isinstance(msg, dict), msg

        try:
            self.all_svc_.push_single_message(msg)  # this can cause exceptions like Warnings
        except Warning as ex:
            self.log.error(ex)
            self.close_transport_from_mt()


def main():
    try:
        # Args
        arg_parser = argparse.ArgumentParser()
        configure_my_args(arg_parser)
        configure_arg_parser_for_log(arg_parser)        # let logger add his arguments for later configure_logger() call
        env = arg_parser.parse_args()

        # Logging
        configure_logger(env)
        log = logging.getLogger(env.name)   # should log under our instance name

        # Server
        server = IECServer(env, log)
        try:
            server.load_le()
        except LoadException as ex:
            log.error(ex)
            return 1

        # Launch
        client = MyVolcanoClient(server, env, log)
        volcano_factory = VolcanoTwistedFactory()
        volcano_factory.log = log
        volcano_factory.client = client

        log.info('Connect to core at %s:%s', env.core_host, env.core_port)
        reactor.connectTCP(env.core_host, env.core_port, volcano_factory)
        reactor.run()

        return 0

    finally:
        logging.shutdown()      # safe to call even if logging.init was not called - tested it without exception


if __name__ == '__main__':
    sys.exit(main())
