# tapl.driver

import importlib
import sys

def start(interpret, repl):
    if len(sys.argv) == 1:
        import readline
        repl(input, sys.stdout, sys.stderr)
    elif len(sys.argv) == 2:
        if sys.argv[1] == '-':
            source = sys.stdin
        else:
            source = open(sys.argv[1])
        sys.exit(interpret(source, sys.stdout, sys.stderr))

def drive(interpreter):
    module      = 'tapl.{}.interpreter'.format(interpreter)
    interpreter = importlib.import_module(module)
    start(interpreter.interpret, interpreter.repl)

