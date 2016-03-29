# tests.untyped.test_parser

from unittest import TestCase
from io       import StringIO

from tapl.relexer        import Location, ReLexer
from tapl.untyped.tokens import tokens

from tapl.lrparser         import IncompleteParseError, LRParser
from tapl.untyped.table    import table
from tapl.untyped.concrete import Abstraction as Abs, \
                                  Application as App, \
                                  Variable    as Var, \
                                  Parens      as Par

lexer = ReLexer(tokens)
def lex(source):
    return lexer.lex(source)

def p(text):
    parser = LRParser(table)
    return parser.parse(lex(StringIO(text)))

class Variable(TestCase):
    def test(self):
        t = p(u'x')

        assert(isinstance(t, Var))
        assert(u'x' == t.id)

class Identity(TestCase):
    def test(self):
        t = p(u'\\x x')

        assert(isinstance(t, Abs))
        assert(u'x' == t.id)
        t = t.body

        assert(isinstance(t, Var))
        assert(u'x'  == t.id)

class SelfApplication(TestCase):
    def test(self):
        t = p(u'\\x x x')

        assert(isinstance(t, Abs))
        assert(u'x' == t.id)
        t = t.body

        assert(isinstance(t, App))
        tr = t.rhs
        tl = t.lhs

        assert(isinstance(tr, Var))
        assert(u'x' == tr.id)

        assert(isinstance(tl, Var))
        assert(u'x' == tl.id)

class TripleApplication(TestCase):
    def test(self):
        t = p(u'\\x x x x')

        assert(isinstance(t, Abs))
        assert(u'x' == t.id)
        t = t.body

        assert(isinstance(t, App))
        tr = t.rhs
        tl = t.lhs

        assert(isinstance(tr, Var))
        assert(u'x' == tr.id)

        t = tl
        assert(isinstance(t, App))
        tr = t.rhs
        tl = t.lhs

        assert(isinstance(tr, Var))
        assert(u'x' == tr.id)

        assert(isinstance(tl, Var))
        assert(u'x' == tl.id)

class ParensIdentity(TestCase):
    def test(self):
        t = p(u'(\\x x)')

        assert(isinstance(t, Par))
        t = t.subterm

        assert(isinstance(t, Abs))
        assert(u'x' == t.id)
        t = t.body

        assert(isinstance(t, Var))
        assert(u'x' == t.id)

class ParensSelfApplication(TestCase):
    def test(self):
        t = p(u'(x x)')

        assert(isinstance(t, Par))
        t = t.subterm

        assert(isinstance(t, App))

        tl = t.lhs
        assert(isinstance(tl, Var))
        assert(u'x' == tl.id)

        tr = t.rhs
        assert(isinstance(tr, Var))
        assert(u'x' == tr.id)

class NestedLambda(TestCase):
    def test(self):
        t = p(u'\\x x \\x x')

        assert(isinstance(t, Abs))
        t = t.body

        assert(isinstance(t, App))
        assert(isinstance(t.lhs, Var))
        assert(u'x' == t.lhs.id)

        assert(isinstance(t.rhs, Abs))
        assert(isinstance(t.rhs.body, Var))
        assert(u'x' == t.rhs.body.id)

class UnbalancedParensFailure(TestCase):
    def test(self):
        failed = False
        try:
            p(u'(\\x x')
        except IncompleteParseError:
            failed = True
        assert(failed)

