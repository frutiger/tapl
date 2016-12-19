# tapl.untyped.evaluator

import copy

from ..evaluation import NoRuleApplies
from .            import terms

def shift(term, distance, cutoff=0):
    if isinstance(term, terms.Variable):
        if term.id >= cutoff:
            id = term.id + distance
        else:
            id = term.id
        return terms.Variable(term.location, id)
    elif isinstance(term, terms.Abstraction):
        return terms.Abstraction(term.location,
                                 term.id,
                                 shift(term.body, distance, cutoff + 1))
    else:
        subterms = [term.location]
        for subterm in term.subterms:
            subterms.append(shift(getattr(term, subterm), distance, cutoff))
        return type(term)(*subterms)

def substitute(term, placeholder, replacement):
    if isinstance(term, terms.Variable):
        if term.id == placeholder:
            return replacement
        else:
            return term
    elif isinstance(term, terms.Abstraction):
        return terms.Abstraction(term.location,
                                 term.id,
                                 substitute(term.body,
                                            placeholder + 1,
                                            shift(replacement, 1)))
    else:
        subterms = [term.location]
        for subterm in term.subterms:
            subterms.append(substitute(getattr(term, subterm),
                                       placeholder,
                                       replacement))
        return type(term)(*subterms)

def is_value(term):
    return isinstance(term, terms.Abstraction)

class Evaluator(object):
    def __init__(self, sub=None, is_value=is_value):
        self._sub      = sub if sub is not None else self
        self._is_value = is_value

    def one_step(self, term):
        if isinstance(term, terms.Application):
            if isinstance(term.lhs, terms.Abstraction) and \
                                                      self._is_value(term.rhs):
                result = copy.deepcopy(term.rhs)
                result = shift(result, 1)
                result = substitute(term.lhs.body, 0, result)
                result = shift(result, -1)
                return result
            if self._is_value(term.lhs):
                return terms.Application(term.location,
                                         term.lhs,
                                         self._sub.one_step(term.rhs))
            return terms.Application(term.location,
                                     self._sub.one_step(term.lhs),
                                     term.rhs)
        if isinstance(term, terms.Abstraction):
            raise NoRuleApplies()
        if isinstance(term, terms.Variable):
            raise NoRuleApplies()

