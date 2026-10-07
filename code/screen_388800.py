"""Wide exclusion screen (Section 7, "The exclusion phenomenon").

Claim checked (paper, Section 7): on three structurally different squares
-- the S2 = 3799 optimal square, Pfeffermann's square (1894) and
Wroblewski's square with row sum 648 -- over ALL oriented orthogonal
views, ALL 15 column pairs and ALL 720 bijections between the two
columns of a pair (388,800 pairings in total), no pairing makes the
homogeneous and the affine system solvable at the same time
(equivalently N3(pi) * N2(pi) = 0, by Proposition 9).

Expected, written before the run: 36 oriented views in total over the
three squares, 36 * 15 * 720 = 388,800 pairings, and 0 mixed pairings.

The two systems are tested with hom_aff(), copied verbatim from
seduta_g.py / m5_predizioni.py (the implementation used for the original
screen, which was run ad hoc and not kept as a script; this file
re-creates it for the public release). Squares and partition loading as
in seduta_g.py. Standard library only.

Usage:  python code/screen_388800.py  > logs/screen-388800.log
"""
import os
import sys
import time
from itertools import combinations, permutations

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from semibimagic import find_subsets, partitions as gp


def n1(A, B):
    return sum(1 for a in A for b in B if len(a & b) == 1)


def hom_aff(pj, qj):
    """Solvability of the two systems on the six pairs (p, q)."""
    dj = [qj[j] - pj[j] for j in range(6)]
    ej = [qj[j] ** 2 - pj[j] ** 2 for j in range(6)]
    hom = any(sum(dj[j] for j in J) == 0 and sum(ej[j] for j in J) == 0
              for J in combinations(range(6), 3))
    aff = False
    for j1 in range(6):
        for j2 in range(6):
            if j1 == j2:
                continue
            resto = [j for j in range(6) if j not in (j1, j2)]
            for K in combinations(resto, 2):
                if (qj[j1] - pj[j2] + sum(dj[j] for j in K) == 0 and
                        qj[j1] ** 2 - pj[j2] ** 2
                        + sum(ej[j] for j in K) == 0):
                    aff = True
                    break
            if aff:
                break
        if aff:
            break
    return hom, aff


def carica(V):
    s1 = sum(V) // 6
    s2 = sum(v * v for v in V) // 6
    subs = find_subsets(V, 6, s1, s2)
    parts = [tuple(sorted((frozenset(x) for x in p), key=min))
             for p in gp(subs, V)]
    return s1, s2, parts


PF = [[6, 42, 29, 3, 40, 30], [8, 44, 47, 21, 20, 10],
      [33, 31, 41, 37, 1, 7], [19, 17, 13, 9, 43, 49],
      [36, 2, 5, 35, 34, 38], [48, 14, 15, 45, 12, 16]]
W648 = [[23, 82, 151, 190, 109, 93], [99, 75, 135, 159, 166, 14],
        [90, 215, 102, 39, 97, 105], [111, 119, 177, 114, 1, 126],
        [202, 50, 57, 81, 141, 117], [123, 107, 26, 65, 134, 193]]
WORLDS = [
    ("optimal S2=3799 (omits 19..24)",
     sorted(v for v in range(1, 43) if v not in {19, 20, 21, 22, 23, 24})),
    ("Pfeffermann 1894", sorted(v for r in PF for v in r)),
    ("Wroblewski, row sum 648", sorted(v for r in W648 for v in r)),
]

print(__doc__)
t_all = time.time()
PERMS = list(permutations(range(6)))
assert len(PERMS) == 720
tot_views = tot_pairings = tot_mixed = tot_hom = tot_aff = 0
for label, V in WORLDS:
    s1, s2, parts = carica(V)
    orth = [(i, j) for i in range(len(parts))
            for j in range(i + 1, len(parts))
            if n1(parts[i], parts[j]) == 36]
    views = [(i, j) for i, j in orth] + [(j, i) for i, j in orth]
    w_pair = w_mixed = w_hom = w_aff = 0
    for Ei, Qi in views:
        E, Q = parts[Ei], parts[Qi]
        M = [[next(iter(E[r] & Q[c])) for c in range(6)] for r in range(6)]
        for c1, c2 in combinations(range(6), 2):
            pj = [M[r][c1] for r in range(6)]
            qj = [M[r][c2] for r in range(6)]
            for pi in PERMS:
                h, a = hom_aff(pj, [qj[pi[r]] for r in range(6)])
                w_pair += 1
                w_hom += h
                w_aff += a
                if h and a:
                    w_mixed += 1
                    print(f"  MIXED: {label} view (E={Ei},Q={Qi}) "
                          f"columns ({c1},{c2}) pairing {pi}")
    print(f"{label}: S1={s1} S2={s2}, {len(parts)} row partitions, "
          f"{len(orth)} orthogonal pairs -> {len(views)} oriented views; "
          f"pairings {w_pair}, homogeneous solvable {w_hom}, "
          f"affine solvable {w_aff}, BOTH (mixed) {w_mixed}")
    tot_views += len(views)
    tot_pairings += w_pair
    tot_mixed += w_mixed
    tot_hom += w_hom
    tot_aff += w_aff

print()
print(f"TOTAL: {tot_views} oriented views, {tot_pairings} pairings, "
      f"homogeneous solvable {tot_hom}, affine solvable {tot_aff}, "
      f"mixed {tot_mixed}")
print(f"expected: 36 views, 388800 pairings, 0 mixed -> "
      f"{'AS EXPECTED' if (tot_views, tot_pairings, tot_mixed) == (36, 388800, 0) else 'DIFFERENT FROM EXPECTED'}")
print(f"time {time.time() - t_all:.0f}s")
