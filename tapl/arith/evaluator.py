# tapl.arith.evaluator

from . import terms

class NoRuleApplies(Exception):
    pass

def is_numeric(term):
    if isinstance(term, terms.ZeroValue):
        return True
    elif isinstance(term, terms.Succ) and is_numeric(term.argument):
        return True
    else:
        return False

def is_value(term):
    if isinstance(term, terms.TrueValue):
        return True
    elif isinstance(term, terms.FalseValue):
        return True
    elif is_numeric(term):
        return True
    else:
        return False

def evaluate_one_step(term):
    if isinstance(term, terms.If):
        if isinstance(term.predicate, terms.TrueValue):
            return term.true_value
        elif isinstance(term.predicate, terms.FalseValue):
            return term.false_value
        else:
            return terms.If(term.location,
                            evaluate_one_step(term.predicate),
                            term.true_value,
                            term.false_value)
    elif isinstance(term, terms.Succ):
        return terms.Succ(term.location,
                          evaluate_one_step(term.argument))
    elif isinstance(term, terms.Pred):
        if isinstance(term.argument, terms.ZeroValue):
            return terms.ZeroValue(None)
        elif isinstance(term.argument, terms.Succ) and \
                                            is_numeric(term.argument.argument):
            return term.argument.argument
        else:
            return terms.Pred(term.location,
                              evaluate_one_step(term.argument))
    elif isinstance(term, terms.IsZero):
        if isinstance(term.argument, terms.ZeroValue):
            return terms.TrueValue(None)
        elif isinstance(term.argument, terms.Succ) and \
                                            is_numeric(term.argument.argument):
            return terms.FalseValue(None)
        else:
            return terms.IsZero(term.location,
                                evaluate_one_step(term.argument))
    else:
        raise NoRuleApplies()

def evaluate(term):
    try:
        next_step = evaluate_one_step(term)
        return evaluate(next_step)
    except NoRuleApplies:
        return term

