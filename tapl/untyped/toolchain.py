# tapl.untyped.toolchain
# coding: UTF-8

import re

from .terms     import Variable, Abstraction, Application, \
                       to_nameless
from .evaluator import evaluate

class Toolchain(object):
    '''Grammar:

Term -> Variable
Variable -> ID
Term -> LAMBDA ID Term
Term -> LPAREN Term RPAREN
Term -> Term Term
'''

    tokens = {
        'whitespace': {' ', '\n'},
        'types': {
            'LPAREN': re.compile('^\($'),
            'RPAREN': re.compile('^\)$'),
            'LAMBDA': re.compile('^\\\\$'),
            'ID':     re.compile('^[a-z]+$'),
        },
    }

    table = {
        'finish': 8,
        'gotos': {
            (2, 'Term'): 8,
            (9, 'Term'): 3,
            (0, 'Term'): 4,
            (3, 'Term'): 3,
            (8, 'Term'): 3,
            (6, 'Term'): 9,
            (4, 'Term'): 3,
        },
        'reductions': {
            1: ('Term', 3, 2),
            3: ('Term', 2, 3),
            4: ('Term', 3, 1),
            7: ('Term', 1, 0),
        },
        'start': 2,
        'shifts': {
            (8, 'ID'): 7,
            (4, 'LPAREN'): 6,
            (3, 'LAMBDA'): 5,
            (3, 'ID'): 7,
            (8, 'LAMBDA'): 5,
            (6, 'LPAREN'): 6,
            (9, 'RPAREN'): 1,
            (6, 'ID'): 7,
            (3, 'LPAREN'): 6,
            (4, 'ID'): 7,
            (8, 'LPAREN'): 6,
            (9, 'LAMBDA'): 5,
            (0, 'LPAREN'): 6,
            (2, 'LPAREN'): 6,
            (9, 'ID'): 7,
            (9, 'LPAREN'): 6,
            (0, 'LAMBDA'): 5,
            (4, 'LAMBDA'): 5,
            (2, 'ID'): 7,
            (2, 'LAMBDA'): 5,
            (6, 'LAMBDA'): 5,
            (0, 'ID'): 7,
            (5, 'ID'): 0,
        },
    }

    rules = (
        ((0,),   {},     Variable),        # ID
        ((1, 2), {1},    Abstraction),     # LAMBDA ID Term
        ((1,),   {0},    lambda _, x: x),  # LPAREN Term RPAREN
        ((0, 1), {0, 1}, Application),     # Term Term
    )

    @staticmethod
    def semantics(node):
        return to_nameless(node)

    @staticmethod
    def evaluate(node):
        return evaluate(node)

