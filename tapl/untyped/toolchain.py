# tapl.untyped.toolchain
# coding: UTF-8

import re

from .terms     import Variable, Abstraction, Application, to_nameless
from .evaluator import evaluate

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
        'types': {
            'LPAREN': re.compile('^\($'),
            'RPAREN': re.compile('^\)$'),
            'LAMBDA': re.compile('^\\\\$'),
            'ID':     re.compile('^[a-z]+$'),
        },
    }

    table = {
        'gotos': {
            (7, 'SubTerm'): 4,
            (10, 'SubTerm'): 4,
            (9, 'SubTerm'): 6,
            (9, 'Term'): 7,
            (0, 'Term'): 10,
            (0, 'SubTerm'): 6,
            (3, 'Term'): 1,
            (1, 'SubTerm'): 4,
            (3, 'SubTerm'): 6,
        },
        'shifts': {
            (9, 'LAMBDA'): 5,
            (3, 'LPAREN'): 9,
            (1, 'LPAREN'): 9,
            (9, 'LPAREN'): 9,
            (3, 'LAMBDA'): 5,
            (0, 'LPAREN'): 9,
            (1, 'LAMBDA'): 5,
            (9, 'ID'): 8,
            (7, 'LAMBDA'): 5,
            (0, 'LAMBDA'): 5,
            (10, 'LPAREN'): 9,
            (7, 'LPAREN'): 9,
            (3, 'ID'): 8,
            (1, 'ID'): 8,
            (5, 'ID'): 3,
            (0, 'ID'): 8,
            (7, 'ID'): 8,
            (10, 'LAMBDA'): 5,
            (7, 'RPAREN'): 2,
            (10, 'ID'): 8,
        },
        'start': 0,
        'reductions': {
            8: ('SubTerm', 1, 2),
            1: ('SubTerm', 3, 3),
            2: ('SubTerm', 3, 4),
            4: ('Term', 2, 0),
            6: ('Term', 1, 1),
        },
        'finish': 10,
    }

    rules = (
        ((0, 1), {0, 1}, Application),     # Term SubTerm
        ((0,),   {0},    lambda _, x: x),  # SubTerm
        ((0,),   {},     Variable),        # ID
        ((1, 2), {1},    Abstraction),     # LAMBDA ID Term
        ((1,),   {0},    lambda _, x: x),  # LPAREN Term RPAREN
    )

    @staticmethod
    def semantics(node):
        return to_nameless(node)

    @staticmethod
    def evaluate(node):
        return evaluate(node)

