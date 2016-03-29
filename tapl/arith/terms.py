# tapl.arith.terms
# coding: UTF-8

class Term(object):
    fields   = ('location',)
    subterms = tuple()

    def __init__(self, location):
        self.location = location

class ZeroValue(Term):
    def __init__(self, location):
        Term.__init__(self, location)

class TrueValue(Term):
    def __init__(self, location):
        Term.__init__(self, location)

class FalseValue(Term):
    def __init__(self, location):
        Term.__init__(self, location)

class Succ(Term):
    fields   = Term.fields   + ('argument',)
    subterms = Term.subterms + ('argument',)

    def __init__(self, location, argument):
        Term.__init__(self, location)
        self.argument = argument

class Pred(Term):
    fields   = Term.fields   + ('argument',)
    subterms = Term.subterms + ('argument',)

    def __init__(self, location, argument):
        Term.__init__(self, location)
        self.argument = argument

class IsZero(Term):
    fields   = Term.fields   + ('argument',)
    subterms = Term.subterms + ('argument',)

    def __init__(self, location, argument):
        Term.__init__(self, location)
        self.argument = argument

class If(Term):
    fields   = Term.fields   + ('predicate', 'true_value', 'false_value')
    subterms = Term.subterms + ('predicate', 'true_value', 'false_value')

    def __init__(self, location, predicate, true_value, false_value):
        Term.__init__(self, location)
        self.predicate   = predicate
        self.true_value  = true_value
        self.false_value = false_value

producers = [
    # r0. § → Term $
    lambda location, term, _: term,

    # r1. Term → ZERO
    lambda location, _: ZeroValue(location),

    # r2. Term → SUCC Term
    lambda location, _, term: Succ(location, term),

    # r3. Term → PRED Term
    lambda location, _, term: Pred(location, term),

    # r4. Term → TRUE
    lambda location, _: TrueValue(location),

    # r5. Term → FALSE
    lambda location, _: FalseValue(location),

    # r6. Term → ISZERO Term
    lambda location, _, term: IsZero(location, term),

    # r7. Term → IF Term THEN Term ELSE Term
    lambda location, _1, predicate, _2, true_value, _3, false_value: \
                              If(location, predicate, true_value, false_value),
]

