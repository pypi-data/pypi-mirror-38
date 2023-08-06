#!/usr/bin/python3

import logging

from twisted.internet.protocol import Protocol, Factory

# locals
from volcano.general.bin import bytes_to_str
from volcano.general.modbus import *

from .mb_srv_protocol import *

g_env = None


class DropProtocol(Protocol):
    def connectionMade(self):
        self.transport.loseConnection()


class MbConnection(Protocol):
    def __init__(self, factory, devices):
        self.factory_ = factory
        self.devices_ = devices
        self.rcv_buf_ = bytearray()
        self.log_ = logging.getLogger(g_env.name)

    def log(self):
        return self.log_

    def process_mber_mbex(self, req: (ModbusRequestReadWords, ModbusRequestReadBits)):
        slave_nb = req.slave_nb
        slave = next((x for x in self.devices_ if x.slave_nb() == slave_nb), None)
        if not slave:
            raise MbException(MB_EXC_GATEWAY_PATHS_NA, 'Slave {} (0x{:x}) does not exist'.format(slave_nb, slave_nb))

        fn_nb = req.fn_nb
        if fn_nb == MB_FN_READ_OUT_BITS_1 or fn_nb == MB_FN_READ_IN_BITS_2:
            bits = slave.mb_read_bits_mbex(req.addr, req.nb_bits)  # can raise MbException/MbError
            return build_response_read_bits(req, bits)
        elif fn_nb == MB_FN_READ_OUT_WORDS_3 or fn_nb == MB_FN_READ_IN_WORDS_4:
            data_bytes = slave.mb_read_words_mbex(req.addr, req.nb_words)  # can raise MbException/MbError
            return build_response_read_words(req, data_bytes)
        else:
            raise MbException(MB_EXC_ILLEGAL_FN_CODE, 'Modbus function {} is not supported'.format(fn_nb))

    def dataReceived(self, data):
        self.log().debug('R< {}'.format(bytes_to_str(data)))
        self.rcv_buf_ += data
        try:
            while self.rcv_buf_:

                # MbError, None, {}
                req = parse_req_tcp(self.rcv_buf_)  # throws
                if req is None:  # not enough data
                    if len(self.rcv_buf_) >= MAX_FRAME_SIZE_BYTES:
                        raise MbError('Modbus rcv buffer overflow')
                    else:
                        return

                assert isinstance(req, (ModbusRequestReadWords, ModbusRequestReadBits)), req
                assert req.size_bytes > 0 and req.size_bytes <= len(self.rcv_buf_), req

                self.rcv_buf_ = self.rcv_buf_[req.size_bytes:]

                try:
                    res = self.process_mber_mbex(req)
                    self.log().debug('S> {}'.format(bytes_to_str(res)))
                    self.transport.write(res)
                except MbException as ex:
                    self.log().warning(ex)
                    res_ba = build_response_exception(req, ex.code)
                    self.transport.write(res_ba)
        except MbError as e:
            self.log().warning(e)
            self.transport.loseConnection()

    def connectionMade(self):
        self.log().debug('Modbus client connected')

    def connectionLost(self, reason):
        self.log().debug('Modbus client disconnected')
        self.factory_.on_connection_lost(self)


class MbFactory(Factory):
    def __init__(self, devices, env):
        super().__init__()

        global g_env
        g_env = env

        self.devices_ = devices
        self.connections_ = []
        self.log_ = logging.getLogger(env.name)

    def log(self): return self.log_

    def buildProtocol(self, addr):
        if len(self.connections_) >= g_env.max_con:
            self.log().warning('Max number of connections [{}] reached'.format(g_env.max_con))
            return DropProtocol()

        c = MbConnection(self, self.devices_)
        self.connections_.append(c)
        return c

    def on_connection_lost(self, con):
        self.connections_.remove(con)
