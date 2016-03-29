# tapl.arith.terms

from . import concrete

class Term(object):
    fields   = ('location',)
    subterms = tuple()

    def __init__(self, location):
        self.location = location

class ZeroValue(Term):
    def __init__(self, location):
        Term.__init__(self, location)

class TrueValue(Term):
    def __init__(self, location):
        Term.__init__(self, location)

class FalseValue(Term):
    def __init__(self, location):
        Term.__init__(self, location)

class Succ(Term):
    fields   = Term.fields   + ('argument',)
    subterms = Term.subterms + ('argument',)

    def __init__(self, location, argument):
        Term.__init__(self, location)
        self.argument = argument

class Pred(Term):
    fields   = Term.fields   + ('argument',)
    subterms = Term.subterms + ('argument',)

    def __init__(self, location, argument):
        Term.__init__(self, location)
        self.argument = argument

class IsZero(Term):
    fields   = Term.fields   + ('argument',)
    subterms = Term.subterms + ('argument',)

    def __init__(self, location, argument):
        Term.__init__(self, location)
        self.argument = argument

class If(Term):
    fields   = Term.fields   + ('predicate', 'true_value', 'false_value')
    subterms = Term.subterms + ('predicate', 'true_value', 'false_value')

    def __init__(self, location, predicate, true_value, false_value):
        Term.__init__(self, location)
        self.predicate   = predicate
        self.true_value  = true_value
        self.false_value = false_value

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

