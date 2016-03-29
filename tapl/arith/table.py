# tapl.arith.table
# coding: UTF-8

from . import concrete

# Given a grammar with the following production rules:
#
# r0. § → Term $
# r1. Term -> ZERO
# r2. Term -> SUCC Term
# r3. Term -> PRED Term
# r4. Term -> TRUE
# r6. Term -> FALSE
# r7. Term -> ISZERO Term
# r8. Term -> IF Term THEN Term ELSE Term
#
# We can produce the following item sets, along with their transitions:
#
#  0. [Goal -> · Term $]                         1
#     [Term -> · ZERO]                           2
#     [Term -> · SUCC Term]                      3
#     [Term -> · PRED Term]                      4
#     [Term -> · TRUE]                           5
#     [Term -> · FALSE]                          6
#     [Term -> · ISZERO Term]                    7
#     [Term -> · IF Term THEN Term ELSE Term]    8
#  1. [Goal -> Term · $]                        17
#  2. [Term -> ZERO ·]
#  3. [Term -> SUCC · Term]                      9
#     [Term -> · ZERO]                           2
#     [Term -> · SUCC Term]                      3
#     [Term -> · PRED Term]                      4
#     [Term -> · TRUE]                           5
#     [Term -> · FALSE]                          6
#     [Term -> · ISZERO Term]                    7
#     [Term -> · IF Term THEN Term ELSE Term]    8
#  4. [Term -> PRED · Term]                     10
#     [Term -> · ZERO]                           2
#     [Term -> · SUCC Term]                      3
#     [Term -> · PRED Term]                      4
#     [Term -> · TRUE]                           5
#     [Term -> · FALSE]                          6
#     [Term -> · ISZERO Term]                    7
#     [Term -> · IF Term THEN Term ELSE Term]    8
#  5. [Term -> TRUE ·]
#  6. [Term -> FALSE ·]
#  7. [Term -> ISZERO · Term]                   11
#     [Term -> · ZERO]                           2
#     [Term -> · SUCC Term]                      3
#     [Term -> · PRED Term]                      4
#     [Term -> · TRUE]                           5
#     [Term -> · FALSE]                          6
#     [Term -> · ISZERO Term]                    7
#     [Term -> · IF Term THEN Term ELSE Term]    8
#  8. [Term -> IF · Term THEN Term ELSE Term]   12
#     [Term -> · ZERO]                           2
#     [Term -> · SUCC Term]                      3
#     [Term -> · PRED Term]                      4
#     [Term -> · TRUE]                           5
#     [Term -> · FALSE]                          6
#     [Term -> · ISZERO Term]                    7
#     [Term -> · IF Term THEN Term ELSE Term]    8
#  9. [Term -> SUCC Term ·]
# 10. [Term -> PRED Term ·]
# 11. [Term -> ISZERO Term ·]
# 12. [Term -> IF Term · THEN Term ELSE Term]   13
# 13. [Term -> IF Term THEN · Term ELSE Term]   14
#     [Term -> · ZERO]                           2
#     [Term -> · SUCC Term]                      3
#     [Term -> · PRED Term]                      4
#     [Term -> · TRUE]                           5
#     [Term -> · FALSE]                          6
#     [Term -> · ISZERO Term]                    7
#     [Term -> · IF Term THEN Term ELSE Term]    8
# 14. [Term -> IF Term THEN Term · ELSE Term]   15
# 15. [Term -> IF Term THEN Term ELSE · Term]   16
#     [Term -> · ZERO]                           2
#     [Term -> · SUCC Term]                      3
#     [Term -> · PRED Term]                      4
#     [Term -> · TRUE]                           5
#     [Term -> · FALSE]                          6
#     [Term -> · ISZERO Term]                    7
#     [Term -> · IF Term THEN Term ELSE Term]    8
# 16. [Term -> IF Term THEN Term ELSE Term ·]
# 17. [Goal -> Term $ ·]
#
# Using the transitions, we can produce the following shift-reduce table:
#
# |----|----|----|----|----|----|----|-----|-----|-----|-----|----|
# | St | ZE | SU | PR | TR | FA | IS |  IF |  TH |  EL |   $ | Te |
# |----|----|----|----|----|----|----|-----|-----|-----|-----|----|
# |  0 | s2 | s3 | s4 | s5 | s6 | s7 |  s8 |     |     |     |  1 |
# |  1 |    |    |    |    |    |    |     |     |     |  17 |    |
# |  2 | r1 | r1 | r1 | r1 | r1 | r1 |  r1 |  r1 |  r1 |  r1 |    |
# |  3 | s2 | s3 | s4 | s5 | s6 | s7 |  s8 |     |     |     |  9 |
# |  4 | s2 | s3 | s4 | s5 | s6 | s7 |  s8 |     |     |     | 10 |
# |  5 | r4 | r4 | r4 | r4 | r4 | r4 |  r4 |  r4 |  r4 |  r4 |    |
# |  6 | r6 | r6 | r6 | r6 | r6 | r6 |  r6 |  r6 |  r6 |  r6 |    |
# |  7 | s2 | s3 | s4 | s5 | s6 | s7 |  s8 |     |     |     | 11 |
# |  8 | s2 | s3 | s4 | s5 | s6 | s7 |  s8 |     |     |     | 12 |
# |  9 | r2 | r2 | r2 | r2 | r2 | r2 |  r2 |  r2 |  r2 |  r2 |    |
# | 10 | r3 | r3 | r3 | r3 | r3 | r3 |  r3 |  r3 |  r3 |  r3 |    |
# | 11 | r7 | r7 | r7 | r7 | r7 | r7 |  r7 |  r7 |  r7 |  r7 |    |
# | 12 |    |    |    |    |    |    |     | s13 |     |     |    |
# | 13 | s2 | s3 | s4 | s5 | s6 | s7 |  s8 |     |     |     | 14 |
# | 14 |    |    |    |    |    |    |     |     | s15 |     |    |
# | 15 | s2 | s3 | s4 | s5 | s6 | s7 |  s8 |     |     |     | 16 |
# | 16 | r8 | r8 | r8 | r8 | r8 | r8 |  r8 |  r8 |  r8 |  r8 |    |
# | 17 | r0 | r0 | r0 | r0 | r0 | r0 |  r0 |  r0 |  r0 |  r0 |    |
# |----|----|----|----|----|----|----|-----|-----|-----|-----|----|
#

