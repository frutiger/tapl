# tapl.fulluntyped.evaluator

import copy

from ..evaluation import NoRuleApplies
from ..untyped    import evaluator as untyped
from ..arith      import evaluator as arith
from ..nat        import evaluator as nat
from .            import terms

def is_value(term):
    return any((untyped.is_value(term),
                nat.is_numeric(term),
                isinstance(term, terms.TrueValue),
                isinstance(term, terms.FalseValue)))

class Evaluator(object):
    def __init__(self, sub=None):
        self._sub     = sub if sub is not None else self
        self._arith   = arith.Evaluator(self)
        self._untyped = untyped.Evaluator(self, is_value)

    def one_step(self, term):
        result = self._arith.one_step(term)
        if result:
            return result

        result = self._untyped.one_step(term)
        if result:
            return result

