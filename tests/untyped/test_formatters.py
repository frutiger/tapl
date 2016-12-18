# tests.untyped.test_formatters
# coding: utf-8

from io       import StringIO
from unittest import TestCase

from tapl.visit              import *
from tapl.untyped.terms      import *
from tapl.untyped.toolchain  import Toolchain

def var(id):
    return Variable(None, id)

def abst(id, body):
    return Abstraction(None, id, body)

def app(lhs, rhs):
    return Application(None, lhs, rhs)

def text(t):
    f = StringIO()
    v = Toolchain.formatters['text'](f)
    visit(t, v)
    return f.getvalue()

class IdentityAsText(TestCase):
    def test(self):
        t = abst(u'x', var(0))
        assert(u'(λx.x)' == text(t))

class SelfApplAsText(TestCase):
    def test(self):
        t = abst(u'x', app(var(0), var(0)))
        assert(u'(λx.(x x))' == text(t))

class SelfApplApplAsText(TestCase):
    def test(self):
        t = abst(u'x', app(app(var(0), var(0)), var(0)))
        assert(u'(λx.((x x) x))' == text(t))

