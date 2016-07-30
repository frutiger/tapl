# tapl.visit

def visit(term, visitor):
    subterms = getattr(term, 'subterms', set())
    acceptor = visitor._acceptors.get(type(term), None)
    if acceptor:
        if len(subterms):
            acceptor = acceptor(visitor, term)
        else:
            acceptor(visitor, term)
        for subterm in subterms:
            next(acceptor)
            visit(getattr(term, subterm), visitor)
        if len(subterms):
            try:
                next(acceptor)
            except StopIteration:
                return
            raise Exception('Incomplete acceptor')
    else:
        for subterm in subterms:
            visit(getattr(term, subterm), visitor)

def visitor(cls):
    cls._acceptors = {}
    for name, method in cls.__dict__.items():
        if hasattr(method, '_acceptor'):
            cls._acceptors[method._acceptor] = method
    return cls

def accept(Term):
    def decorate(function):
        function._acceptor = Term
        return function
    return decorate

