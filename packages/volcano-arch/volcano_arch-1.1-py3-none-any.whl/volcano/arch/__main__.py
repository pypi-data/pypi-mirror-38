#!/usr/bin/python3

import argparse
import sys
import logging

from twisted.internet import reactor

from volcano.general.log import configure_arg_parser_for_log, configure_logger
from volcano.general.xml_reader import LoadException, load_xml_file_le, XmlReader
from volcano.general.stddef import VOLCANO_DEFAULT_TCP_PORT
from volcano.general.stdsvc import SingleThreadAllService

from volcano.twistedclient.twisted_factory import VolcanoTwistedFactory
from volcano.twistedclient.twisted_client_st import VolcanoTwistedClientST

from .archive import Archive


def configure_my_args(parser):
    parser.add_argument('--core_host', help='Volcano core host', default='localhost')
    parser.add_argument('--core_port', help='Volcano core port', default=VOLCANO_DEFAULT_TCP_PORT, type=int)
    parser.add_argument('-n', '--name', help='Instance name', default='arch')
    parser.add_argument('-f', '--file', help='Config file', default='arch.xml')


class MyVolcanoClient(VolcanoTwistedClientST):
    def __init__(self, factory: 'MyLavaFactory'):
        super().__init__(logging.getLogger(factory.env.name))
        self.all_svc_ = None
        self.factory_ = factory

    def connectionMade(self):
        super().connectionMade()

        self.all_svc_ = SingleThreadAllService(self)
        self.all_svc_.salute( self.factory_.env.name)

        for mod in self.factory_.modules:
            mod.sync(find_tag_svc=self.all_svc_, subs_svc=self.all_svc_)
        self.all_svc_.echo(self.sync_complete)

    def sync_complete(self):
        self.factory_.start()

    def on_msg_rcvd_no_exc(self, msg: dict) -> None:   # Exceptions not expected
        self.all_svc_.push_single_message(msg)


class MyLavaFactory(VolcanoTwistedFactory):
    env = None
    threads_started = False
    modules = []

    def load(self):
        cfg = load_xml_file_le(self.env.file)
        for node in cfg.getroot():
            if node.tag != 'Archive':
                raise LoadException('Unknown node name "{}". Use "Archive"'.format(node.tag), node)

            mod = Archive(node, self.log)

            self.modules.append(mod)

        if not self.modules:
            raise LoadException('No modules configured')

    def buildProtocol(self, addr):
        return MyVolcanoClient(self)

    def start(self):
        assert not self.threads_started

        self.threads_started = True
        for arc in self.modules:
            arc.start()

    def stop(self):
        if self.threads_started:    # if we fail on sync, threads are still not started
            self.log.info('Stop all threads...')
            for mod in self.modules:
                mod.stop_async()

            for mod in self.modules:
                self.log.info('Wait %s...' % mod)
                mod.join()


def main():
    # Args
    arg_parser = argparse.ArgumentParser()
    configure_my_args(arg_parser)
    configure_arg_parser_for_log(arg_parser)  # let logger add his arguments for later configure_logger() call
    env = arg_parser.parse_args()

    # Logging
    configure_logger(env)
    log = logging.getLogger(env.name)

    volcano_factory = MyLavaFactory()
    volcano_factory.log = log
    volcano_factory.env = env

    try:
        volcano_factory.load()
    except LoadException as ex:
        log.error(ex)
        return 1

    log.info('Connect to core at {}:{}'.format(env.core_host, env.core_port))
    reactor.connectTCP(env.core_host, env.core_port, volcano_factory)

    try:
        reactor.run()
    finally:
        volcano_factory.stop()

    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    finally:
        logging.shutdown()
