# tapl.untyped.toolchain

import re

from .terms      import Variable, Abstraction, Application, to_nameless
from .table      import table_literal
from .evaluator  import Evaluator
from .formatters import text, dot

class Toolchain(object):
    '''Grammar:

Term -> Term SubTerm
Term -> SubTerm
SubTerm -> ID
SubTerm -> LAMBDA ID Term
SubTerm -> LPAREN Term RPAREN
'''

    tokens = {
        'whitespace': {' ', '\n'},
        'types': (
            ('LAMBDA', re.compile('^\\\\$')),
            ('LPAREN', re.compile('^\($')),
            ('RPAREN', re.compile('^\)$')),
            ('ID',     re.compile('^[a-z]+$')),
        )
    }

    table = table_literal

    rules = (
        ((0, 1), {0, 1}, Application),     # Term SubTerm
        ((0,),   {0},    lambda _, x: x),  # SubTerm
        ((0,),   {},     Variable),        # ID
        ((1, 2), {1},    Abstraction),     # LAMBDA ID Term
        ((1,),   {0},    lambda _, x: x),  # LPAREN Term RPAREN
    )

    formatters = {
        'text': text.Formatter,
        'dot':  dot.Formatter,
    }

    @staticmethod
    def semantics(node):
        return to_nameless(node)

    Evaluator = Evaluator

