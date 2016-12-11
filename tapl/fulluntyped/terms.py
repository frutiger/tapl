# tapl.untyped.terms
# coding: UTF-8

from ..errors import EvaluationError

class Term(object):
    name     = 'Term'
    fields   = ('location',)
    subterms = tuple()

    def __init__(self, location):
        self.location = location

class ZeroValue(Term):
    def __init__(self, location):
        Term.__init__(self, location)

    def __str__(self):
        return 'Zero'

class TrueValue(Term):
    def __init__(self, location):
        Term.__init__(self, location)

    def __str__(self):
        return 'True'

class FalseValue(Term):
    def __init__(self, location):
        Term.__init__(self, location)

    def __str__(self):
        return 'False'

class Succ(Term):
    fields   = Term.fields   + ('argument',)
    subterms = Term.subterms + ('argument',)

    def __init__(self, location, argument):
        Term.__init__(self, location)
        self.argument = argument

    def __str__(self):
        return 'Succ({})'.format(self.argument)

class Pred(Term):
    fields   = Term.fields   + ('argument',)
    subterms = Term.subterms + ('argument',)

    def __init__(self, location, argument):
        Term.__init__(self, location)
        self.argument = argument

    def __str__(self):
        return 'Pred({})'.format(self.argument)

class IsZero(Term):
    fields   = Term.fields   + ('argument',)
    subterms = Term.subterms + ('argument',)

    def __init__(self, location, argument):
        Term.__init__(self, location)
        self.argument = argument

    def __str__(self):
        return 'IsZero({})'.format(self.argument)

class If(Term):
    fields   = Term.fields   + ('predicate', 'true_value', 'false_value')
    subterms = Term.subterms + ('predicate', 'true_value', 'false_value')

    def __init__(self, location, predicate, true_value, false_value):
        Term.__init__(self, location)
        self.predicate   = predicate
        self.true_value  = true_value
        self.false_value = false_value

    def __str__(self):
        return 'If({}, {}, {})'.format(self.predicate,
                                       self.true_value,
                                       self.false_value)

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
    else:
        subterms = [term.location]
        for subterm in term.subterms:
            subterms.append(to_nameless(getattr(term, subterm), context))
        return type(term)(*subterms)

