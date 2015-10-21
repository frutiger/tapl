# tapl.untyped.terms

from collections import namedtuple

from . import concrete

Variable    = namedtuple('Variable',    ['location', 'binder'])
Abstraction = namedtuple('Abstraction', ['location', 'hint', 'body'])
Application = namedtuple('Application', ['location', 'lhs',  'rhs'])

Abstraction.subterms = { 'body' }
Application.subterms = { 'lhs', 'rhs' }

def from_concrete(term, context=None):
    if not context:
        context = []

    if isinstance(term, concrete.Variable):
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

