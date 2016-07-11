# tapl.untyped.formatters.dot
# coding: UTF-8

from ...visit import accept, visitor

from .. import terms

@visitor
class Formatter:
    def __init__(self, file):
        self._file   = file
        self._labels = {}
        self._file.write(u'digraph term {\n')

    def _get_label_id(self, value):
        label_id = len(self._labels)
        self._labels[label_id] = value
        return label_id

    def finish(self):
        for id, label in self._labels.items():
            self._file.write(u'{} [label = {}]\n'.format(id, label))
        self._file.write(u'}\n')

    @accept(terms.Variable, 'id')
    def in_variable(self, id):
        return self._get_label_id(id)

    @accept(terms.Abstraction, 'id')
    def pre_abstraction(self, id):
        self._current_id = self._get_label_id(u'\u03bb')

    @accept(terms.Abstraction, 'body')
    def post_abstraction(self, visited_body):
        self._file.write(u'{} -> {}\n'.format(self._current_id, visited_body))
        return self._current_id

    @accept(terms.Application, 'lhs')
    def pre_application(self, visited_lhs):
        self._current_id = self._get_label_id(u'""')
        self._file.write(u'{} -> {}\n'.format(self._current_id, visited_lhs))

    @accept(terms.Application, 'rhs')
    def post_application(self, visited_rhs):
        self._file.write(u'{} -> {}\n'.format(self._current_id, visited_rhs))
        return self._current_id

