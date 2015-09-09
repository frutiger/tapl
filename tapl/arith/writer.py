# tapl.arith.writer

from . import terms

def format_term(term):
    if isinstance(term, terms.TrueValue):
        return 'true'
    elif isinstance(term, terms.FalseValue):
        return 'false'
    elif isinstance(term, terms.ZeroValue):
        return 'zero'
    elif isinstance(term, terms.Succ):
        return 'succ {}'.format(format_term(term.argument))
    elif isinstance(term, terms.Pred):
        return 'pred {}'.format(format_term(term.argument))
    elif isinstance(term, terms.IsZero):
        return 'iszero {}'.format(format_term(term.argument))
    elif isinstance(term, terms.If):
        return 'if {} then {} else {}'.format(format_term(term.predicate),
                                              format_term(term.true_value),
                                              format_term(term.false_value))
    else:
        raise RuntimeError('Unknown term: {}'.format(term))

def write(file, term):
    file.write(format_term(term) + '\n')

