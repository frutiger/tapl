# tapl.arith.terms

from collections import namedtuple

from . import concrete

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

def from_concrete(term):
    if isinstance(term, concrete.ZeroValue):
        return ZeroValue(term.location)
    elif isinstance(term, concrete.TrueValue):
        return TrueValue(term.location)
    elif isinstance(term, concrete.FalseValue):
        return FalseValue(term.location)
    elif isinstance(term, concrete.Succ):
        return Succ(term.location, from_concrete(term.argument))
    elif isinstance(term, concrete.Pred):
        return Pred(term.location, from_concrete(term.argument))
    elif isinstance(term, concrete.IsZero):
        return IsZero(term.location, from_concrete(term.argument))
    elif isinstance(term, concrete.If):
        return If(term.location,
                  from_concrete(term.predicate),
                  from_concrete(term.true_value),
                  from_concrete(term.false_value))

