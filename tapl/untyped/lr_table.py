# tapl.untyped.lr_table

from . import concrete

# Given a grammar with the following production rules:
#
# Goal -> Term
# Term -> ID
# Term -> LAMBDA ID Term
# Term -> Term Term
# Term -> LPAREN Term RPAREN
#
# We can produce the following item sets, along with their transitions:
#
# 0. [Goal -> · Term]                  1
#    [Term -> · ID]                    2
#    [Term -> · LAMBDA ID Term]        3
#    [Term -> · Term Term]             1
#    [Term -> · LPAREN Term RPAREN]    4
# 1. [Goal -> Term ·]
#    [Term -> Term · Term]             5
#    [Term -> · ID]                    2
#    [Term -> · LAMBDA ID Term]        3
#    [Term -> · Term Term]             5
#    [Term -> · LPAREN Term RPAREN]    4
# 2. [Term -> i ·]
# 3. [Term -> LAMBDA ·ID Term]         8
# 4. [Term -> LPAREN ·Term RPAREN]     6
#    [Term -> · ID]                    2
#    [Term -> · LAMBDA ID Term]        3
#    [Term -> · Term Term]             6
#    [Term -> · LPAREN Term RPAREN]    4
# 5. [Term -> Term Term ·]
#    [Term -> Term · Term]             5
#    [Term -> · ID]                    2
#    [Term -> · LAMBDA ID Term]        3
#    [Term -> · Term Term]             5
#    [Term -> · LPAREN Term RPAREN]    4
# 6. [Term -> LPAREN Term · RPAREN]    7
#    [Term -> Term · Term]             5
#    [Term -> · ID]                    2
#    [Term -> · LAMBDA ID Term]        3
#    [Term -> · Term Term]             5
#    [Term -> · LPAREN Term RPAREN]    4
# 7. [Term -> LPAREN Term RPAREN · ]
# 8. [Term -> LAMBDA ID · Term]        9
#    [Term -> · ID]                    2
#    [Term -> · LAMBDA ID Term]        3
#    [Term -> · Term Term]             9
#    [Term -> · LPAREN Term RPAREN]    4
# 9. [Term -> LAMBDA ID Term·]
#    [Term -> Term · Term]             5
#    [Term -> · ID]                    2
#    [Term -> · LAMBDA ID Term]        3
#    [Term -> · Term Term]             5
#    [Term -> · LPAREN Term RPAREN]    4
#
# Using the transitions, we can produce the following shift-reduce table:
#
# |-------|----|--------|--------|--------|-----|------|
# | State | ID | LAMBDA | LPAREN | RPAREN |   $ | Term |
# |-------|----|--------|--------|--------|-----|------|
# |     0 | s2 |     s3 |     s4 |        |     |    1 |
# |     1 | s2 |     s3 |     s4 |        | acc |    5 |
# |     2 | r1 |     r1 |     r1 |     r1 |  r1 |      |
# |     3 | s8 |        |        |        |     |      |
# |     4 | s2 |     s3 |     s4 |        |     |    6 |
# |     5 | r3 |     r3 |     r3 |     r3 |  r3 |    5 |
# |     6 | s2 |     s3 |     s4 |     s7 |     |    5 |
# |     7 | r4 |     r4 |     r4 |     r4 |  r4 |      |
# |     8 | s2 |     s3 |     s4 |        |     |    9 |
# |     9 | s2 |     s3 |     s4 |     r2 |  r2 |    5 |
# |-------|----|--------|--------|--------|-----|------|
#

ACCEPTANCE = (1, '$')

SHIFTS = {
    (0,  'ID'):     2,
    (0,  'LAMBDA'): 3,
    (0,  'LPAREN'): 4,
    (1,  'ID'):     2,
    (1,  'LAMBDA'): 3,
    (1,  'LPAREN'): 4,
    (3,  'ID'):     8,
    (4,  'ID'):     2,
    (4,  'LAMBDA'): 3,
    (4,  'LPAREN'): 4,
    (6,  'ID'):     2,
    (6,  'LAMBDA'): 3,
    (6,  'LPAREN'): 4,
    (6,  'RPAREN'): 7,
    (8,  'ID'):     2,
    (8,  'LAMBDA'): 3,
    (8,  'LPAREN'): 4,
    (9,  'ID'):     2,
    (9,  'LAMBDA'): 3,
    (9,  'LPAREN'): 4,
}

REDUCTIONS = {
    (2,  'ID'):     concrete.Variable,
    (2,  'LAMBDA'): concrete.Variable,
    (2,  'LPAREN'): concrete.Variable,
    (2,  'RPAREN'): concrete.Variable,
    (2,  '$'):      concrete.Variable,
    (5,  'ID'):     concrete.Application,
    (5,  'LAMBDA'): concrete.Application,
    (5,  'LPAREN'): concrete.Application,
    (5,  'RPAREN'): concrete.Application,
    (5,  '$'):      concrete.Application,
    (7,  'ID'):     concrete.Parens,
    (7,  'LAMBDA'): concrete.Parens,
    (7,  'LPAREN'): concrete.Parens,
    (7,  'RPAREN'): concrete.Parens,
    (7,  '$'):      concrete.Parens,
    (9,  'RPAREN'): concrete.Abstraction,
    (9,  '$'):      concrete.Abstraction,
}

GOTOS = {
    0: 1,
    1: 5,
    4: 6,
    5: 5,
    6: 5,
    8: 9,
    9: 5,
}

