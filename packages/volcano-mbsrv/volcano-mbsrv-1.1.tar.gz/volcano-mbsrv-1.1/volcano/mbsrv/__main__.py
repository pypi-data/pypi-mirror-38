#!/usr/bin/python3

import argparse
import logging

from twisted.internet import reactor, protocol
from twisted.internet.error import CannotListenError

# volcano
from volcano.general.log import configure_arg_parser_for_log, configure_logger
from volcano.general.stddef import VOLCANO_DEFAULT_TCP_PORT
from volcano.general.xml_reader import *
from volcano.general.stdsvc import SingleThreadAllService

from volcano.twistedclient.twisted_factory import VolcanoTwistedFactory
from volcano.twistedclient.twisted_client_st import VolcanoTwistedClientST

from . import device
from .mb_server import MbFactory


def configure_my_args(parser):
    parser.add_argument('--core_host', help='Volcano core host', default='localhost')
    parser.add_argument('--core_port', help='Volcano core port', default=VOLCANO_DEFAULT_TCP_PORT, type=int)
    parser.add_argument('-n', '--name', help='Instance name', default='mbsrv')
    parser.add_argument('-f', '--file', help='Config file', default='mbsrv.xml')
    parser.add_argument('-i', '--iface', help='Listen interface', default='')
    parser.add_argument('-p', '--port', help='ModbusTCP port', type=int, default=-1)
    parser.add_argument('--max_con', help='Max number of connections', type=int, default=2)


def load():
    file = load_xml_file_le(g_env.file)

    p = XmlReader(file.getroot())

    # Interface
    xml_iface = p.get_str('iface', '')
    if xml_iface == '' and g_env.iface == '':
        g_env.iface = '0.0.0.0'
        g_log.info('Interface set to default value: {}'.format(g_env.iface))
    elif xml_iface and g_env.iface:
        g_log.info('Interface set to {} because command line has priority over xml (in xml interface is {})'.format(g_env.iface, xml_iface))
    elif xml_iface:
        assert g_env.iface == '', g_env.iface
        g_env.iface = xml_iface

        # Port
    xml_port = p.get_int('port', -1, min_val=1, max_val=0xffff)
    if xml_port == -1 and g_env.port == -1:
        g_env.port = 502
        g_log.info('Port set to default value: {}'.format(g_env.port))
    elif xml_port != -1 and g_env.port != -1:
        g_log.info('Port set to {} because command line has priority over xml (in xml port is {})'.format(g_env.port, xml_port))
    elif xml_port != -1:
        assert g_env.port == -1, g_env.port
        g_env.port = xml_port

    for node in file.getroot():
        if node.tag == 'Device':
            dev = device.Device(node, g_log)
            g_devices.append(dev)
        else:
            raise LoadException('Unknown node name: "{}"'.format(node.tag))

    if len(g_devices) == 0:
        raise LoadException('No devices configured')


class MyLavaClient(VolcanoTwistedClientST):
    def __init__(self):
        super().__init__(logging.getLogger(g_env.name))
        self.all_svc_ = None

    def connectionMade(self):
        super().connectionMade()

        self.all_svc_ = SingleThreadAllService(self)
        self.all_svc_.salute(g_env.name)

        for dev in g_devices:
            dev.sync(self.all_svc_)
        self.all_svc_.echo(self.sync_complete)

    def sync_complete(self):
        self.log.info('Start listen: iface=%s port=%s', g_env.iface, g_env.port)
        try:
            reactor.listenTCP(g_env.port, MbFactory(g_devices, g_env), interface=g_env.iface)
        except CannotListenError as ex:
            self.log.error(ex)
            reactor.stop()

    def on_msg_rcvd_no_exc(self, msg: dict) -> None:   # Exceptions not expected
        self.all_svc_.push_single_message(msg)


class MyLavaFactory(VolcanoTwistedFactory):
    protocol = MyLavaClient


if __name__ == '__main__':
    # Args
    arg_parser = argparse.ArgumentParser()
    configure_my_args(arg_parser)
    configure_arg_parser_for_log(arg_parser)  # let logger add his arguments for later configure_logger() call
    g_env = arg_parser.parse_args()

    # Logging
    configure_logger(g_env)
    g_log = logging.getLogger(g_env.name)

    g_devices = []

    try:
        load()

        volcano_factory = MyLavaFactory()
        volcano_factory.log = g_log

        g_log.info('Connect to core at {}:{}'.format(g_env.core_host, g_env.core_port))
        reactor.connectTCP(g_env.core_host, g_env.core_port, volcano_factory)
        reactor.run()
    except (LoadException, Warning) as e:
        g_log.error(e)

    print("\n\n GOOBYE \n\n")
