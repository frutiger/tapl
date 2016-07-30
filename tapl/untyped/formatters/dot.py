# tapl.untyped.formatters.dot
# coding: UTF-8

from ...visit import accept, visitor

from .. import terms

@visitor
class Formatter:
    def __init__(self, file):
        self._file     = file
        self._labels   = {}
        self._stack    = [self._get_label_id(u'root')]
        self._write(u'digraph term {')

    def _get_label_id(self, value):
        label_id = len(self._labels)
        self._labels[label_id] = value
        return label_id

    def _add_parent(self, id):
        label = self._get_label_id(id)
        self._write(u'{} -> {}'.format(self._stack[-1], label))
        self._stack.append(label)

    def _write(self, *args, **kwargs):
        self._file.write(*args, **kwargs)
        self._file.write(u'\n')

    def finish(self):
        for id, label in self._labels.items():
            self._write(u'{} [label = {}]'.format(id, label))
        self._write(u'}')

    @accept(terms.Variable)
    def variable(self, variable):
        self._write(u'{} -> {}'.format(self._stack[-1],
                                       self._get_label_id(variable.id)))

    @accept(terms.Abstraction)
    def abstraction(self, abstraction):
        self._add_parent(u'"\u03bb"')
        yield
        self._stack.pop()

    @accept(terms.Application)
    def application(self, application):
        self._add_parent(u'""')
        yield
        yield
        self._stack.pop()

