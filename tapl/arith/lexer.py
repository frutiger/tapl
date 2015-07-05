# tapl.arith.lexer

from collections import namedtuple

Location = namedtuple('Location', ['line', 'column'])

def lex(source):
    location      = Location(1, 1)
    token_start   = None
    token         = None
    while True:
        char = source.read(1)
        if not char:
            break

        if char == ' ' or char == '\n':
            if token:
                yield (token_start, token)
                token = None
        else:
            if not token:
                token_start = Location(location.line, location.column)
                token       = char
            else:
                token += char

        if char == '\n':
            location = Location(location.line + 1, 1)
        else:
            location = Location(location.line, location.column + 1)

