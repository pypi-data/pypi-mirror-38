
import struct

# volcano
from volcano.general.stddef import ValueType
from volcano.general.bin import bytes_to_str
from volcano.general.vector import Vector
from volcano.general import stdsvcdef
from volcano.general.xml_reader import XmlReader, LoadException, load_xml_file_le
from volcano.general.modbus import *
from volcano.general import variant

# locals
from .mb_rules import RegRule


class SharedReg(stdsvcdef.IFindTagHandler, stdsvcdef.ITagUpdateHandler):
    def __init__(self, xml_node, device):
        p = XmlReader(xml_node)

        self.device_ = device
        self.name_ = p.get_str('name')

        # addr & format
        # (str_id, size_words, min|None, max|None, struct_format)
        self.fmt_tpl_ = p.get_dic('fmt', MB_FORMATS_DICT)
        a, fmt_size_words, *r = self.fmt_tpl_

        addr = p.get_int('addr', min_val=0, max_val=(0xffff - fmt_size_words + 1))

        self.vec_ = Vector(addr, size=fmt_size_words)
        # можно и float, но надо быть осторожным. int(big_int * 1.0) != big_int! потому что при умножении
        # на 1.0 значение преобразуется во float, где на больших порядках (как int64) точность ниже 1.
        # У меня ошибка составляла 11
        self.k_ = p.get_int('k', 1)
        self.value_ = None
        self.exists_ = False
        self.all_svc_ = None

    def exists(self):
        return self.exists_

    def sync(self, pipe):
        tag_full_name = self.device_.branch() + '.' + self.name_
        self.all_svc_ = pipe
        pipe.find_tag(tag_full_name, self)

    def on_find_tag_ok(self, tag_id: int, tag_name: str, vt: str, user_data):
        assert not self.exists_

        if ValueType(vt) in (ValueType.VT_INT, ValueType.VT_FLOAT, ValueType.VT_BOOL):
            self.exists_ = True
            self.all_svc_.subscribe(tag_name, send_tstamp=False, handler=self)
        else:
            self.device_.log().warning('Cant share tag {} [{}]. Only support int,float,bool'.format(tag_name, vt))

    def on_find_tag_err(self, tag_name_or_id: (int, str), user_data):
        assert not self.exists_

        log = self.device_.log()
        log.warn('Mapped tag not found: {}'.format(tag_name_or_id))

    def on_tag_updated(self, tag_name_or_id: (int, str), val_raw, quality: int, ts):
        assert self.exists_

        log = self.device_.log()
        log.debug('Got update {}={}[{}]'.format(tag_name_or_id, val_raw, quality))

        self.value_ = val_raw

    def map_mbex(self, data_bytes, req_vec):
        if self.exists_ and req_vec.intersects(self.vec_):
            if not req_vec.contains(self.vec_):
                raise MbException (MB_EXC_ILLEGAL_DATA_ADDRESS)

            #val: (int, float)
            rule = self.device_.default_reg_rule()
            if self.value_ is None:
                if rule.ns == 'zero':
                    val = 0
                else:
                    raise MbException(MB_EXC_ILLEGAL_DATA_VALUE, '')
            else:
                if isinstance(self.value_, bool):
                    val = 1 if self.value_ else 0
                else:
                    val = self.value_ if self.k_ == 1 else self.value_ * self.k_

            fmt_id, fmt_size_words, fmt_min_n, fmt_max_n, fmt_struct_format, val_type = self.fmt_tpl_
            if fmt_min_n is not None and val < fmt_min_n:
                val = fmt_min_n
            elif fmt_max_n is not None and val > fmt_max_n:
                val = fmt_max_n
            elif not isinstance(val, val_type):
                val = int(val) if val_type == int else float(val)

            struct.pack_into(fmt_struct_format, data_bytes, 2 * (self.vec_.s - req_vec.s), val)


