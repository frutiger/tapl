# tapl.__main__

from __future__ import print_function

import argparse
import importlib
import io
import locale
import os
import sys

from .errors   import EvaluationError
from .lrparser import LRParser, IncompleteParseError, ParserError
from .relexer  import ReLexer, UnknownToken
from .visit    import visit

def lexical_analysis(Toolchain, source):
    return ReLexer(Toolchain.tokens).lex(source)

def syntax_analysis(Toolchain, tokens):
    return LRParser(Toolchain.table).parse(tokens)

def semantic_analysis(Toolchain, node):
    def visit(node):
        selections = Toolchain.rules[node['reduction']][0]
        children   = [node['children'][slot] for slot in selections]
        recursions = Toolchain.rules[node['reduction']][1]
        children   = [visit(child) if index in recursions else child \
                                       for index, child in enumerate(children)]
        return Toolchain.rules[node['reduction']][2](node['location'], *children)

    return Toolchain.semantics(visit(node))

def write(Formatter, term, out):
    formatter = Formatter(out)
    visit(term, formatter)
    formatter.finish()

def getline(*args):
    try:
        return raw_input(*args).decode(locale.getpreferredencoding(True))
    except NameError:
        return input(*args)

def repl(Toolchain, Formatter):
    while True:
        try:
            line = getline('> ') + '\n'
            if line == '\n':
                continue
            while True:
                try:
                    tokens = lexical_analysis(Toolchain, io.StringIO(line))
                    tree   = syntax_analysis(Toolchain, tokens)
                    break
                except IncompleteParseError:
                    line = line + getline('. ') + '\n'
            node = semantic_analysis(Toolchain, tree)
            term = Toolchain.evaluate(node)
            write(Formatter, term, sys.stdout)
        except (UnknownToken, ParserError, EvaluationError) as e:
            print(e.args[0], file=sys.stderr)
            continue
        except (KeyboardInterrupt, EOFError):
            Formatter(sys.stdout).finish()
            break

def interpret(Toolchain, Formatter, infile, outfile, no_evaluate=False):
    tokens = lexical_analysis(Toolchain, infile)
    tree   = syntax_analysis(Toolchain, tokens)
    node   = semantic_analysis(Toolchain, tree)
    if not no_evaluate:
        term = Toolchain.evaluate(node)
        write(Formatter, term, outfile)
    else:
        write(Formatter, node, outfile)

def get_toolchain_and_formatter(toolchain, formatter):
    toolchain_module = 'tapl.{}.toolchain'.format(toolchain)
    try:
        Toolchain = getattr(importlib.import_module(toolchain_module),
                           'Toolchain')
    except ImportError as e:
        print('Unknown toolchain: ' + toolchain, file=sys.stderr)
        return -1

    formatter_module = 'tapl.{}.formatters.{}'.format(toolchain, formatter)
    try:
        Formatter = getattr(importlib.import_module(formatter_module),
                           'Formatter')
    except ImportError as e:
        print(formatter_module)
        print('Unknown formatter: ' + formatter, file=sys.stderr)
        return -1

    return Toolchain, Formatter

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('toolchain',
                         nargs='?', default=os.path.basename(sys.argv[0]))
    parser.add_argument('-i', '--input',  type=str)
    parser.add_argument('-o', '--output', type=str)
    parser.add_argument('-f', '--format', default='text')
    parser.add_argument('-n', '--no-evaluate', action='store_true')
    args = parser.parse_args()

    Toolchain, Formatter = get_toolchain_and_formatter(args.toolchain,
                                                       args.format)

    if args.input is None and args.output is None:
        import readline
        return repl(Toolchain, Formatter)

    if args.input == '-' or args.input is None:
        infile = sys.stdin
    else:
        infile = open(args.input)

    if args.output == '-' or args.output is None:
        outfile = sys.stdout
    else:
        outfile = open(args.output, 'w')

    try:
        return interpret(Toolchain,
                         Formatter,
                         infile,
                         outfile,
                         args.no_evaluate)
    except (UnknownToken, IncompleteParseError, ParserError,
            EvaluationError) as e:
        print(e.args[0], file=sys.stderr)
        return -1

if __name__ == '__main__':
    sys.exit(main())

