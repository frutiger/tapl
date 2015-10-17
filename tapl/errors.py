# tapl.errors

class ParserError(RuntimeError):
    pass

class IncompleteParseError(ParserError):
    def __init__(self):
        ParserError.__init__(self, 'Unexpected end of input')