class SharedBit(stdsvcdef.IFindTagHandler, stdsvcdef.ITagUpdateHandler):
    def __init__(self, xml_node, device):
        p = XmlReader(xml_node)

        self.device_ = device
        self.name_ = p.get_str('name')

        self.addr_ = p.get_int('addr', min_val=0, max_val=0xffff)
        self.invert_ = p.get_bool('invert', False)
        self.value_ = None
        self.exists_ = False
        self.all_svc_ = None

    def exists(self):
        return self.exists_

    def sync(self, pipe):
        tag_full_name = self.device_.branch() + '.' + self.name_
        pipe.find_tag(tag_full_name, self)
        self.all_svc_ = pipe

    def on_find_tag_ok(self, tag_id: int, tag_name: str, vt: str, user_data):
        assert not self.exists_

        if ValueType(vt) in (ValueType.VT_INT, ValueType.VT_FLOAT, ValueType.VT_BOOL):
            self.exists_ = True
            self.all_svc_.subscribe(tag_name, send_tstamp=False, handler=self)
        else:
            self.device_.log().warning(
                'Cant share tag {} [{}]. Only support int,float,bool'.format(tag_name, vt))

    def on_find_tag_err(self, tag_name_or_id, user_data):
        assert not self.exists_

        log = self.device_.log()
        log.warn('Mapped tag not found: {}'.format(tag_name_or_id))

    def on_tag_updated(self, tag_name_or_id: (int, str), val_raw, quality: int, ts):
        assert self.exists_

        log = self.device_.log()
        log.debug('Got update {}={}[{}]'.format(tag_name_or_id, val_raw, quality))

        self.value_ = val_raw

    def map_mbex(self, bits, req_vec):
        if self.exists_:
            if self.value_ is not None and req_vec.contains_value(self.addr_):
                bits[self.addr_ - req_vec.s] = bool(self.value_) != self.invert_  # this is xor


class Device:
    def __init__(self, xml_node, parent_log):
        p = XmlReader(xml_node)

        self.branch_ = p.get_str('branch')
        self.slave_nb_ = p.get_int('slaveNb', min_val=0, max_val=0xff)
        self.log_ = parent_log.getChild(str(self.slave_nb_))
        self.regs_ = []
        self.bits_ = []
        self.default_reg_rule_ = RegRule ()

        template_name = p.get_str('template')
        template_xml = load_xml_file_le(template_name)

        for tag_node in template_xml.getroot():
            if tag_node.tag == 'Tag':
                p2 = XmlReader(tag_node)
                is_coil = p2.get_bool('coil', False)
                if is_coil:
                    self.bits_.append(SharedBit(tag_node, self))
                else:
                    self.regs_.append(SharedReg(tag_node, self))
            else:
                raise LoadException('Unknown node name: {}'.format(tag_node.tag), tag_node)

    def log(self):
        return self.log_

    def branch(self):
        return self.branch_

    def slave_nb(self):
        return self.slave_nb_

    def default_reg_rule(self):
        return self.default_reg_rule_

    def sync(self, pipe):
        for x in self.regs_:
            x.sync(pipe)
        for x in self.bits_:
            x.sync(pipe)
        pipe.echo(self.on_sync_complete)

    def on_sync_complete(self):
        self.regs_ = tuple(filter(lambda x: x.exists(), self.regs_))
        self.bits_ = tuple(filter(lambda x: x.exists(), self.bits_))

    # can raise MbException
    def mb_read_words_mbex(self, addr, nb_words):
        data_bytes = bytearray(nb_words * 2)
        req_vec = Vector(addr, size=nb_words)
        for reg in self.regs_:
            reg.map_mbex(data_bytes, req_vec)

        self.log_.debug('Read words {}/{} => data[{}]'.format(addr, nb_words, bytes_to_str(data_bytes)))

        return data_bytes

    def mb_read_bits_mbex(self, addr, nb_bits):
        bits = [False] * nb_bits

        req_vec = Vector(addr, size=nb_bits)
        for bit in self.bits_:
            bit.map_mbex(bits, req_vec)

        self.log_.debug('Read bits {}/{} => data[{}]'.format(addr, nb_bits, bits))

        return bits
