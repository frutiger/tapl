# tapl.untyped.toolchain

import re

from .terms      import (ZeroValue, TrueValue, FalseValue, Succ, Pred, IsZero,
                         If, Variable, Abstraction, Application, to_nameless)
from .table      import table_literal
from .evaluator  import Evaluator
from .formatters import text

class Toolchain(object):
    '''Grammar:

Term -> Term SubTerm
Term -> SubTerm
Term -> ZERO
Term -> SUCC Term
Term -> PRED Term
Term -> TRUE
Term -> FALSE
Term -> ISZERO Term
Term -> IF Term THEN Term ELSE Term
SubTerm -> ID
SubTerm -> LAMBDA ID Term
SubTerm -> LPAREN Term RPAREN
'''

    tokens = {
        'whitespace': {' ', '\n'},
        'types': (
            ('LPAREN', re.compile('^\($')),
            ('RPAREN', re.compile('^\)$')),
            ('LAMBDA', re.compile('^\\\\$')),
            ('TRUE',   re.compile('^true$')),
            ('FALSE',  re.compile('^false$')),
            ('ZERO',   re.compile('^zero$')),
            ('ISZERO', re.compile('^iszero$')),
            ('SUCC',   re.compile('^succ$')),
            ('PRED',   re.compile('^pred$')),
            ('IF',     re.compile('^if$')),
            ('THEN',   re.compile('^then$')),
            ('ELSE',   re.compile('^else$')),
            ('ID',     re.compile('^[a-z]+$')),
        ),
    }

    table = table_literal

    rules = (
        ((0, 1),    {0, 1},    Application),     # Term SubTerm
        ((0,),      {0},       lambda _, x: x),  # SubTerm
        ((),        {},        ZeroValue),       # ZERO
        ((1,),      {0},       Succ),            # Succ Term
        ((1,),      {0},       Pred),            # Pred Term
        ((),        {},        TrueValue),       # TRUE
        ((),        {},        FalseValue),      # FALSE
        ((1,),      {0},       IsZero),          # IsZero Term
        ((1, 3, 5), {0, 1, 2}, If),              # IF Term THEN Term ELSE Term
        ((0,),      {},        Variable),        # ID
        ((1, 2),    {1},       Abstraction),     # LAMBDA ID Term
        ((1,),      {0},       lambda _, x: x),  # LPAREN Term RPAREN
    )

    formatters = {
        'text': text.Formatter,
    }

    @staticmethod
    def semantics(node):
        return to_nameless(node)

    Evaluator = Evaluator

