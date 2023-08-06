#!/usr/bin/python3
import collections

# ns: zero/exception
# min: zero/min/exception
# max: zero/max/exception
RegRule = collections.namedtuple('RegRule', 'ns min max')

StdRegRule = RegRule('zero', 'min', 'max')
