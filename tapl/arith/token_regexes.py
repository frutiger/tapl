# tapl.arith.token_regexes

import re

WHITESPACE  = {' ', '\n'}

TOKEN_TYPES = {
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

