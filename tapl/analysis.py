# tapl.analysis

from .lrparser import LRParser
from .relexer  import ReLexer

def lexical(Toolchain, source):
    return ReLexer(Toolchain.tokens).lex(source)

def syntax(Toolchain, tokens):
    return LRParser(Toolchain.table).parse(tokens)

def semantic(Toolchain, node):
    def visit(node):
        selections = Toolchain.rules[node['reduction']][0]
        children   = [node['children'][slot] for slot in selections]
        recursions = Toolchain.rules[node['reduction']][1]
        children   = [visit(child) if index in recursions else child \
                                       for index, child in enumerate(children)]
        return Toolchain.rules[node['reduction']][2](node['location'], *children)

    if hasattr(Toolchain, 'semantics'):
        return Toolchain.semantics(visit(node))
    else:
        return visit(node)

