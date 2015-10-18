# tapl.arith.lexer

import re

from .. import relexer

def lex(source):
    whitespace  = {' ', '\n'}
    token_types = {
        'TRUE':   re.compile('^true$'),
        'FALSE':  re.compile('^false$'),
        'ZERO':   re.compile('^zero$'),
        'ISZERO': re.compile('^iszero$'),
        'SUCC':   re.compile('^succ$'),
        'PRED':   re.compile('^pred$'),
        'IF':     re.compile('^if$'),
        'THEN':   re.compile('^then$'),
        'ELSE':   re.compile('^else$'),
    }

    lexer = relexer.ReLexer(whitespace, token_types)
    return lexer.lex(source)

