# tapl.arith.evaluator

from ..bool import evaluator as bool
from ..nat  import evaluator as nat
from .      import terms

class Evaluator(object):
    def __init__(self, sub=None):
        self._sub  = sub if sub is not None else self
        self._bool = bool.Evaluator(self)
        self._nat  = nat.Evaluator(self)

    def one_step(self, term):
        result = self._bool.one_step(term)
        if result:
            return result
        result = self._nat.one_step(term)
        if result:
            return result
        if isinstance(term, terms.IsZero):
            if isinstance(term.argument, terms.ZeroValue):
                return terms.TrueValue(None)
            if isinstance(term.argument, terms.Succ) and \
                                        nat.is_numeric(term.argument.argument):
                return terms.FalseValue(None)
            return terms.IsZero(term.location,
                                self._sub.one_step(term.argument))

