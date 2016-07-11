#!/usr/bin/env python3

from collections import OrderedDict
from itertools   import chain
from sys         import stdin

from build_table import parse_grammar, classify_terms, build

order = lambda iterable: OrderedDict(map(reversed, enumerate(iterable)))

def format_reduction(reduction):
    return reduction[0] + ' → ' + ' '.join(reduction[1]) + ' ·'

def tabulate(cols, callback=print, sep=''):
    cell_formats = ['{{{0}:{{{1}}}}}'.format(i, len(cols) + i) for i in range(len(cols))]
    cells_format = sep.join(cell_formats)
    widths       = [max(len('{}'.format(c)) for c in col) for col in cols]
    rule         = sep.join(map(lambda x: x * '-', widths))
    for cells in zip(*cols):
        if all(cell == None for cell in cells):
            callback(rule)
        else:
            callback(cells_format.format(*cells, *widths))

def main():
    rules,        goal      = parse_grammar(stdin)
    nonterminals, terminals = classify_terms(rules)
    symbols                 = order(chain(nonterminals, terminals))
    table                   = build(rules, goal)

    rules     = order(rules)
    item_sets = order(table['item_sets'])


    print('Given a grammar with the following production rules:')
    print()
    for rule, index in rules.items():
        print('r{}. {} → {}'.format(index, rule[0], ' '.join(rule[1])))
    print()
    print('We can produce the following item sets, along with their transitions:')
    print()
    cols = [[] for i in range(5)]
    for item_set, index in item_sets.items():
        if item_set in table['reductions']:
            reduction = table['reductions'][item_set]
            rule      = rules[reduction]
            cols[0].append(index)
            cols[1].append('. ')
            cols[2].append('[' + format_reduction(reduction) + ']')
            cols[3].append('  →  ')
            cols[4].append('r' + str(rule))
        for symbol in symbols:
            if (item_set, symbol) in table['shifts']:
                shift = table['shifts'][(item_set, symbol)]
                for item in shift[0]:
                    cols[0].append(index)
                    cols[1].append('. ')
                    cols[2].append('[' + str(item) + ']')
                    cols[3].append('  →  ')
                    cols[4].append(item_sets[shift[1]])
    tabulate(cols, lambda l: print('' + l))
    print()
    print('Using the transitions, we can produce the following shift-reduce table:')
    print()
    cols = [[None, 'State', None]] + [[None, symbol, None] for symbol in symbols]
    for item_set, index in item_sets.items():
        cols[0].append(index)
        for symbol, symbol_index in symbols.items():
            if item_set in table['reductions'] and symbol in terminals:
                rule = rules[table['reductions'][item_set]]
                cell = 'r' + str(rule)
            elif (item_set, symbol) in table['shifts']:
                transition = item_sets[table['shifts'][(item_set, symbol)][1]]
                cell = ('s' if symbol in terminals else '') + str(transition)
            else:
                cell = ''
            cols[1 + symbol_index].append(cell)
    for col in cols:
        col.append(None)
    tabulate(cols, lambda l: print('| ' + l + ' |'), ' | ')
    print()

if __name__ == '__main__':
    main()

