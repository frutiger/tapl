# tapl.__main__

import importlib
import io
import os
import sys

from . import errors

def interpret(interpreter, source, output, error):
    tokens = interpreter.lex(source)
    try:
        term = interpreter.parse(tokens)
    except errors.ParserError as e:
        print(e.args[0], file=error)
        return -1
    result = interpreter.evaluate(term)
    interpreter.write(output, result)

def repl(interpreter, getline, output, error):
    while True:
        try:
            line = getline('> ') + '\n'
            while True:
                tokens = interpreter.lex(io.StringIO(line))
                try:
                    term = interpreter.parse(tokens)
                    break
                except errors.IncompleteParseError:
                    line = line + getline('. ') + '\n'
            result = interpreter.evaluate(term)
            interpreter.write(output, result)
        except errors.ParserError as e:
            print('Error:', e.args[0], file=error)
            continue
        except KeyboardInterrupt:
            print('', file=output)
            break
        except EOFError:
            print('', file=output)
            break

def load_interpreter(name):
    return importlib.import_module('tapl.' + name)

def main():
    try:
        interpreter_name = os.path.basename(sys.argv[0])
        module           = load_interpreter(interpreter_name)
    except ImportError:
        try:
            interpreter_name = sys.argv.pop(1)
            module           = load_interpreter(interpreter_name)
        except ImportError:
            print('No interpreter named ' + interpreter_name, file=sys.stderr)
            sys.exit(-1)

    interpreter = module.Interpreter()

    if len(sys.argv) == 1:
        import readline
        repl(interpreter, input, sys.stdout, sys.stderr)
    elif len(sys.argv) == 2:
        if sys.argv[1] == '-':
            source = sys.stdin
        else:
            source = open(sys.argv[1])
        sys.exit(interpret(interpreter, source, sys.stdout, sys.stderr))

if __name__ == '__main__':
    main()

