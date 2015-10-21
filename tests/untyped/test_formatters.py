# tests.untyped.test_formatters

from io       import StringIO
from unittest import TestCase

from tapl.visit              import *
from tapl.untyped.terms      import *
from tapl.untyped.formatters import *

def var(binder):
    return Variable(None, binder)

def abst(hint, body):
    return Abstraction(None, hint, body)

def app(lhs, rhs):
    return Application(None, lhs, rhs)

def text(t):
    f = StringIO()
    v = TextFormatter(f)
    visit(t, v)
    return f.getvalue()

class IdentityAsText(TestCase):
    def test(self):
        t = abst('x', var(0))
        assert('(\u03bbx.x)' == text(t))

class SelfApplAsText(TestCase):
    def test(self):
        t = abst('x', app(var(0), var(0)))
        assert('(\u03bbx.(x x))' == text(t))

class SelfApplApplAsText(TestCase):
    def test(self):
        t = abst('x', app(app(var(0), var(0)), var(0)))
        assert('(\u03bbx.((x x) x))' == text(t))

