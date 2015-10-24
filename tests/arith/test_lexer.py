# tests.arith.test_lexer

from unittest import TestCase
from io       import StringIO

from tapl.relexer             import Location, ReLexer
from tapl.arith.token_regexes import WHITESPACE, TOKEN_TYPES

def l(line, column):
    return Location(line, column)

lexer = ReLexer(WHITESPACE, TOKEN_TYPES)
def lex(text):
    return lexer.lex(StringIO(text))

class If(TestCase):
    def test(self):
        ts = list(lex(u'if'))
        assert(2 == len(ts))

        t = ts[0]
        assert(3       == len(t))
        assert(l(1, 1) == t[0])
        assert(u'IF'   == t[1])
        assert(u'if'   == t[2])

        t = ts[1]
        assert(u'$' == t[1])

