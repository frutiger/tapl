# tests.untyped.test_parser

from unittest import TestCase
from io       import StringIO

from tapl                   import analysis
from tapl.lrparser          import IncompleteParseError

from tapl.untyped.toolchain import Toolchain
from tapl.untyped.terms     import Abstraction as Abs, \
                                   Application as App, \
                                   Variable    as Var

def p(text):
    tokens = analysis.lexical(Toolchain, StringIO(text))
    tree   = analysis.syntax(Toolchain, tokens)
    node   = analysis.semantic(Toolchain, tree)
    return node

class Identity(TestCase):
    def test(self):
        t = p(u'\\x x')

        assert(isinstance(t, Abs))
        assert(u'x' == t.id)
        t = t.body

        assert(isinstance(t, Var))
        assert(0 == t.id)

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
        assert(0 == tr.id)

        assert(isinstance(tl, Var))
        assert(0 == tl.id)

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
        assert(0 == tr.id)

        t = tl
        assert(isinstance(t, App))
        tr = t.rhs
        tl = t.lhs

        assert(isinstance(tr, Var))
        assert(0 == tr.id)

        assert(isinstance(tl, Var))
        assert(0 == tl.id)

class ParensIdentity(TestCase):
    def test(self):
        t = p(u'(\\x x)')

        assert(isinstance(t, Abs))
        assert(u'x' == t.id)
        t = t.body

        assert(isinstance(t, Var))
        assert(0 == t.id)

class ParensSelfApplication(TestCase):
    def test(self):
        t = p(u'\\x (x x)')

        assert(isinstance(t, Abs))
        assert(u'x' == t.id)
        t = t.body

        assert(isinstance(t, App))
        tr = t.rhs
        tl = t.lhs

        assert(isinstance(tr, Var))
        assert(0 == tr.id)

        assert(isinstance(tl, Var))
        assert(0 == tl.id)

class NestedLambda(TestCase):
    def test(self):
        t = p(u'\\x x \\x x')

        assert(isinstance(t, Abs))
        t = t.body

        assert(isinstance(t, App))
        assert(isinstance(t.lhs, Var))
        assert(0 == t.lhs.id)

        assert(isinstance(t.rhs, Abs))
        assert(isinstance(t.rhs.body, Var))
        assert(0 == t.rhs.body.id)

class UnbalancedParensFailure(TestCase):
    def test(self):
        failed = False
        try:
            p(u'(\\x x')
        except IncompleteParseError:
            failed = True
        assert(failed)

