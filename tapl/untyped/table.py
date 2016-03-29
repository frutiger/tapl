# tapl.untyped.table
# coding: UTF-8

from . import concrete

# Given a grammar with the following production rules:
#
# r0. § → Term $
# r1. Term -> ID
# r2. Term -> LAMBDA ID Term
# r3. Term -> Term Term
# r4. Term -> LPAREN Term RPAREN
#
# We can produce the following item sets, along with their transitions:
#
#  0. [Goal -> · Term $]                 1
#     [Term -> · ID]                     2
#     [Term -> · LAMBDA ID Term]         3
#     [Term -> · Term Term]              1
#     [Term -> · LPAREN Term RPAREN]     4
#  1. [Goal -> Term · $]                10
#     [Term -> Term · Term]              5
#     [Term -> · ID]                     2
#     [Term -> · LAMBDA ID Term]         3
#     [Term -> · Term Term]              5
#     [Term -> · LPAREN Term RPAREN]     4
#  2. [Term -> ID ·]
#  3. [Term -> LAMBDA · ID Term]         8
#  4. [Term -> LPAREN · Term RPAREN]     6
#     [Term -> · ID]                     2
#     [Term -> · LAMBDA ID Term]         3
#     [Term -> · Term Term]              6
#     [Term -> · LPAREN Term RPAREN]     4
#  5. [Term -> Term Term ·]
#     [Term -> Term · Term]              5
#     [Term -> · ID]                     2
#     [Term -> · LAMBDA ID Term]         3
#     [Term -> · Term Term]              5
#     [Term -> · LPAREN Term RPAREN]     4
#  6. [Term -> LPAREN Term · RPAREN]     7
#     [Term -> Term · Term]              5
#     [Term -> · ID]                     2
#     [Term -> · LAMBDA ID Term]         3
#     [Term -> · Term Term]              5
#     [Term -> · LPAREN Term RPAREN]     4
#  7. [Term -> LPAREN Term RPAREN ·]
#  8. [Term -> LAMBDA ID · Term]         9
#     [Term -> · ID]                     2
#     [Term -> · LAMBDA ID Term]         3
#     [Term -> · Term Term]              9
#     [Term -> · LPAREN Term RPAREN]     4
#  9. [Term -> LAMBDA ID Term ·]
#     [Term -> Term · Term]              5
#     [Term -> · ID]                     2
#     [Term -> · LAMBDA ID Term]         3
#     [Term -> · Term Term]              5
#     [Term -> · LPAREN Term RPAREN]     4
# 10. [Goal -> Term $ ·]                10
#
# Using the transitions, we can produce the following shift-reduce table:
#
# |-------|----|--------|--------|--------|-----|------|
# | State | ID | LAMBDA | LPAREN | RPAREN |   $ | Term |
# |-------|----|--------|--------|--------|-----|------|
# |     0 | s2 |     s3 |     s4 |        |     |    1 |
# |     1 | s2 |     s3 |     s4 |        |  10 |    5 |
# |     2 | r1 |     r1 |     r1 |     r1 |  r1 |      |
# |     3 | s8 |        |        |        |     |      |
# |     4 | s2 |     s3 |     s4 |        |     |    6 |
# |     5 | r3 |     r3 |     r3 |     r3 |  r3 |    5 |
# |     6 | s2 |     s3 |     s4 |     s7 |     |    5 |
# |     7 | r4 |     r4 |     r4 |     r4 |  r4 |      |
# |     8 | s2 |     s3 |     s4 |        |     |    9 |
# |     9 | s2 |     s3 |     s4 |     r2 |  r2 |    5 |
# |    10 | r0 |     r0 |     r0 |     r0 |  r0 |      |
# |-------|----|--------|--------|--------|-----|------|
#

table = {
    'start': 0,
    'finish': 10,
    'shifts': {
        (0,  'ID'):      2,
        (0,  'LAMBDA'):  3,
        (0,  'LPAREN'):  4,
        (1,  'ID'):      2,
        (1,  'LAMBDA'):  3,
        (1,  'LPAREN'):  4,
        (1,  '$'):      10,
        (3,  'ID'):      8,
        (4,  'ID'):      2,
        (4,  'LAMBDA'):  3,
        (4,  'LPAREN'):  4,
        (6,  'ID'):      2,
        (6,  'LAMBDA'):  3,
        (6,  'LPAREN'):  4,
        (6,  'RPAREN'):  7,
        (8,  'ID'):      2,
        (8,  'LAMBDA'):  3,
        (8,  'LPAREN'):  4,
        (9,  'ID'):      2,
        (9,  'LAMBDA'):  3,
        (9,  'LPAREN'):  4,
    },
    'reductions': {
        2:  concrete.Variable,
        5:  concrete.Application,
        7:  concrete.Parens,
        9:  concrete.Abstraction,
        10: concrete.Goal,
    },
    'gotos': {
        0: 1,
        1: 5,
        4: 6,
        5: 5,
        6: 5,
        8: 9,
        9: 5,
    },
}

