# tapl.errors

class EvaluationError(Exception):
    def __init__(self, location, message):
        Exception.__init__(self, '{} (at {}:{})'.format(message,
                                                        location.line,
                                                        location.column))

