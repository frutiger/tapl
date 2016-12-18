# tests.fulluntyped.test_integration
# coding: UTF-8

from io       import StringIO
from unittest import TestCase

from tapl                       import analysis
from tapl.evaluation            import evaluate
from tapl.visit                 import visit
from tapl.fulluntyped.toolchain import Toolchain

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
            (u'true',                                                   u'true'),
            (u'false',                                                  u'false'),
            (u'zero',                                                   u'zero'),
            (u'succ zero',                                              u'succ zero'),
            (u'pred zero',                                              u'zero'),
            (u'pred succ zero',                                         u'zero'),
            (u'pred succ zero',                                         u'zero'),
            (u'if false then zero else succ zero',                      u'succ zero'),
            (u'if true then zero else succ zero',                       u'zero'),
            (u'iszero zero',                                            u'true'),
            (u'if iszero zero then zero else succ zero',                u'zero'),
            (u'iszero false',                                           u'iszero false'),
            (u'\\x x',                                                  u'(λx.x)'),
            (u'((\\x x)(\\y y y))',                                     u'(λy.(y y))'),
            (u'((\\n \\s \\z s (n s z))(\\s \\z z)(\\x succ x)zero)',   u'succ zero'),
            (u'((\\n \\s \\z s (n s z))(\\s \\z s z)(\\x succ x)zero)', u'succ succ zero'),
        )

        for input, output in cases:
            self.assertEqual(eval(input), output)

