# tapl.nat.terms
# encoding: UTF-8

class Term(object):
    fields   = ('location',)
    subterms = tuple()

    def __init__(self, location):
        self.location = location

class ZeroValue(Term):
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

