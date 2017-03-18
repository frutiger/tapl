# tapl.nat.terms

from ..terms import Term

class ZeroValue(Term):
    def __init__(self, location):
        Term.__init__(self, location)

class Succ(Term):
    subterms = Term.subterms + ('argument',)

    def __init__(self, location, argument):
        Term.__init__(self, location)
        self.argument = argument

class Pred(Term):
    subterms = Term.subterms + ('argument',)

    def __init__(self, location, argument):
        Term.__init__(self, location)
        self.argument = argument

