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

