# tapl.errors

class _LocationError(Exception):
    def __init__(self, location, message):
        Exception.__init__(self, '{} (at {}:{})'.format(message,
                                                        location.line,
                                                        location.column))

class EvaluationError(_LocationError):
    pass

class TypeError(_LocationError):
    pass

