#!/usr/bin/env python3

import ast
import sys

def format(stream, value, indent=0, spacesPerLevel=4):
    if isinstance(value, dict):
        stream.write('{\n')
        for k, v in value.items():
            stream.write(' ' * (indent + 1) * spacesPerLevel)
            format(stream, k, indent + 1, spacesPerLevel)
            stream.write(': ')
            format(stream, v, indent + 1, spacesPerLevel)
            stream.write(',\n')
        stream.write(' ' * indent * spacesPerLevel)
        stream.write('}')
    elif isinstance(value, tuple):
        stream.write('(')
        for index, item in enumerate(value):
            format(stream, item, indent, spacesPerLevel)
            if index != len(value) - 1:
                stream.write(', ')
        stream.write(')')
    elif isinstance(value, list):
        stream.write('[')
        for index, item in enumerate(value):
            format(stream, item, indent, spacesPerLevel)
            if index != len(value) - 1:
                stream.write(', ')
        stream.write(']')
    else:
        stream.write(repr(value))

format(sys.stdout, ast.literal_eval(sys.stdin.read()))

