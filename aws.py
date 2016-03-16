# aws

import io

from tapl.driver import lex, parse, evaluate, write

def aws(event, context):
    input = event['input'].decode('UTF-8')

    tokens = lex(event['interpreter'], io.StringIO(input))
    term   = parse(event['interpreter'], tokens)
    term   = evaluate(event['interpreter'], term)

    output = io.StringIO()
    write(event['interpreter'], term, 'TextFormatter', output)
    return output.getvalue().encode('UTF-8')

if __name__ == '__main__':
    import sys
    print aws({
        'interpreter': sys.argv[1],
        'input': ' '.join(sys.argv[2:]),
    }, None)

