# tapl.arith.parser

from .. import errors

from .  import terms

def error(message, location):
    raise errors.ParserError('{} (at {}:{})'.format(message,
                                                    location.line,
                                                    location.column))

def parse(tokens):
    def parse_if(tokens):
        def expect(tokens, expected_type):
            location, token_type, token = next(tokens)
            if token_type == '$':
                raise errors.IncompleteParseError()
            if token_type != expected_type:
                error('Expected "{}" not "{}"'.format(expected_type,
                                                      token_type),
                      location)

        predicate   = parse(tokens)
        expect(tokens, 'THEN')
        true_value  = parse(tokens)
        expect(tokens, 'ELSE')
        false_value = parse(tokens)
        return terms.If(location, predicate, true_value, false_value)

    location, token_type, token = next(tokens)
    if token_type == 'TRUE':
        return terms.TrueValue(location)
    elif token_type == 'FALSE':
        return terms.FalseValue(location)
    elif token_type == 'ZERO':
        return terms.ZeroValue(location)
    elif token_type == 'SUCC':
        return terms.Succ(location, parse(tokens))
    elif token_type == 'PRED':
        return terms.Pred(location, parse(tokens))
    elif token_type == 'ISZERO':
        return terms.IsZero(location, parse(tokens))
    elif token_type == 'IF':
        return parse_if(tokens)
    elif token_type == '$':
        raise errors.IncompleteParseError()
    else:
        error('Unexpected token "{}"'.format(token), location)

