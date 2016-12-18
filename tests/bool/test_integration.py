# tests.bool.test_integration

from io       import StringIO
from unittest import TestCase

from tapl                 import analysis
from tapl.evaluation      import evaluate
from tapl.visit           import visit
from tapl.bool.toolchain  import Toolchain

def eval(string):
    infile    = StringIO(string)
    tokens    = analysis.lexical(Toolchain, infile)
    tree      = analysis.syntax(Toolchain, tokens)
    node      = analysis.semantic(Toolchain, tree)
    result    = evaluate(node, Toolchain.Evaluator())
    outfile   = StringIO()
    formatter = Toolchain.formatters['text'](outfile)
    visit(result, formatter)
    formatter.finish()
    assert(outfile.getvalue()[-1] == '\n')
    return outfile.getvalue()[:-1]

class ExpressionTest(TestCase):
    def test_evaluation(self):
        cases = (
            (u'true',                          u'true'),
            (u'false',                         u'false'),
            (u'if false then false else true', u'true'),
            (u'if true then false else true',  u'false'),
        )

        for input, output in cases:
            self.assertEqual(eval(input), output)

