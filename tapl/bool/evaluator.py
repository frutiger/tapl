# tapl.bool.evaluator

from ..evaluation import NoRuleApplies
from .            import terms

class Evaluator(object):
    def __init__(self, sub=None):
        self._sub = sub if sub is not None else self

    def one_step(self, term):
        if isinstance(term, terms.If):
            if isinstance(term.predicate, terms.TrueValue):
                return term.true_value
            if isinstance(term.predicate, terms.FalseValue):
                return term.false_value
            return terms.If(term.location,
                            self._sub.one_step(term.predicate),
                            term.true_value,
                            term.false_value)
        if isinstance(term, terms.TrueValue):
            raise NoRuleApplies()
        if isinstance(term, terms.FalseValue):
            raise NoRuleApplies()

