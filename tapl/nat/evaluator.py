# tapl.arith.evaluator

from ..evaluation import NoRuleApplies
from .            import terms

def is_numeric(term):
    return any((isinstance(term, terms.ZeroValue),
                isinstance(term, terms.Succ) and is_numeric(term.argument)))

class Evaluator(object):
    def __init__(self, sub=None):
        self._sub = sub if sub is not None else self

    def one_step(self, term):
        if isinstance(term, terms.Succ):
            return terms.Succ(term.location, self._sub.one_step(term.argument))
        if isinstance(term, terms.Pred):
            if isinstance(term.argument, terms.ZeroValue):
                return terms.ZeroValue(None)
            if isinstance(term.argument, terms.Succ) and \
                                            is_numeric(term.argument.argument):
                return term.argument.argument
            return terms.Pred(term.location, self._sub.one_step(term.argument))
        if isinstance(term, terms.ZeroValue):
            raise NoRuleApplies()

