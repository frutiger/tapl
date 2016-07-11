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

    @accept(terms.ZeroValue, 'location')
    def write_zero(self, location):
        self._file.write(u'zero')

    @accept(terms.Succ, 'location')
    def write_succ(self, location):
        self._file.write(u'succ ')

    @accept(terms.Pred, 'location')
    def write_pred(self, location):
        self._file.write(u'pred ')

