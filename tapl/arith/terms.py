# tapl.arith.terms

from ..terms      import Term
from ..bool.terms import *
from ..nat.terms  import *

class IsZero(Term):
    subterms = Term.subterms + ('argument',)

    def __init__(self, location, argument):
        Term.__init__(self, location)
        self.argument = argument

