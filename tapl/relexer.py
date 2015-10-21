# tapl.relexer

from collections import namedtuple

Location = namedtuple('Location', ['line', 'column'])

class UnknownToken(Exception):
    def __init__(self, location, token):
        Exception.__init__(self,
                          'Unknown token "{}" (at {}:{})'.format(
                                                              token,
                                                              location.line,
                                                              location.column))

def bump_location(char, location):
    if char == '\n':
        return Location(location.line + 1, 1)
    else:
        return Location(location.line, location.column + 1)

class ReLexer:
    def __init__(self, whitespace, token_types):
        self._whitespace  = whitespace
        self._token_types = token_types

    def _token_type(self, location, token):
        for token_type, regex in self._token_types.items():
            if regex.match(token):
                return token_type
        raise UnknownToken(location, token)

    def _valid_token(self, token):
        try:
            self._token_type(Location(0, 0), token)
            return True
        except UnknownToken:
            return False

    def lex(self, source):
        location     = Location(1, 0)
        token_start  = None
        token_so_far = ''

        while True:
            char     = source.read(1)
            location = bump_location(char, location)

            if char and char not in self._whitespace:
                if token_start is None:
                    assert(not token_so_far)
                    token_start = location

                if not self._valid_token(token_so_far + char) and \
                                               self._valid_token(token_so_far):
                    yield (token_start,
                           self._token_type(token_start, token_so_far),
                           token_so_far)
                    token_start  = location
                    token_so_far = char
                else:
                    token_so_far += char
            else:
                if token_start is not None:
                    assert(token_so_far)

                    if not self._valid_token(token_so_far):
                        raise UnknownToken(token_start, token_so_far)

                    yield (token_start,
                           self._token_type(token_start, token_so_far),
                           token_so_far)

                token_start  = None
                token_so_far = ''

                if not char:
                    yield (location, '$', None)
                    break

