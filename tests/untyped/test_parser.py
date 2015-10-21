# tests.untyped.test_parser

from unittest import TestCase
from io       import StringIO

from tapl.relexer               import Location, ReLexer
from tapl.untyped.token_regexes import WHITESPACE, TOKEN_TYPES

from tapl.lrparser         import IncompleteParseError, LRParser
from tapl.untyped.lr_table import ACCEPTANCE, SHIFTS, REDUCTIONS, GOTOS
from tapl.untyped.concrete import Abstraction as Abs, \
                                  Application as App, \
                                  Variable    as Var, \
                                  Parens      as Par

lexer = ReLexer(WHITESPACE, TOKEN_TYPES)
def lex(source):
    return lexer.lex(source)

def p(text):
    parser = LRParser(ACCEPTANCE, SHIFTS, REDUCTIONS, GOTOS)
    return parser.parse(lex(StringIO(text)))

class Variable(TestCase):
    def test(self):
        t = p('x')

        assert(isinstance(t, Var))
        assert('x' == t.id)

class Identity(TestCase):
    def test(self):
        t = p('\\x x')

        assert(isinstance(t, Abs))
        assert('x' == t.id)
        t = t.body

        assert(isinstance(t, Var))
        assert('x'  == t.id)

class SelfApplication(TestCase):
    def test(self):
        t = p('\\x x x')

        assert(isinstance(t, Abs))
        assert('x' == t.id)
        t = t.body

        assert(isinstance(t, App))
        tr = t.rhs
        tl = t.lhs

        assert(isinstance(tr, Var))
        assert('x' == tr.id)

        assert(isinstance(tl, Var))
        assert('x' == tl.id)

class TripleApplication(TestCase):
    def test(self):
        t = p('\\x x x x')

        assert(isinstance(t, Abs))
        assert('x' == t.id)
        t = t.body

        assert(isinstance(t, App))
        tr = t.rhs
        tl = t.lhs

        assert(isinstance(tr, Var))
        assert('x' == tr.id)

        t = tl
        assert(isinstance(t, App))
        tr = t.rhs
        tl = t.lhs

        assert(isinstance(tr, Var))
        assert('x' == tr.id)

        assert(isinstance(tl, Var))
        assert('x' == tl.id)

class ParensIdentity(TestCase):
    def test(self):
        t = p('(\\x x)')

        assert(isinstance(t, Par))
        t = t.subterm

        assert(isinstance(t, Abs))
        assert('x' == t.id)
        t = t.body

        assert(isinstance(t, Var))
        assert('x' == t.id)

class ParensSelfApplication(TestCase):
    def test(self):
        t = p('(x x)')

        assert(isinstance(t, Par))
        t = t.subterm

        assert(isinstance(t, App))

        tl = t.lhs
        assert(isinstance(tl, Var))
        assert('x' == tl.id)

        tr = t.rhs
        assert(isinstance(tr, Var))
        assert('x' == tr.id)

class NestedLambda(TestCase):
    def test(self):
        t = p('\\x x \\x x')

        assert(isinstance(t, Abs))
        t = t.body

        assert(isinstance(t, App))
        assert(isinstance(t.lhs, Var))
        assert('x' == t.lhs.id)

        assert(isinstance(t.rhs, Abs))
        assert(isinstance(t.rhs.body, Var))
        assert('x' == t.rhs.body.id)

class UnbalancedParensFailure(TestCase):
    def test(self):
        failed = False
        try:
            p('(\\x x')
        except IncompleteParseError:
            failed = True
        assert(failed)

