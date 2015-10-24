# tapl.__main__

import argparse
import importlib
import io
import os
import sys

from .driver   import lex, parse, evaluate, write, flush
from .relexer  import UnknownToken
from .lrparser import IncompleteParseError, ParserError

def repl(interpreter_name, formatter_name):
    while True:
        try:
            line = input('> ') + '\n'
            while True:
                try:
                    tokens = lex(interpreter_name, io.StringIO(line))
                    term   = parse(interpreter_name, tokens)
                    break
                except IncompleteParseError:
                    line = line + input('. ') + '\n'
            term = evaluate(interpreter_name, term)
            write(interpreter_name, term, formatter_name, sys.stdout)
        except (UnknownToken, ParserError) as e:
            print(e.args[0], file=sys.stderr)
            continue
        except (KeyboardInterrupt, EOFError):
            flush(interpreter_name, formatter_name, sys.stdout)
            break

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('interpreter',
                         nargs='?', default=os.path.basename(sys.argv[0]))
    parser.add_argument('-i', '--input',  type=str)
    parser.add_argument('-o', '--output', type=str)
    parser.add_argument('-f', '--format', default='text')
    parser.add_argument('-n', '--no-evaluate', action='store_true')
    args = parser.parse_args()

    try:
        importlib.import_module('tapl.' + args.interpreter)
    except ImportError as e:
        print('Unknown interpreter: ' + args.interpreter, file=sys.stderr)
        return -1

    interpreter_name = args.interpreter
    formatter_name = args.format[0].upper() + args.format[1:] + 'Formatter'

    if args.input is None and args.output is None:
        import readline
        return repl(args.interpreter, formatter_name)

    if args.input == '-' or args.input is None:
        infile = sys.stdin
    else:
        infile = open(args.input)

    if args.output == '-' or args.output is None:
        outfile = sys.stdout
    else:
        outfile = open(args.output)

    try:
        tokens = lex(interpreter_name, infile)
        term   = parse(interpreter_name, tokens)
        if not args.no_evaluate:
            term = evaluate(interpreter_name, term)
        write(interpreter_name, term, formatter_name, outfile)
    except (UnknownToken, IncompleteParseError, ParserError) as e:
        print(e.args[0], file=sys.stderr)
        return -1

if __name__ == '__main__':
    sys.exit(main())

