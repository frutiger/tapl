# tapl.arith.interpreter

import io

from . import lexer
from . import parser
from . import evaluator
from . import printer

def interpret(source, output, error):
    tokens = lexer.lex(source)
    try:
        term = parser.parse(tokens)
    except parser.Error as e:
        print(e.args[0], file=error)
        return -1
    result = evaluator.evaluate(term)
    printer.print(output, result)

def repl(getline, output, error):
    while True:
        try:
            line = getline('> ') + '\n'
            while True:
                tokens = lexer.lex(io.StringIO(line))
                try:
                    term = parser.parse(tokens)
                    break
                except parser.IncompleteError:
                    line = line + getline('. ') + '\n'
            result = evaluator.evaluate(term)
            printer.print(output, result)
        except parser.Error as e:
            print('Error:', e.args[0], file=error)
            continue
        except KeyboardInterrupt:
            print('', file=output)
            break
        except EOFError:
            print('', file=output)
            break

