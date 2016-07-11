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

def evaluate_one_step(term):
    if isinstance(term, terms.Succ):
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
    elif isinstance(term, terms.ZeroValue):
        raise NoRuleApplies()
    else:
        raise RuntimeError('Unknown term: {}'.format(term))

def evaluate(term):
    try:
        next_step = evaluate_one_step(term)
        return evaluate(next_step)
    except NoRuleApplies:
        return term

