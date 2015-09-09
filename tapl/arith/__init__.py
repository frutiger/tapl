# tapl.arith

from . import evaluator
from . import lexer
from . import parser
from . import writer

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
    def write(self, file, term):
        return writer.write(file, term)

