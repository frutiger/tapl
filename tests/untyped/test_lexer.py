# tests.untyped.test_lexer

from unittest import TestCase
from io       import StringIO

from tapl.relexer           import Location, ReLexer
from tapl.untyped.toolchain import Toolchain

def l(line, column):
    return Location(line, column)

lexer = ReLexer(Toolchain.tokens)
def lex(text):
    return lexer.lex(StringIO(text))

class LastToken(TestCase):
    def test(self):
        ts = list(lex(u'a'))
        assert(2 == len(ts))

        t = ts[0]
        assert(3       == len(t))
        assert(l(1, 1) == t[0])
        assert(u'ID'   == t[1])
        assert(u'a'    == t[2])

        t = ts[1]
        assert(u'$' == t[1])

class ParenParen(TestCase):
    def test(self):
        ts = list(lex(u'(('))
        assert(3 == len(ts))

        t = ts[0]
        assert(3         == len(t))
        assert(l(1, 1)   == t[0])
        assert(u'LPAREN' == t[1])

        t = ts[1]
        assert(3         == len(t))
        assert(l(1, 2)   == t[0])
        assert(u'LPAREN' == t[1])

        t = ts[2]
        assert(u'$' == t[1])

class ParenId(TestCase):
    def test(self):
        ts = list(lex(u'(foobar'))
        assert(3 == len(ts))

        t = ts[0]
        assert(3         == len(t))
        assert(l(1, 1)   == t[0])
        assert(u'LPAREN' == t[1])

        t = ts[1]
        assert(3         == len(t))
        assert(l(1, 2)   == t[0])
        assert(u'ID'     == t[1])
        assert(u'foobar' == t[2])

        t = ts[2]
        assert(u'$' == t[1])

class Identity(TestCase):
    def test(self):
        ts = list(lex(u'\\x x'))
        assert(4 == len(ts))

        t = ts[0]
        assert(3         == len(t))
        assert(l(1, 1)   == t[0])
        assert(u'LAMBDA' == t[1])

        t = ts[1]
        assert(3       == len(t))
        assert(l(1, 2) == t[0])
        assert(u'ID'   == t[1])
        assert(u'x'    == t[2])

        t = ts[2]
        assert(3       == len(t))
        assert(l(1, 4) == t[0])
        assert(u'ID'   == t[1])
        assert(u'x'    == t[2])

        t = ts[3]
        assert(u'$' == t[1])

