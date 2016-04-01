# tapl.lrparser

class ParserError(Exception):
    def __init__(self, location, message):
        Exception.__init__(self, '{} (at {}:{})'.format(message,
                                                        location.line,
                                                        location.column))

class IncompleteParseError(Exception):
    def __init__(self, location):
        message = 'Unexpected end of input'
        Exception.__init__(self, '{} (at {}:{})'.format(message,
                                                        location.line,
                                                        location.column))

class LRParser:
    def __init__(self, table, producers):
        assert(set(table['shifts']) & set(table['reductions']) == set())
        self._table     = table
        self._producers = producers
        self._stack     = [table['start']]

    def _shift(self, state, location, token):
        self._stack.append((location, token))
        self._stack.append(state)

    def _reduce(self, rule):
        producer = self._producers[rule]
        num_properties = producer.__code__.co_argcount - 1
        num_to_remove  = 2 * num_properties

        tokens      = self._stack[-1 * num_to_remove::2]
        self._stack = self._stack[:-1 * num_to_remove]

        location   = tokens[0][0]
        properties = [token[1] for token in tokens]
        fields     = [location] + properties
        term       = producer(*fields)
        self._stack.append((location, term))

        if (self._stack[-2], term.name) not in self._table['gotos']:
            raise RuntimeError('goto from state: {}'.format(self._stack[-2]))
        goto = self._table['gotos'][(self._stack[-2], term.name)]
        self._stack.append(goto)

    def parse(self, tokens):
        location, token_type, token = next(tokens)
        while True:
            state = self._stack[-1]
            if state == self._table['finish']:
                self._reduce(self._table['reductions'][state])
                return self._stack[-2][1]
            elif (state, token_type) in self._table['shifts']:
                self._shift(self._table['shifts'][(state, token_type)], location, token)
                if token_type != '$':
                    location, token_type, token = next(tokens)
            elif state in self._table['reductions']:
                self._reduce(self._table['reductions'][state])
            elif token_type == '$':
                raise IncompleteParseError(location)
            else:
                raise ParserError(location,
                                 'Unexpected token "{}"'.format(token))

