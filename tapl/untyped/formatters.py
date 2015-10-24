# tapl.untyped.formatters
# coding=UTF-8

from ..visit import visit, accept, visitor

from . import terms

@visitor
class TextFormatter:
    def __init__(self, file):
        self._file    = file
        self._context = []

    def finish(self):
        self._file.write(u'\n')

    @accept(terms.Variable, 'binder')
    def write_binder(self, binder):
        self._file.write(self._context[binder])

    @accept(terms.Abstraction, 'hint')
    def insert_and_write_hint(self, hint):
        while hint in self._context:
            hint = hint + '\''
        self._context.insert(0, hint)
        self._file.write(u'(λ' + hint + '.')

    @accept(terms.Abstraction)
    def pop_hint(self, result):
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

@visitor
class DotFormatter:
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

    @accept(terms.Variable, 'binder')
    def in_variable(self, binder):
        return self._get_label_id(binder)

    @accept(terms.Abstraction, 'hint')
    def pre_abstraction(self, hint):
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

