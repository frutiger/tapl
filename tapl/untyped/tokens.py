# tapl.untyped.tokens

import re

tokens = {
    'whitespace': {' ', '\n'},
    'types': {
        'LPAREN': re.compile('^\($'),
        'RPAREN': re.compile('^\)$'),
        'LAMBDA': re.compile('^\\\\$'),
        'ID':     re.compile('^[a-z]+$'),
    },
}

