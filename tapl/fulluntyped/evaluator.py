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
    else:
        subterms = [term.location]
        for subterm in term.subterms:
            subterms.append(substitute(getattr(term, subterm),
                                       placeholder,
                                       replacement))
        return type(term)(*subterms)

def is_numeric(term):
    return any((isinstance(term, terms.ZeroValue),
                isinstance(term, terms.Succ) and is_numeric(term.argument)))

def is_value(term):
    return any(map(lambda Type: isinstance(term, Type), (terms.Abstraction,
                                                         terms.TrueValue,
                                                         terms.FalseValue)) + \
               [is_numeric(term)])

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
    elif isinstance(term, terms.If):
        if isinstance(term.predicate, terms.TrueValue):
            return term.true_value
        elif isinstance(term.predicate, terms.FalseValue):
            return term.false_value
        else:
            return terms.If(term.location,
                            evaluate_one_step(term.predicate, context),
                            term.true_value,
                            term.false_value)
    elif isinstance(term, terms.Succ):
        return terms.Succ(term.location,
                          evaluate_one_step(term.argument, context))
    elif isinstance(term, terms.Pred):
        if isinstance(term.argument, terms.ZeroValue):
            return terms.ZeroValue(None)
        elif isinstance(term.argument, terms.Succ) and \
                                            is_numeric(term.argument.argument):
            return term.argument.argument
        else:
            return terms.Pred(term.location,
                              evaluate_one_step(term.argument, context))
    elif isinstance(term, terms.IsZero):
        if isinstance(term.argument, terms.ZeroValue):
            return terms.TrueValue(None)
        elif isinstance(term.argument, terms.Succ) and \
                                            is_numeric(term.argument.argument):
            return terms.FalseValue(None)
        else:
            return terms.IsZero(term.location,
                                evaluate_one_step(term.argument, context))
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

