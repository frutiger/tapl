# tapl.arith.terms

from collections import namedtuple

ZeroValue  = namedtuple('ZeroValue',  ['location'])
TrueValue  = namedtuple('TrueValue',  ['location'])
FalseValue = namedtuple('FalseValue', ['location'])
Succ       = namedtuple('Succ',       ['location', 'argument'])
Pred       = namedtuple('Pred',       ['location', 'argument'])
IsZero     = namedtuple('IsZero',     ['location', 'argument'])
If         = namedtuple('If',         ['location',
                                       'predicate',
                                       'true_value',
                                       'false_value'])

Succ.subterms   = { 'argument' }
Pred.subterms   = { 'argument' }
IsZero.subterms = { 'argument' }
If.subterms     = { 'predicate', 'true_value', 'false_value' }

