# tapl.bool.terms
# coding: UTF-8

class Term(object):
    fields   = ('location',)
    subterms = tuple()

    def __init__(self, location):
        self.location = location

class TrueValue(Term):
    def __init__(self, location):
        Term.__init__(self, location)

class FalseValue(Term):
    def __init__(self, location):
        Term.__init__(self, location)

class If(Term):
    fields   = Term.fields   + ('predicate', 'true_value', 'false_value')
    subterms = Term.subterms + ('predicate', 'true_value', 'false_value')

    def __init__(self, location, predicate, true_value, false_value):
        Term.__init__(self, location)
        self.predicate   = predicate
        self.true_value  = true_value
        self.false_value = false_value
