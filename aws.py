# aws

import io

from tapl.__main__ import get_toolchain_and_formatter, interpret

def aws(event, context):
    Toolchain, Formatter = get_toolchain_and_formatter(event['interpreter'],
                                                       'text')
    infile  = io.StringIO(event['input'].decode('UTF-8'))
    outfile = io.StringIO()
    interpret(Toolchain, Formatter, infile, outfile)
    return outfile.getvalue().encode('UTF-8')

if __name__ == '__main__':
    import sys
    print aws({
        'interpreter': sys.argv[1],
        'input': ' '.join(sys.argv[2:]),
    }, None)

