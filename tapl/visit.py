# tapl.visit

def visit(term, visitor):
    accumulator = None
    subterms    = getattr(term, 'subterms', set())
    for field in term._fields:
        prop     = getattr(term, field)
        result   = visit(prop, visitor) if field in subterms else prop
        acceptor = visitor._acceptors.get((type(term), field), None)
        if acceptor is not None:
            accumulator = acceptor(visitor, result)
    return accumulator

def visitor(cls):
    cls._acceptors = {}
    for name, method in cls.__dict__.items():
        if hasattr(method, '_acceptor'):
            cls._acceptors[method._acceptor] = method
    return cls

def accept(type, field=None):
    def decorate(function):
        function._acceptor = (type, field)
        return function
    return decorate

