#!/usr/bin/env python3

from collections import OrderedDict
from sys         import stdin

from build_table import parse_grammar, classify_terms, build

order = lambda iterable: OrderedDict(map(reversed, enumerate(iterable)))

def main():
    rules,        goal      = parse_grammar(stdin)
    nonterminals, terminals = classify_terms(rules)
    table                   = build(rules, goal)

    rules     = order(rules)
    item_sets = order(table['item_sets'])

    print({
        'start': item_sets[table['start']],
        'finish': item_sets[table['finish']],
        'shifts': {
            (item_sets[state[0]], state[1]): item_sets[transition[1]] \
                for state, transition in table['shifts'].items() \
                if state[1] in terminals
        },
        'reductions': {
            item_sets[state]: (rule[0], len(rule[1]), rules[rule]) \
                for state, rule in table['reductions'].items()
        },
        'gotos': {
            (item_sets[state[0]], state[1]): item_sets[transition[1]] \
                for state, transition in table['shifts'].items() \
                if state[1] in nonterminals
        },
    })

if __name__ == '__main__':
    main()

