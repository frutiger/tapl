# tapl.lrparser

class ParserError(Exception):
    def __init__(self, location, token):
        Exception.__init__(self,
                          'Unexpected token "{}" (at {}:{})'.format(
                                                              token,
                                                              location.line,
                                                              location.column))

class IncompleteParseError(Exception):
    def __init__(self, location):
        Exception.__init__(self,
                          'Unexpected end of input (at {}:{})'.format(
                                                              location.line,
                                                              location.column))

class LRParser:
    def __init__(self, acceptance, shifts, reductions, gotos):
        assert(set(shifts.keys()) & set(reductions.keys()) == set())
        self._acceptance = acceptance
        self._shifts     = shifts
        self._reductions = reductions
        self._gotos      = gotos
        self._stack      = [0]

    def _shift(self, state, location, token):
        self._stack.append((location, token))
        self._stack.append(state)

    def _reduce(self, Term):
        num_properties = len(Term._fields) - 1
        num_to_remove  = 2 * num_properties

        tokens      = self._stack[-1 * num_to_remove::2]
        self._stack = self._stack[:-1 * num_to_remove]

        location   = tokens[0][0]
        properties = [token[1] for token in tokens]
        fields     = [location] + properties
        term       = Term(*fields)
        self._stack.append((location, term))

        if (self._stack[-2]) not in self._gotos:
            raise RuntimeError('goto from state: {}'.format(self._stack[-2]))
        self._stack.append(self._gotos[(self._stack[-2])])

    def parse(self, tokens):
        location, token_type, token = next(tokens)
        while True:
            state = self._stack[-1]
            if (state, token_type) == self._acceptance:
                return self._stack[-2][1]
            elif (state, token_type) in self._shifts:
                self._shift(self._shifts[(state, token_type)], location, token)
                location, token_type, token = next(tokens)
            elif state in self._reductions:
                self._reduce(self._reductions[state])
            elif (state, token_type) in self._reductions:
                self._reduce(self._reductions[(state, token_type)])
            elif token_type == '$':
                raise IncompleteParseError(location)
            else:
                raise ParserError(token, location)

