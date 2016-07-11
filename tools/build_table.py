#!/usr/bin/env python3
# coding: UTF-8

from collections import defaultdict
from itertools   import chain

def close(elements, get_candidates):
    result = set(elements)
    while True:
        to_add = set(get_candidates(result)) - result
        if not to_add:
            break
        result.update(to_add)
    return frozenset(result)

class Item:
    def __init__(self, lhs, rhs, marker=0):
        assert(marker <= len(rhs))
        self._lhs    = lhs
        self._rhs    = rhs
        self._marker = marker

    def __str__(self):
        symbols = list(self._rhs)
        symbols.insert(self._marker, '·')
        return '{} → {}'.format(self._lhs, ' '.join(symbols))

    def __eq__(self, other):
        return self.to_tuple() == other.to_tuple()

    def __hash__(self):
        return hash(self.to_tuple())

    def to_tuple(self):
        return (self._lhs, self._rhs, self._marker)

    def to_rule(self):
        return (self._lhs, self._rhs)

    def is_consumed(self):
        return self._marker == len(self._rhs)

    def next_symbol(self):
        return self._rhs[self._marker]

    def advance(self):
        return Item(self._lhs, self._rhs, self._marker + 1)

    def is_start(self):
        return self._lhs == '§' and self._marker == 0

class ItemExtender:
    def __init__(self, rules):
        self._rules = rules

    def __call__(self, item_set):
        for item in item_set:
            if item.is_consumed():
                continue

            next_symbol = item.next_symbol()
            for rule in self._rules:
                if next_symbol == rule[0]:
                    yield Item(rule[0], rule[1])

class ItemSetExtender:
    def __init__(self, rules):
        self._rules     = rules
        self.shifts     = {}
        self.reductions = {}
        self.start      = None
        self.finish     = None

    def _add_reduction(self, state, rule):
        if state not in self.reductions:
            self.reductions[state] = rule

        if self.reductions[state] == rule:
            return

        raise RuntimeError('Ambiguous reduction from:\n{}'.format(
                                       '\n'.join(str(item) for item in state)))

    def __call__(self, item_sets):
        for item_set in item_sets:
            transitions = defaultdict(lambda: [[], []])
            for item in item_set:
                if item.is_consumed():
                    rule = item.to_rule()
                    if rule[0] == '§':
                        self.finish = item_set
                        continue
                    assert(rule in self._rules)
                    self._add_reduction(item_set, rule)
                else:
                    next_symbol = item.next_symbol()
                    new_item    = item.advance()
                    transitions[next_symbol][0].append(item)
                    transitions[next_symbol][1].append(new_item)
                    if item.is_start():
                        self.start = item_set
            for next_symbol, transition in transitions.items():
                next_item_set = close(transition[1], ItemExtender(self._rules))
                self.shifts[item_set, next_symbol] = \
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
                                       '\n'.join(str(item) for item in state)))

def parse_grammar(infile):
    rules = []
    for line in infile:
        rule = [x.strip() for x in line.split('->')]
        rule[1] = tuple(x.strip() for x in rule[1].split())
        rules.append(tuple(rule))
    return rules, rules[0][0]

def classify_terms(rules):
    nonterminals = set(p[0] for p in sorted(rules))
    terminals    = set(chain(*chain(p[1] for p in sorted(rules)))) \
                                                            - set(nonterminals)
    return nonterminals, terminals

def build(rules, goal):
    seed_item         = Item('§', (goal,))
    item_extender     = ItemExtender(rules)
    seed_item_set     = close({seed_item}, item_extender)
    item_set_extender = ItemSetExtender(rules)
    item_sets         = close({seed_item_set}, item_set_extender)

    return {
        'item_sets':    item_sets,
        'shifts':       item_set_extender.shifts,
        'reductions':   item_set_extender.reductions,
        'start':        item_set_extender.start,
        'finish':       item_set_extender.finish,
    }

