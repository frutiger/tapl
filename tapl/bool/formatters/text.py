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

    @accept(TrueValue, 'location')
    def write_true(self, location):
        self._file.write(u'true')

    @accept(FalseValue, 'location')
    def insert_false(self, location):
        self._file.write(u'false')

    @accept(If, 'location')
    def write_if(self, location):
        self._file.write(u'if ')

    @accept(If, 'predicate')
    def write_then(self, predicate):
        self._file.write(u' then ')

    @accept(If, 'true_value')
    def write_else(self, true_value):
        self._file.write(u' else ')

