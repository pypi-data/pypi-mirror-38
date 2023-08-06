#!/usr/bin/python3
import argparse
import logging
import sys
from time import perf_counter

from twisted.internet.protocol import Factory, Protocol
from twisted.internet import reactor, stdio, task
from twisted.internet.error import CannotListenError

# volcano
from volcano.general.stddef import VOLCANO_DEFAULT_TCP_PORT, Quality
from volcano.general.log import configure_arg_parser_for_log, configure_logger
from volcano.general.xml_reader import LoadException
from volcano.general import variant

# locals
from .db import Db, Tag
from .cvt import StdValueCvt
from .cp import TTYControlPanel
from .connection import Connection


class DropProtocol(Protocol):
    def connectionMade(self):
        self.transport.loseConnection()


def configure_my_args(parser):
    parser.add_argument('-f', '--file', help='Config file', default='db.xml')
    parser.add_argument('-i', '--iface', help='Listen interface', default='')
    parser.add_argument('-p', '--port', help='Listen port', type=int, default=VOLCANO_DEFAULT_TCP_PORT)
    parser.add_argument('--demo', help='Turn on demo mode', action='store_true')
    parser.add_argument('--max_con', help='Max number of connections', type=int, default=5, choices=range(1, 10))

    parser.add_argument('--log_tag_upd', help='Log tag udates', action='store_true')


class VolcanoServer(Factory):
    def __init__(self, db, env, log):
        self.db = db        # pylint: disable=invalid-name
        self.env = env
        self.log = log

        self.connections = []
        self.value_cvt_ = StdValueCvt()

        self.sys_tags_ = {
            'fps_in': self.db.create_tag_by_long_name(None, 'sys.fps_in', variant.IntValue(), Quality.QUALITY_GOOD),
            'fps_out': self.db.create_tag_by_long_name(None, 'sys.fps_out', variant.IntValue(), Quality.QUALITY_GOOD),
        }
        self.nb_msg_in_ = 0
        self.nb_msg_out_ = 0
        self.fps_tstamp_ = perf_counter()

        self.timer_handler_ = task.LoopingCall(self.on_timer_)  # stop() will stop the looping calls
        self.timer_handler_.start(1.0)

    def value_cvt(self):
        return self.value_cvt_

    def buildProtocol(self, addr):
        if len(self.connections) >= self.env.max_con:
            self.log.warning('Max number of connections (%s pcs) reached, new one is dropped', self.env.max_con)
            return DropProtocol()

        con = Connection(self, self.db, self.env, self.log)

        self.connections.append(con)
        self.log.info('New connection. Nb connections: %s', len(self.connections))
        return con

    def forget(self, con):
        self.connections.remove(con)
        self.log.info('Connection removed. Nb connections: %s', len(self.connections))

    def on_timer_(self):
        t = perf_counter()
        secs = t - self.fps_tstamp_
        if secs > 0:
            fps_in = self.nb_msg_in_ / secs
            fps_out = self.nb_msg_out_ / secs
            self.sys_tags_['fps_in'].set_strict(int(fps_in), Quality.QUALITY_GOOD, None)
            self.sys_tags_['fps_out'].set_strict(int(fps_out), Quality.QUALITY_GOOD, None)

            self.notify_satelites_tag_changed(self.sys_tags_.values())

        self.nb_msg_in_ = 0
        self.nb_msg_out_ = 0
        self.fps_tstamp_ = t

    def notify_satelites_tag_changed(self, tag_or_tags: (Tag, list, tuple)) -> None:
        tags = (tag_or_tags,) if isinstance(tag_or_tags, Tag) else tag_or_tags

        for tag in tags:
            assert isinstance(tag, Tag), tag
            assert not tag.is_void(), tag

            for c in self.connections:
                c.notify_update(tag)


def main():
    try:
        # Args
        arg_parser = argparse.ArgumentParser()
        configure_my_args(arg_parser)
        configure_arg_parser_for_log(arg_parser)  # let logger add his arguments for later configure_logger() call
        env = arg_parser.parse_args()

        # Logging
        configure_logger(env)
        log = logging.getLogger('core')  # should log under our instance name

        #myself = 'volcano-core'
        #log.info('Volcano v%s', pkg_resources.get_distribution(myself).version)

        # Database
        db = Db(log)
        try:
            if env.demo:
                log.info('!! DEMO MODE !! Database is not loaded, creating demo structure')
                db.setup_demo_mode()
            else:
                db.upload_file(env.file)
                log.info('Loaded %s tags', db.nb_tags())
        except LoadException as ex:
            log.error(ex)
            return 1

        server = VolcanoServer(db, env, log)
        con_server = TTYControlPanel(server)
        stdio.StandardIO(con_server)

        log.info('Start listen: iface=%s port=%s max_con=%s', env.iface, env.port, env.max_con)
        try:
            reactor.listenTCP(env.port, server, interface=env.iface)    # pylint: disable=no-member
        except CannotListenError as ex:
            log.error(ex)
            return 1

        reactor.run()                                               # pylint: disable=no-member

        log.info('GOODBYE')

        return 0

    finally:
        logging.shutdown()


if __name__ == '__main__':
    sys.exit(main())
