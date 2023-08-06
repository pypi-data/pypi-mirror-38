#!/usr/bin/python3

from volcano.general.xml_reader import XmlReader


class RegRule:
    def __init__(self, node=None):
        if node is None:
            self.ns = 'zero'
            self.min = 'min'
            self.max = 'max'
        else:
            p = XmlReader(node)
            self.ns = p.get_str('ns', default='zero', allowed=('zero', 'exception'))
            self.min = p.get_str('min', default='min', allowed=('zero', 'min', 'exception'))
            self.max = p.get_str('max', default='max', allowed=('zero', 'max', 'exception'))

