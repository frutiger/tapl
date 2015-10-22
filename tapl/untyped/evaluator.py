# tapl.untyped.evaluator

import copy

from . import terms

class NoRuleApplies(Exception):
    pass

def shift(term, distance, cutoff=0):
    if isinstance(term, terms.Variable):
        if term.binder >= cutoff:
            binder = term.binder + distance
        else:
            binder = term.binder
        return terms.Variable(term.location, binder)
    elif isinstance(term, terms.Abstraction):
        return terms.Abstraction(term.location,
                                 term.hint,
                                 shift(term.body, distance, cutoff + 1))
    elif isinstance(term, terms.Application):
        return terms.Application(term.location,
                                 shift(term.lhs, distance, cutoff),
                                 shift(term.rhs, distance, cutoff))
    else:
        raise RuntimeError('Unknown term: {}'.format(term))

def substitute(term, placeholder, replacement):
    if isinstance(term, terms.Variable):
        if term.binder == placeholder:
            return replacement
        else:
            return term
    elif isinstance(term, terms.Abstraction):
        return terms.Abstraction(term.location,
                                 term.hint,
                                 substitute(term.body,
                                            placeholder + 1,
                                            shift(replacement, 1)))
    elif isinstance(term, terms.Application):
        return terms.Application(term.location,
                                 substitute(term.lhs,
                                            placeholder,
                                            replacement),
                                 substitute(term.rhs,
                                            placeholder,
                                            replacement))
    else:
        raise RuntimeError('Unknown term: {}'.format(term))

def is_value(term):
    if isinstance(term, terms.Abstraction):
        return True
    else:
        return False

def evaluate_one_step(term, context):
    if isinstance(term, terms.Application):
        if isinstance(term.lhs, terms.Abstraction) and is_value(term.rhs):
            result = copy.deepcopy(term.rhs)
            result = shift(result, 1)
            result = substitute(term.lhs.body, 0, result)
            result = shift(result, -1)
            return result
        elif is_value(term.lhs):
            return terms.Application(term.location,
                                     term.lhs,
                                     evaluate_one_step(term.rhs, context))
        else:
            return terms.Application(term.location,
                                     evaluate_one_step(term.lhs, context),
                                     term.rhs)
    else:
        raise NoRuleApplies()

def evaluate(term, context=None):
    if context == None:
        context = []
    try:
        next_step = evaluate_one_step(term, context)
        return evaluate(next_step, context)
    except NoRuleApplies:
        return term

