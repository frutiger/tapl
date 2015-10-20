# tapl.errors

class ParserError(Exception):
    pass

class IncompleteParseError(ParserError):
    def __init__(self):
        ParserError.__init__(self, 'Unexpected end of input')

