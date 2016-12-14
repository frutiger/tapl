# tapl.bool.terms
# coding: UTF-8

from ..terms import Term

class TrueValue(Term):
    def __init__(self, location):
        Term.__init__(self, location)

class FalseValue(Term):
    def __init__(self, location):
        Term.__init__(self, location)

class If(Term):
    subterms = Term.subterms + ('predicate', 'true_value', 'false_value')

    def __init__(self, location, predicate, true_value, false_value):
        Term.__init__(self, location)
        self.predicate   = predicate
        self.true_value  = true_value
        self.false_value = false_value

