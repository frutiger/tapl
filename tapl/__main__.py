# tapl.__main__

import argparse
import importlib
import io
import os
import sys

from . import errors, visit

def write(term, Formatter):
    formatter = Formatter()
    visit.visit(term, formatter)
    formatter.finish()

def get(package, module_name, attribute_name):
    return getattr(importlib.import_module(package + '.' + module_name),
                    attribute_name)

def interpret(package, source, Formatter, error):
    lex      = get(package, 'lexer',     'lex')
    parse    = get(package, 'parser',    'parse')
    evaluate = get(package, 'evaluator', 'evaluate')

    tokens = lex(source)
    try:
        term = parse(tokens)
    except errors.ParserError as e:
        print(e.args[0], file=error)
        return -1
    result = evaluate(term)
    write(result, Formatter)

def repl(package, getline, Formatter, error):
    lex      = get(package, 'lexer',     'lex')
    parse    = get(package, 'parser',    'parse')
    evaluate = get(package, 'evaluator', 'evaluate')

    while True:
        try:
            line = getline('> ') + '\n'
            while True:
                tokens = lex(io.StringIO(line))
                try:
                    term = parse(tokens)
                    break
                except errors.IncompleteParseError:
                    line = line + getline('. ') + '\n'
            result = evaluate(term)
            write(result, Formatter)
        except errors.ParserError as e:
            print('Error:', e.args[0], file=error)
            continue
        except KeyboardInterrupt:
            Formatter().finish()
            break
        except EOFError:
            Formatter().finish()
            break

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('interpreter', nargs='?', default=os.path.basename(sys.argv[0]))
    parser.add_argument('-i', '--input',  type=str)
    parser.add_argument('-o', '--output', type=str)
    args = parser.parse_args()

    package = 'tapl.' + args.interpreter
    try:
        importlib.import_module(package)
    except ImportError as e:
        print('Unknown interpreter: ' + args.interpreter, file=sys.stderr)
        return -1

    Formatter = get(package, 'formatters', 'TextFormatter')

    if args.input is None and args.output is None:
        import readline
        return repl(package, input, lambda: Formatter(sys.stdout), sys.stderr)

    if args.input == '-' or args.input is None:
        infile = sys.stdin
    else:
        infile = open(args.input)

    if args.output == '-' or args.output is None:
        outfile = sys.stdout
    else:
        outfile = open(args.output)

    return interpret(package, infile, lambda: Formatter(outfile), sys.stderr)

if __name__ == '__main__':
    sys.exit(main())