table = {
    'start': 0,
    'finish': 17,
    'shifts': {
        ( 0, 'ZERO'):    2,
        ( 0, 'SUCC'):    3,
        ( 0, 'PRED'):    4,
        ( 0, 'TRUE'):    5,
        ( 0, 'FALSE'):   6,
        ( 0, 'ISZERO'):  7,
        ( 0, 'IF'):      8,
        ( 1, '$'):      17,
        ( 3, 'ZERO'):    2,
        ( 3, 'SUCC'):    3,
        ( 3, 'PRED'):    4,
        ( 3, 'TRUE'):    5,
        ( 3, 'FALSE'):   6,
        ( 3, 'ISZERO'):  7,
        ( 3, 'IF'):      8,
        ( 4, 'ZERO'):    2,
        ( 4, 'SUCC'):    3,
        ( 4, 'PRED'):    4,
        ( 4, 'TRUE'):    5,
        ( 4, 'FALSE'):   6,
        ( 4, 'ISZERO'):  7,
        ( 4, 'IF'):      8,
        ( 7, 'ZERO'):    2,
        ( 7, 'SUCC'):    3,
        ( 7, 'PRED'):    4,
        ( 7, 'TRUE'):    5,
        ( 7, 'FALSE'):   6,
        ( 7, 'ISZERO'):  7,
        ( 7, 'IF'):      8,
        ( 8, 'ZERO'):    2,
        ( 8, 'SUCC'):    3,
        ( 8, 'PRED'):    4,
        ( 8, 'TRUE'):    5,
        ( 8, 'FALSE'):   6,
        ( 8, 'ISZERO'):  7,
        ( 8, 'IF'):      8,
        (12, 'THEN'):   13,
        (13, 'ZERO'):    2,
        (13, 'SUCC'):    3,
        (13, 'PRED'):    4,
        (13, 'TRUE'):    5,
        (13, 'FALSE'):   6,
        (13, 'ISZERO'):  7,
        (13, 'IF'):      8,
        (14, 'ELSE'):   15,
        (15, 'ZERO'):    2,
        (15, 'SUCC'):    3,
        (15, 'PRED'):    4,
        (15, 'TRUE'):    5,
        (15, 'FALSE'):   6,
        (15, 'ISZERO'):  7,
        (15, 'IF'):      8,
    },
    'reductions': {
         2: concrete.ZeroValue,
         5: concrete.TrueValue,
         6: concrete.FalseValue,
         9: concrete.Succ,
        10: concrete.Pred,
        11: concrete.IsZero,
        16: concrete.If,
        17: concrete.Goal,
    },
    'gotos': {
         0:  1,
         3:  9,
         4: 10,
         7: 11,
         8: 12,
        13: 14,
        15: 16,
    },
}

