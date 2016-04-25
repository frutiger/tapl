#!/usr/bin/env python3
# coding: UTF-8

from collections import defaultdict, OrderedDict
from functools   import reduce
from itertools   import chain
from math        import log
from pprint      import pprint
import sys

def format_reduction(reduction):
    return reduction[0] + ' → ' + ' '.join(reduction[1]) + ' ·'

def format_item(item):
    symbols = list(item[2])
    symbols.insert(item[1], '·')
    return item[0] + ' → ' + ' '.join(symbols)

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

def order(iterable):
    result = OrderedDict()
    for index, value in enumerate(iterable):
        result[value] = index
    return result

def close(elements, get_candidates):
    result = set(elements)
    while True:
        to_add = set(get_candidates(result)) - result
        if not to_add:
            break
        result.update(to_add)
    return frozenset(result)

def seed_item(rule):
    return rule[0], 0, rule[1]

class ItemExtender:
    def __init__(self, rules):
        self._rules = rules

    def __call__(self, item_set):
        for item in item_set:
            if item[1] == len(item[2]):
                continue

            next_symbol = item[2][item[1]]
            for rule in self._rules:
                if next_symbol == rule[0]:
                    yield seed_item(rule)

class ItemSetExtender:
    def __init__(self, rules, observer):
        self._rules    = rules
        self._observer = observer

    def __call__(self, item_sets):
        for item_set in item_sets:
            transitions = defaultdict(lambda: [[], []])
            for item in item_set:
                if item[1] == len(item[2]):
                    rule = (item[0], item[2])
                    if rule[0] == '§':
                        self._observer.finish = item_set
                        continue
                    assert(rule in self._rules)
                    self._observer.add_reduction(item_set, rule)
                else:
                    next_symbol = item[2][item[1]]
                    new_item = (item[0], item[1] + 1, item[2])
                    transitions[next_symbol][0].append(item)
                    transitions[next_symbol][1].append(new_item)
                    if item[0] == '§' and item[1] == 0:
                        self._observer.start = item_set
            for next_symbol, transition in transitions.items():
                next_item_set = close(transition[1], ItemExtender(self._rules))
                self._observer.shifts[item_set, next_symbol] = \
                                                 (transition[0], next_item_set)
                yield next_item_set

class Observer:
    def __init__(self):
        self.shifts     = {}
        self.reductions = {}
        self.start      = None
        self.finish     = None

    def add_reduction(self, state, rule):
        if state not in self.reductions:
            self.reductions[state] = rule

        if self.reductions[state] == rule:
            return

        raise RuntimeError('Ambiguous reduction from:\n{}'.format(
                '\n'.join(format_item(item) for item in state)))

def generate(goal, rules):
    observer  = Observer()
    item_sets = close({close({seed_item(('§', (goal,)))},
                             ItemExtender(rules))},
                      ItemSetExtender(rules, observer))

    return item_sets, observer

def build(goal, productions):
    rules = order(productions)

    nonterminals = order(set(p[0] for p in rules) - {'§'})
    terminals    = order(set(chain(*chain(p[1] for p in rules))) - \
                         set(nonterminals))
    symbols      = order(set(chain(nonterminals, terminals)))

    item_sets, observer = generate(goal, rules)
    item_sets = order(item_sets)

    return rules, nonterminals, terminals, symbols, observer, item_sets

def table(observer, terminals, nonterminals, item_sets, rules):
    return {
        'start': item_sets[observer.start],
        'finish': item_sets[observer.finish],
        'shifts': {
            (item_sets[state[0]], state[1]): item_sets[transition[1]] \
                for state, transition in observer.shifts.items() \
                if state[1] in terminals
        },
        'reductions': {
            item_sets[state]: (rule[0], len(rule[1]), rules[rule]) \
                for state, rule in observer.reductions.items()
        },
        'gotos': {
            (item_sets[state[0]], state[1]): item_sets[transition[1]] \
                for state, transition in observer.shifts.items() \
                if state[1] in nonterminals
        },
    }

