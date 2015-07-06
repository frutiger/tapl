# tapl.arith.parser

from .. import errors

from .  import terms

def error(message, location):
    raise errors.ParserError('{} (at {}:{})'.format(message,
                                                    location.line,
                                                    location.column))

def parse(tokens):
    def next_token(tokens):
        try:
            return next(tokens)
        except StopIteration:
            raise errors.IncompleteParseError('Unexpected end of input')

    def parse_if(tokens):
        def expect(tokens, value):
            location, token = next_token(tokens)
            if token != value:
                error('Expected "{}" not "{}"'.format(value, token), location)

        predicate   = parse(tokens)
        expect(tokens, 'then')
        true_value  = parse(tokens)
        expect(tokens, 'else')
        false_value = parse(tokens)
        return terms.If(location, predicate, true_value, false_value)

    location, token = next_token(tokens)
    if token == 'true':
        return terms.TrueValue(location)
    elif token == 'false':
        return terms.FalseValue(location)
    elif token == 'zero':
        return terms.ZeroValue(location)
    elif token == 'succ':
        return terms.Succ(location, parse(tokens))
    elif token == 'pred':
        return terms.Pred(location, parse(tokens))
    elif token == 'iszero':
        return terms.IsZero(location, parse(tokens))
    elif token == 'if':
        return parse_if(tokens)
    else:
        error('Unexpected token "{}"'.format(token), location)

