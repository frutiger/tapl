# tapl.nat.toolchain

import re

from .terms     import TrueValue, FalseValue, If
from .table     import table_literal
from .evaluator import evaluate

class Toolchain(object):
    '''Grammar:

Term -> TRUE
Term -> FALSE
Term -> IF Term THEN Term ELSE Term
'''

    tokens = {
        'whitespace': {' ', '\n'},
        'types': (
            ('TRUE',   re.compile('^true$')),
            ('FALSE',  re.compile('^false$')),
            ('IF',     re.compile('^if$')),
            ('THEN',   re.compile('^then$')),
            ('ELSE',   re.compile('^else$')),
        ),
    }

    table = table_literal

    rules = (
        ((),        {},        TrueValue),    # TRUE
        ((),        {},        FalseValue),   # FALSE
        ((1, 3, 5), {0, 1, 2}, If),           # IF Term THEN Term ELSE Term
    )

    @staticmethod
    def semantics(node):
        return node

    @staticmethod
    def evaluate(node):
        return evaluate(node)

