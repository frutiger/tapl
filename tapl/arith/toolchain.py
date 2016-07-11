# tapl.arith.toolchain
# coding: UTF-8

import re

from .terms     import ZeroValue, Succ, Pred, TrueValue, FalseValue, IsZero, If
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

    table = {
        'start': 7,
        'gotos': {
            (5, 'Term'): 2,
            (7, 'Term'): 9,
            (14, 'Term'): 15,
            (0, 'Term'): 1,
            (4, 'Term'): 16,
            (3, 'Term'): 12,
            (6, 'Term'): 13,
        },
        'finish': 9,
        'reductions': {
            16: ('Term', 6, 6),
            2: ('Term', 2, 5),
            8: ('Term', 1, 3),
            10: ('Term', 1, 0),
            11: ('Term', 1, 4),
            12: ('Term', 2, 2),
            13: ('Term', 2, 1),
        },
        'shifts': {
            (14, 'FALSE'): 11,
            (4, 'FALSE'): 11,
            (0, 'IF'): 0,
            (5, 'ISZERO'): 5,
            (6, 'ISZERO'): 5,
            (15, 'ELSE'): 4,
            (6, 'TRUE'): 8,
            (5, 'PRED'): 3,
            (7, 'ISZERO'): 5,
            (3, 'SUCC'): 6,
            (6, 'SUCC'): 6,
            (5, 'FALSE'): 11,
            (7, 'TRUE'): 8,
            (14, 'ISZERO'): 5,
            (0, 'PRED'): 3,
            (0, 'SUCC'): 6,
            (7, 'SUCC'): 6,
            (6, 'PRED'): 3,
            (4, 'SUCC'): 6,
            (4, 'ISZERO'): 5,
            (5, 'IF'): 0,
            (3, 'TRUE'): 8,
            (7, 'PRED'): 3,
            (5, 'ZERO'): 10,
            (14, 'ZERO'): 10,
            (6, 'FALSE'): 11,
            (3, 'ISZERO'): 5,
            (1, 'THEN'): 14,
            (14, 'SUCC'): 6,
            (5, 'SUCC'): 6,
            (14, 'IF'): 0,
            (4, 'IF'): 0,
            (4, 'TRUE'): 8,
            (14, 'TRUE'): 8,
            (0, 'FALSE'): 11,
            (7, 'IF'): 0,
            (4, 'ZERO'): 10,
            (6, 'IF'): 0,
            (3, 'IF'): 0,
            (3, 'PRED'): 3,
            (0, 'ISZERO'): 5,
            (7, 'ZERO'): 10,
            (0, 'ZERO'): 10,
            (14, 'PRED'): 3,
            (7, 'FALSE'): 11,
            (3, 'FALSE'): 11,
            (4, 'PRED'): 3,
            (5, 'TRUE'): 8,
            (0, 'TRUE'): 8,
            (6, 'ZERO'): 10,
            (3, 'ZERO'): 10,
        },
    }

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

