# tapl.bool.formatters.text

from ...visit import accept, visitor
from ..terms  import TrueValue, FalseValue, If

@visitor
class Formatter:
    def __init__(self, file):
        self._file    = file
        self._context = []

    def finish(self):
        self._file.write(u'\n')

    @accept(terms.TrueValue)
    def true_value(self, location):
        self._file.write(u'true')

    @accept(terms.FalseValue)
    def false_value(self, location):
        self._file.write(u'false')

    @accept(terms.If)
    def if_stmt(self, location):
        self._file.write(u'if ')
        yield
        self._file.write(u' then ')
        yield
        self._file.write(u' else ')
        yield

