# tapl.untyped.terms
# coding: UTF-8

from ..errors import EvaluationError

class Term(object):
    name     = 'Term'
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

def to_nameless(term, context=None):
    if not context:
        context = []

    if isinstance(term, Variable):
        if term.id not in context:
            raise EvaluationError(term.location,
                                  'Unknown variable "{}"'.format(term.id))
        return Variable(term.location, context.index(term.id))
    elif isinstance(term, Abstraction):
        return Abstraction(term.location,
                           term.id,
                           to_nameless(term.body, [term.id] + context))
    elif isinstance(term, Application):
        return Application(term.location,
                           to_nameless(term.lhs, context),
                           to_nameless(term.rhs, context))

producers = [
    # r0. § → Term $
    lambda location, term, _: to_nameless(term),

    # r1. Term → ID
    lambda location, id: Variable(location, id),

    # r2. Term → LAMBDA ID Term
    lambda location, _, id, body: Abstraction(location, id, body),

    # r3. Term → Term Term
    lambda location, lhs, rhs: Application(location, lhs, rhs),

    # r4. Term → LPAREN Term RPAREN
    lambda location, _1, term, _2: term,
]

