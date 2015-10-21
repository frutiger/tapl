# tests.untyped.test_lexer

from unittest import TestCase
from io       import StringIO

from tapl.relexer               import Location, ReLexer
from tapl.untyped.token_regexes import WHITESPACE, TOKEN_TYPES

def l(line, column):
    return Location(line, column)

lexer = ReLexer(WHITESPACE, TOKEN_TYPES)
def lex(text):
    return lexer.lex(StringIO(text))

class LastToken(TestCase):
    def test(self):
        ts = list(lex('a'))
        assert(2 == len(ts))

        t = ts[0]
        assert(3       == len(t))
        assert(l(1, 1) == t[0])
        assert('ID'    == t[1])
        assert('a'     == t[2])

        t = ts[1]
        assert('$' == t[1])

class ParenParen(TestCase):
    def test(self):
        ts = list(lex('(('))
        assert(3 == len(ts))

        t = ts[0]
        assert(3        == len(t))
        assert(l(1, 1)  == t[0])
        assert('LPAREN' == t[1])

        t = ts[1]
        assert(3        == len(t))
        assert(l(1, 2)  == t[0])
        assert('LPAREN' == t[1])

        t = ts[2]
        assert('$' == t[1])

class ParenId(TestCase):
    def test(self):
        ts = list(lex('(foobar'))
        assert(3 == len(ts))

        t = ts[0]
        assert(3        == len(t))
        assert(l(1, 1)  == t[0])
        assert('LPAREN' == t[1])

        t = ts[1]
        assert(3        == len(t))
        assert(l(1, 2)  == t[0])
        assert('ID'     == t[1])
        assert('foobar' == t[2])

        t = ts[2]
        assert('$' == t[1])

class Identity(TestCase):
    def test(self):
        ts = list(lex('\\x x'))
        assert(4 == len(ts))

        t = ts[0]
        assert(3        == len(t))
        assert(l(1, 1)  == t[0])
        assert('LAMBDA' == t[1])

        t = ts[1]
        assert(3       == len(t))
        assert(l(1, 2) == t[0])
        assert('ID'    == t[1])
        assert('x'     == t[2])

        t = ts[2]
        assert(3       == len(t))
        assert(l(1, 4) == t[0])
        assert('ID'    == t[1])
        assert('x'     == t[2])

        t = ts[3]
        assert('$' == t[1])

