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

    @accept(terms.Variable)
    def variable(self, variable):
        self._file.write(self._context[variable.id])

    @accept(terms.Abstraction)
    def abstraction(self, abstraction):
        id = abstraction.id
        while id in self._context:
            id = id + '\''
        self._context.insert(0, id)
        self._file.write(u'(λ' + id + '.')
        yield
        self._file.write(u')')
        self._context.pop(0)

    @accept(terms.Application)
    def application(self, application):
        self._file.write(u'(')
        yield
        self._file.write(u' ')
        yield
        self._file.write(u')')

