# tapl.nat.toolchain

import re

from .terms     import ZeroValue, Succ, Pred
from .table     import table_literal
from .evaluator import evaluate

class Toolchain(object):
    '''Grammar:

Term -> ZERO
Term -> SUCC Term
Term -> PRED Term
'''

    tokens = {
        'whitespace': {' ', '\n'},
        'types': (
            ('ZERO', re.compile('^zero$')),
            ('SUCC', re.compile('^succ$')),
            ('PRED', re.compile('^pred$')),
        ),
    }

    table = table_literal

    rules = (
        ((),   {},  ZeroValue),  # ZERO
        ((1,), {0}, Succ),       # Succ Term
        ((1,), {0}, Pred),       # Pred Term
    )

    @staticmethod
    def semantics(node):
        return node

    @staticmethod
    def evaluate(node):
        return evaluate(node)
