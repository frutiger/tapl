# tapl.evaluation

class NoRuleApplies(Exception):
    pass

def evaluate(term, evaluator):
    try:
        while True:
            term = evaluator.one_step(term)
    except NoRuleApplies:
        return term

