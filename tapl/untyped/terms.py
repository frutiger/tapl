# tapl.untyped.terms

from collections import namedtuple

from ..lrparser import ParserError

from . import concrete

Variable    = namedtuple('Variable',    ['location', 'id'])
Abstraction = namedtuple('Abstraction', ['location', 'id', 'body'])
Application = namedtuple('Application', ['location', 'lhs',  'rhs'])

Abstraction.subterms = { 'body' }
Application.subterms = { 'lhs', 'rhs' }

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

