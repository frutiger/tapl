# tapl.driver

import importlib

from .relexer  import ReLexer
from .lrparser import LRParser
from .visit    import visit

def get(interpreter_name, module_name, attribute_name):
    module_name = 'tapl.' + interpreter_name + '.' + module_name
    module = importlib.import_module(module_name)
    return getattr(module, attribute_name)

def lex(interpreter_name, source):
    lexer = ReLexer(get(interpreter_name, 'token_regexes', 'WHITESPACE'),
                    get(interpreter_name, 'token_regexes', 'TOKEN_TYPES'))
    return lexer.lex(source)

def parse(interpreter_name, tokens):
    parser = LRParser(get(interpreter_name, 'lr_table', 'ACCEPTANCE'),
                      get(interpreter_name, 'lr_table', 'SHIFTS'),
                      get(interpreter_name, 'lr_table', 'REDUCTIONS'),
                      get(interpreter_name, 'lr_table', 'GOTOS'))
    from_concrete = get(interpreter_name, 'terms', 'from_concrete')

    return from_concrete(parser.parse(tokens))

def evaluate(interpreter_name, term):
    evaluate = get(interpreter_name, 'evaluator', 'evaluate')
    return evaluate(term)

def write(interpreter_name, term, formatter_name, out):
    formatter = get(interpreter_name, 'formatters', formatter_name)(out)
    visit(term, formatter)
    formatter.finish()

def flush(interpreter_name, formatter_name, out):
    formatter = get(interpreter_name, 'formatters', formatter_name)(out)
    formatter.finish()

