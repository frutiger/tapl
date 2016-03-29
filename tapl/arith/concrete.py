# tapl.arith.concrete

from collections import namedtuple

ZeroValue  = namedtuple('ZeroValue',  ['location', 'value'])
TrueValue  = namedtuple('TrueValue',  ['location', 'value'])
FalseValue = namedtuple('FalseValue', ['location', 'value'])
Succ       = namedtuple('Succ',       ['location', 'dummy', 'argument'])
Pred       = namedtuple('Pred',       ['location', 'dummy', 'argument'])
IsZero     = namedtuple('IsZero',     ['location', 'dummy', 'argument'])
If         = namedtuple('If',         ['location',
                                       'dummy_if',
                                       'predicate',
                                       'dummy_then',
                                       'true_value',
                                       'dummy_else',
                                       'false_value'])
Goal       = namedtuple('Goal',       ['location', 'value', 'dummy'])

