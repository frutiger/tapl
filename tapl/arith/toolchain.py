# tapl.arith.toolchain

import re

from .terms     import ZeroValue, Succ, Pred, TrueValue, FalseValue, IsZero, If
from .table     import table_literal
from .evaluator import evaluate

class Toolchain(object):
    '''Grammar:

Term -> ZERO
Term -> SUCC Term
Term -> PRED Term
Term -> TRUE
Term -> FALSE
Term -> ISZERO Term
Term -> IF Term THEN Term ELSE Term
'''

    tokens = {
        'whitespace': {' ', '\n'},
        'types': (
            ('TRUE',   re.compile('^true$')),
            ('FALSE',  re.compile('^false$')),
            ('ZERO',   re.compile('^zero$')),
            ('ISZERO', re.compile('^iszero$')),
            ('SUCC',   re.compile('^succ$')),
            ('PRED',   re.compile('^pred$')),
            ('IF',     re.compile('^if$')),
            ('THEN',   re.compile('^then$')),
            ('ELSE',   re.compile('^else$')),
        ),
    }

    table = table_literal

    rules = (
        ((),        {},        ZeroValue),   # ZERO
        ((1,),      {0},       Succ),        # Succ Term
        ((1,),      {0},       Pred),        # Pred Term
        ((),        {},        TrueValue),   # TRUE
        ((),        {},        FalseValue),  # FALSE
        ((1,),      {0},       IsZero),      # IsZero Term
        ((1, 3, 5), {0, 1, 2}, If),          # IF Term THEN Term ELSE Term
    )

    @staticmethod
    def semantics(node):
        return node

    @staticmethod
    def evaluate(node):
        return evaluate(node)

