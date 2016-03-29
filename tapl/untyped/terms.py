# tapl.untyped.terms

from ..lrparser import ParserError

from . import concrete

class Term(object):
    fields   = ('location',)
    subterms = tuple()

    def __init__(self, location):
        self.location = location

class Variable(Term):
    fields   = Term.fields + ('id',)

    def __init__(self, location, id):
        Term.__init__(self, location)
        self.id = id

    def __str__(self):
        return 'Var({})'.format(self.id)

class Abstraction(Term):
    fields   = Term.fields   + ('id', 'body')
    subterms = Term.subterms + ('body',)

    def __init__(self, location, id, body):
        Term.__init__(self, location)
        self.id   = id
        self.body = body

    def __str__(self):
        return 'Abs({}, {})'.format(self.id, self.body)

class Application(Term):
    fields   = Term.fields   + ('lhs', 'rhs')
    subterms = Term.subterms + ('lhs', 'rhs')

    def __init__(self, location, lhs, rhs):
        Term.__init__(self, location)
        self.lhs = lhs
        self.rhs = rhs

    def __str__(self):
        return 'App({}, {})'.format(self.lhs, self.rhs)

def from_concrete(term, context=None):
    if not context:
        context = []

    if isinstance(term, concrete.Variable):
        if term.id not in context:
            raise ParserError(term.location,
                             'Unknown variable "{}"'.format(term.id))
        return Variable(term.location, context.index(term.id))
    elif isinstance(term, concrete.Abstraction):
        return Abstraction(term.location,
                           term.id,
                           from_concrete(term.body, [term.id] + context))
    elif isinstance(term, concrete.Application):
        return Application(term.location,
                           from_concrete(term.lhs, context),
                           from_concrete(term.rhs, context))
    elif isinstance(term, concrete.Parens):
        return from_concrete(term.subterm, context)
    elif isinstance(term, concrete.Goal):
        return from_concrete(term.value, context)

