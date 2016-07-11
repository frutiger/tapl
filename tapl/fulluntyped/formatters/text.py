# tapl.untyped.formatters.text
# coding: UTF-8

from ...visit import accept, visitor

from .. import terms

@visitor
class Formatter:
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

    @accept(terms.Variable, 'id')
    def write_id(self, id):
        self._file.write(self._context[id])

    @accept(terms.Abstraction, 'id')
    def insert_and_write_id(self, id):
        while id in self._context:
            id = id + '\''
        self._context.insert(0, id)
        self._file.write(u'(λ' + id + '.')

    @accept(terms.Abstraction)
    def pop_id(self, result):
        self._context.pop(0)
        self._file.write(u')')

    @accept(terms.Application, 'location')
    def application_lparens(self, location):
        self._file.write(u'(')

    @accept(terms.Application, 'lhs')
    def application_space(self, visited_lhs):
        self._file.write(u' ')

    @accept(terms.Application, 'rhs')
    def application_rparens(self, visited_rhs):
        self._file.write(u')')

