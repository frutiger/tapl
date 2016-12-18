# tests.untyped.test_integration
# coding: UTF-8

from io       import StringIO
from unittest import TestCase

from tapl                   import analysis
from tapl.evaluation        import evaluate
from tapl.visit             import visit
from tapl.untyped.toolchain import Toolchain

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
            (u'\\x x',              u'(λx.x)'),
            (u'((\\x x)(\\y y y))', u'(λy.(y y))'),
        )

        for input, output in cases:
            self.assertEqual(eval(input), output)

