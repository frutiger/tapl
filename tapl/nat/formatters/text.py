# tapl.nat.formatters.text
# coding=UTF-8

from ...visit import accept, visitor

from .. import terms

@visitor
class Formatter:
    def __init__(self, file):
        self._file    = file
        self._context = []

    def finish(self):
        self._file.write(u'\n')

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

