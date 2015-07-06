# tapl.arith

from . import evaluator
from . import lexer
from . import parser
from . import printer

class Interpreter:
    @classmethod
    def lex(self, source):
        return lexer.lex(source)

    @classmethod
    def parse(self, tokens):
        return parser.parse(tokens)

    @classmethod
    def evaluate(self, term):
        return evaluator.evaluate(term)

    @classmethod
    def print(self, file, term):
        return printer.print(file, term)

