# tapl.terms

class Term(object):
    fields   = ('location',)
    subterms = tuple()

    def __init__(self, location):
        self.location = location

