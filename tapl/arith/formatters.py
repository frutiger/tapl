# tapl.arith.formatters

from ..visit import visit, accept, visitor

from . import terms

@visitor
class TextFormatter:
    def __init__(self, file):
        self._file    = file
        self._context = []

    def finish(self):
        self._file.write(u'\n')

    @accept(terms.TrueValue, 'location')
    def write_true(self, location):
        self._file.write(u'true')

    @accept(terms.FalseValue, 'location')
    def insert_false(self, location):
        self._file.write(u'false')

    @accept(terms.ZeroValue, 'location')
    def write_zero(self, location):
        self._file.write(u'zero')

    @accept(terms.Succ, 'location')
    def write_succ(self, location):
        self._file.write(u'succ ')

    @accept(terms.Pred, 'location')
    def write_pred(self, location):
        self._file.write(u'pred ')

    @accept(terms.IsZero, 'location')
    def write_iszero(self, location):
        self._file.write(u'iszero ')

    @accept(terms.If, 'location')
    def write_if(self, location):
        self._file.write(u'if ')

    @accept(terms.If, 'predicate')
    def write_then(self, predicate):
        self._file.write(u' then ')

    @accept(terms.If, 'true_value')
    def write_else(self, true_value):
        self._file.write(u' else ')