def document(rules, nonterminals, terminals, symbols, observer, item_sets):
    print('# coding: UTF-8')
    print('#')
    print('# Given a grammar with the following production rules:')
    print('#')
    for rule, index in rules.items():
        print('# r{}. {} → {}'.format(index, rule[0], ' '.join(rule[1])))
    print('#')
    print('# We can produce the following item sets, along with their transitions:')
    print('#')
    cols = [[] for i in range(5)]
    for item_set, index in item_sets.items():
        if item_set in observer.reductions:
            reduction = observer.reductions[item_set]
            rule      = rules[reduction]
            cols[0].append(index)
            cols[1].append('. ')
            cols[2].append('[' + format_reduction(reduction) + ']')
            cols[3].append('  →  ')
            cols[4].append('r' + str(rule))
        for symbol in symbols:
            if (item_set, symbol) in observer.shifts:
                shift = observer.shifts[(item_set, symbol)]
                for item in shift[0]:
                    cols[0].append(index)
                    cols[1].append('. ')
                    cols[2].append('[' + format_item(item) + ']')
                    cols[3].append('  →  ')
                    cols[4].append(item_sets[shift[1]])
    tabulate(cols, lambda l: print('# ' + l))
    print('#')
    print('# Using the transitions, we can produce the following shift-reduce table:')
    print('#')
    cols = [[None, 'State', None]] + [[None, symbol, None] for symbol in symbols]
    for item_set, index in item_sets.items():
        cols[0].append(index)
        for symbol, symbol_index in symbols.items():
            if item_set in observer.reductions and symbol in terminals:
                rule = rules[observer.reductions[item_set]]
                cell = 'r' + str(rule)
            elif (item_set, symbol) in observer.shifts:
                transition = item_sets[observer.shifts[(item_set, symbol)][1]]
                cell = ('s' if symbol in terminals else '') + str(transition)
            else:
                cell = ''
            cols[1 + symbol_index].append(cell)
    for col in cols:
        col.append(None)
    tabulate(cols, lambda l: print('# | ' + l + ' |'), ' | ')
    print('#')
    print()
    print('table = {')
    print('''    'start': {},'''.format(item_sets[observer.start]))
    print('''    'finish': {},'''.format(item_sets[observer.finish]))
    print('''    'shifts': {''')
    for state, transition in sorted(observer.shifts.items(),
                                    key=lambda x: (item_sets[x[0][0]], x[0][1])):
        if state[1] not in terminals:
            continue
        print('''        ({}, '{}'): {},'''.format(item_sets[state[0]],
                                                   state[1],
                                                   item_sets[transition[1]]))
    print('    },')
    print('''    'reductions': {''')
    for state, rule in sorted(observer.reductions.items(),
                              key=lambda x: item_sets[x[0]]):
        print('        {}: {},'.format(item_sets[state],
                                       (len(rule[1]), rules[rule])))
    print('    },')
    print('''    'gotos': {''')
    for state, transition in sorted(observer.shifts.items(),
                                    key=lambda x: item_sets[x[0][0]]):
        if state[1] not in nonterminals:
            continue
        print('''        ({}, '{}'): {},'''.format(item_sets[state[0]],
                                                   state[1],
                                                   item_sets[transition[1]]))
    print('    },')
    print('}')
    print()

if __name__ == '__main__':
    productions = []
    for line in sys.stdin:
        production = [x.strip() for x in line.split('->')]
        production[1] = tuple(x.strip() for x in production[1].split())
        productions.append(tuple(production))
    productions = tuple(productions)
    goal        = productions[0][0]

    rules, nonterminals, terminals, symbols, observer, item_sets = \
                                                   build(goal, productions)
    print(table(observer, terminals, nonterminals, item_sets, rules))
    #document(rules, nonterminals, terminals, symbols, observer, item_sets)

