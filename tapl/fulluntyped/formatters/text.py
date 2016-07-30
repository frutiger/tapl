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

    @accept(terms.TrueValue)
    def true_value(self, location):
        self._file.write(u'true')

    @accept(terms.FalseValue)
    def false_value(self, location):
        self._file.write(u'false')

    @accept(terms.ZeroValue)
    def zero_value(self, location):
        self._file.write(u'zero')

    @accept(terms.Succ)
    def succ(self, location):
        self._file.write(u'succ ')
        yield

    @accept(terms.Pred)
    def pred(self, location):
        self._file.write(u'pred ')
        yield

    @accept(terms.IsZero)
    def iszero(self, location):
        self._file.write(u'iszero ')
        yield

    @accept(terms.If)
    def if_stmt(self, location):
        self._file.write(u'if ')
        yield
        self._file.write(u' then ')
        yield
        self._file.write(u' else ')
        yield

