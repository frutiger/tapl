# tapl.tyarith.typing

from tapl.arith import terms

from ..errors import TypeError

def typeof(term):
    if isinstance(term, terms.If):
        predicate_type = typeof(term.predicate)
        if predicate_type != u'Bool':
            raise TypeError(term.predicate.location, 'predicate not a Bool')
        true_value_type  = typeof(term.true_value)
        false_value_type = typeof(term.false_value)
        if true_value_type != false_value_type:
            raise TypeError(
                        term.location,
                        'Branches not of equal type: ' +
                        '{} at {}:{} and '
                        '{} at {}:{}'.format(true_value_type,
                                             term.true_value.location.line,
                                             term.true_value.location.column,
                                             false_value_type,
                                             term.false_value.location.line,
                                             term.false_value.location.column))
        return true_value_type
    if isinstance(term, terms.Succ) or isinstance(term, terms.Pred):
        argument_type = typeof(term.argument)
        if argument_type != u'Nat':
            raise TypeError(term.argument.location, 'Argument not a Nat')
        return u'Nat'
    if isinstance(term, terms.IsZero):
        argument_type = typeof(term.argument)
        if argument_type != u'Nat':
            raise TypeError(term.argument.location, 'Argument not a Nat')
        return u'Bool'
    if isinstance(term, terms.ZeroValue):
        return u'Nat'
    if isinstance(term, terms.TrueValue) or isinstance(term, terms.FalseValue):
        return u'Bool'
    raise RuntimeError('Unknown term: ' + term)

