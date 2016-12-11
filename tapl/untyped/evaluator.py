# tapl.untyped.evaluator

import copy

from . import terms

class NoRuleApplies(Exception):
    pass

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
    elif isinstance(term, terms.Application):
        return terms.Application(term.location,
                                 substitute(term.lhs,
                                            placeholder,
                                            replacement),
                                 substitute(term.rhs,
                                            placeholder,
                                            replacement))
    else:
        subterms = [term.location]
        for subterm in term.subterms:
            subterms.append(substitute(getattr(term, subterm),
                                       placeholder,
                                       replacement))
        return type(term)(*subterms)

def is_value(term):
    return isinstance(term, terms.Abstraction)

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

