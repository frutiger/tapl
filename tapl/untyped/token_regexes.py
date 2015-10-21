# tapl.untyped.token_regexes

import re

WHITESPACE  = {' ', '\n'}

TOKEN_TYPES = {
    'LPAREN': re.compile('^\($'),
    'RPAREN': re.compile('^\)$'),
    'LAMBDA': re.compile('^\\\\$'),
    'ID':     re.compile('^[a-z]+$')
}

