# tapl.__main__

import argparse
import importlib
import io
import os
import sys

from .relexer  import UnknownToken
from .lrparser import IncompleteParseError, ParserError
from .visit    import visit

def write(term, Formatter):
    formatter = Formatter()
    visit(term, formatter)
    formatter.finish()

def get(package, module_name, attribute_name):
    return getattr(importlib.import_module(package + '.' + module_name),
                    attribute_name)

def interpret(package, source, Formatter, error, should_eval):
    lex      = get(package, 'lexer',     'lex')
    parse    = get(package, 'parser',    'parse')

    tokens = lex(source)
    try:
        term = parse(tokens)
    except UnknownToken as e:
        print(e.args[0], file=error)
        return -1
    except (IncompleteParseError, ParserError) as e:
        print('Error:', e.args[0], file=error)
        return -1

    if should_eval:
        evaluate = get(package, 'evaluator', 'evaluate')
        term = evaluate(term)
    write(term, Formatter)

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
                except IncompleteParseError:
                    line = line + getline('. ') + '\n'
            result = evaluate(term)
            write(result, Formatter)
        except (UnknownToken, ParserError) as e:
            print(e.args[0], file=error)
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
    parser.add_argument('-f', '--format', default='text')
    parser.add_argument('-n', '--no-evaluate', action='store_true')
    args = parser.parse_args()

    package = 'tapl.' + args.interpreter
    try:
        importlib.import_module(package)
    except ImportError as e:
        print('Unknown interpreter: ' + args.interpreter, file=sys.stderr)
        return -1

    formatter_name = args.format[0].upper() + args.format[1:] + 'Formatter'
    Formatter = get(package, 'formatters', formatter_name)

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

    return interpret(package,
                     infile,
                     lambda: Formatter(outfile),
                     sys.stderr,
                     not args.no_evaluate)

if __name__ == '__main__':
    sys.exit(main())

