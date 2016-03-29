# tapl.untyped.concrete

from collections import namedtuple

Variable    = namedtuple('Variable',    ['location', 'id'])
Abstraction = namedtuple('Abstraction', ['location', 'slash', 'id', 'body'])
Application = namedtuple('Application', ['location', 'lhs', 'rhs'])
Parens      = namedtuple('Parens',      ['location', 'lparen', 'subterm', 'rparen'])
Goal        = namedtuple('Goal',        ['location', 'value', 'dummy'])

