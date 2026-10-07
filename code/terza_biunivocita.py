"""Bersaglio 1a — TERZA implementazione della biunivocita
soluzioni <-> gemelle (riscritta da specifica, non copiata).

FACCE PRE-SCRITTE (stampate prima dei calcoli):
  attesi 1008 soluzioni omogenee = 1008 gemelle 3-allineate,
  9072 affini = 9072 gemelle 2-allineate, zero mismatch di multiset,
  zero collisioni (iniettivita di phi_hom e phi_aff per
  accoppiamento); coppie non vuote per vista 6+7+1 = 14.
  OGNI scarto dagli attesi FERMA la seduta e si verbalizza.

Base: le 3 viste di seduta_g.py (3799 E=38/Q=0; pfeffermann E=2/Q=70;
w648 E=2/Q=1), 15 coppie x 720 accoppiamenti ciascuna, enumerazione
COMPLETA (niente any). Log: logs/terza-biunivocita.log
"""
import os, sys
from itertools import combinations, permutations
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from semibimagic import find_subsets, partitions as gp

L = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "logs")
OUT = []


def P(msg=""):
    OUT.append(msg)
    print(msg, flush=True)


def n1(A, B):
    return sum(1 for a in A for b in B if len(a & b) == 1)


P(__doc__)

PF = [[6, 42, 29, 3, 40, 30], [8, 44, 47, 21, 20, 10],
      [33, 31, 41, 37, 1, 7], [19, 17, 13, 9, 43, 49],
      [36, 2, 5, 35, 34, 38], [48, 14, 15, 45, 12, 16]]
W648 = [[23, 82, 151, 190, 109, 93], [99, 75, 135, 159, 166, 14],
        [90, 215, 102, 39, 97, 105], [111, 119, 177, 114, 1, 126],
        [202, 50, 57, 81, 141, 117], [123, 107, 26, 65, 134, 193]]
V42 = sorted(v for v in range(1, 43) if v not in {19, 20, 21, 22, 23, 24})
V_pf = sorted(v for r in PF for v in r)
V_w = sorted(v for r in W648 for v in r)
VISTE = [("3799 E=38 Q=0", V42, 38, 0),
         ("pfeffermann E=2 Q=70", V_pf, 2, 70),
         ("w648 E=2 Q=1", V_w, 2, 1)]


def carica(V):
    s1 = sum(V) // 6
    s2 = sum(v * v for v in V) // 6
    subs = find_subsets(V, 6, s1, s2)
    parts = [tuple(sorted((frozenset(x) for x in p), key=min))
             for p in gp(subs, V)]
    return parts


tot_hom = tot_g3 = tot_aff = tot_g2 = 0
mismatch = collisioni = 0
nonvuote = []
for label, V, Ei, Qi in VISTE:
    parts = carica(V)
    E, Q = parts[Ei], parts[Qi]
    assert n1(E, Q) == 36
    M = [[next(iter(E[j] & Q[c])) for c in range(6)] for j in range(6)]
    nv = 0
    for c1, c2 in combinations(range(6), 2):
        A = [M[j][c1] for j in range(6)]
        B0 = [M[j][c2] for j in range(6)]
        # G per VALORI (pairing-indipendente)
        G = set()
        for TA in combinations(A, 3):
            for TB in combinations(B0, 3):
                if (sum(TA) == sum(TB) and
                        sum(v * v for v in TA) == sum(v * v for v in TB)):
                    G.add((frozenset(TA), frozenset(TB)))
        if G:
            nv += 1
        for perm in permutations(range(6)):
            q = [B0[perm[j]] for j in range(6)]
            # enumerazione COMPLETA omogenea
            hom = []
            for J in combinations(range(6), 3):
                if (sum(q[j] - A[j] for j in J) == 0 and
                        sum(q[j] ** 2 - A[j] ** 2 for j in J) == 0):
                    hom.append(J)
            # enumerazione COMPLETA affine
            aff = []
            for j1 in range(6):
                for j2 in range(6):
                    if j1 == j2:
                        continue
                    resto = [j for j in range(6) if j not in (j1, j2)]
                    for K in combinations(resto, 2):
                        if (q[j1] - A[j2]
                                + sum(q[j] - A[j] for j in K) == 0 and
                                q[j1] ** 2 - A[j2] ** 2
                                + sum(q[j] ** 2 - A[j] ** 2
                                      for j in K) == 0):
                            aff.append((j1, j2, K))
            # gemelle allineate sotto questo accoppiamento
            g3 = []
            g2 = []
            for (TA, TB) in G:
                posA = frozenset(j for j in range(6) if A[j] in TA)
                posB = frozenset(j for j in range(6) if q[j] in TB)
                k = len(posA & posB)
                if k == 3:
                    g3.append((TA, TB))
                elif k == 2:
                    g2.append((TA, TB))
            # phi_hom e phi_aff: immagini come multiset
            im_hom = [(frozenset(A[j] for j in J),
                       frozenset(q[j] for j in J)) for J in hom]
            im_aff = [(frozenset([A[j2]] + [A[j] for j in K]),
                       frozenset([q[j1]] + [q[j] for j in K]))
                      for (j1, j2, K) in aff]
            from collections import Counter as _C
            if _C(im_hom) != _C(g3) or _C(im_aff) != _C(g2):
                mismatch += 1
                P(f"  <<< MISMATCH {label} ({c1},{c2}) {perm}")
            if (len(set(im_hom)) != len(im_hom) or
                    len(set(im_aff)) != len(im_aff)):
                collisioni += 1
                P(f"  <<< COLLISIONE {label} ({c1},{c2}) {perm}")
            tot_hom += len(hom)
            tot_g3 += len(g3)
            tot_aff += len(aff)
            tot_g2 += len(g2)
    nonvuote.append((label, nv))
    P(f"  {label}: coppie non vuote {nv}")

ok = (tot_hom == 1008 and tot_g3 == 1008 and tot_aff == 9072 and
      tot_g2 == 9072 and mismatch == 0 and collisioni == 0 and
      [n for _, n in nonvuote] == [6, 7, 1])
P(f"\nVERDETTO 1a [base: 3 viste x 15 coppie x 720]: hom {tot_hom} "
  f"g3 {tot_g3} aff {tot_aff} g2 {tot_g2} mismatch {mismatch} "
  f"collisioni {collisioni} nonvuote {[n for _, n in nonvuote]}")
P("  ATTESI CENTRATI — terza implementazione concorde" if ok else
  "  <<< SCARTO DAGLI ATTESI: STOP, si verbalizza senza adattare")

with open(os.path.join(L, "terza-biunivocita.log"), "w",
          encoding="utf-8") as f:
    f.write("\n".join(OUT) + "\n")
