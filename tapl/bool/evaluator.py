# tapl.bool.evaluator

from . import terms

class NoRuleApplies(Exception):
    pass

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
    elif isinstance(term, terms.TrueValue):
        raise NoRuleApplies()
    elif isinstance(term, terms.FalseValue):
        raise NoRuleApplies()
    else:
        raise RuntimeError('Unknown term: {}'.format(term))

def evaluate(term):
    try:
        next_step = evaluate_one_step(term)
        return evaluate(next_step)
    except NoRuleApplies:
        return term

