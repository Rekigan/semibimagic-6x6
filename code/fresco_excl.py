"""Il test decisivo post-falsificazione: EXCL sulle coppie fresche a
|G| = 4 (dove il Teorema G tace).

FACCIA PRE-SCRITTA: se UN accoppiamento di una coppia |G|=4 da
N3 > 0 e N2 > 0 insieme, EXCL e FALSIFICATA IN GENERALE (resta il
teorema-per-ambiente via |G|<=2); se nessuno dei 720 x coppie lo da,
EXCL sopravvive OLTRE il Teorema G e serve un teorema piu forte.

Base: tutte le coppie disgiunte same-bucket di [1..N], N=14..22 pari,
con |G| >= 3 (le violazioni del vaglio fresco). Sweep esaustivo 720.
Log: logs/fresco-excl.log
"""
import os
from itertools import combinations, permutations
from collections import Counter, defaultdict

L = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "logs")
OUT = []


def P(msg=""):
    OUT.append(msg)
    print(msg, flush=True)


P(__doc__)

viol_pairs = []
for N in range(14, 23, 2):
    bucket = defaultdict(list)
    for S in combinations(range(1, N + 1), 6):
        bucket[(sum(S), sum(v * v for v in S))].append(frozenset(S))
    for k, lst in bucket.items():
        if len(lst) < 2:
            continue
        for A, B in combinations(lst, 2):
            if A & B:
                continue
            G = []
            for TA in combinations(sorted(A), 3):
                for TB in combinations(sorted(B), 3):
                    if (sum(TA) == sum(TB) and
                            sum(v * v for v in TA)
                            == sum(v * v for v in TB)):
                        G.append((frozenset(TA), frozenset(TB)))
            if len(G) > 2:
                viol_pairs.append((N, sorted(A), sorted(B), G))

# dedup per (A,B) attraverso gli N (la stessa coppia riappare a N piu alti)
visti = set()
unici = []
for N, A, B, G in viol_pairs:
    k = (tuple(A), tuple(B))
    if k not in visti:
        visti.add(k)
        unici.append((N, A, B, G))
P(f"coppie |G|>2 uniche: {len(unici)} [dedup su N=14..22]")

miste = 0
dist = Counter()
for N, A, B, G in unici:
    Al = list(A)
    Bl = list(B)
    for perm in permutations(range(6)):
        q = [Bl[perm[j]] for j in range(6)]
        N3 = N2 = 0
        for (Ta, Tb) in G:
            posA = frozenset(j for j in range(6) if Al[j] in Ta)
            posB = frozenset(j for j in range(6) if q[j] in Tb)
            k = len(posA & posB)
            if k == 3:
                N3 += 1
            elif k == 2:
                N2 += 1
        dist[(N3 > 0, N2 > 0)] += 1
        if N3 > 0 and N2 > 0 and miste < 3:
            P(f"  <<< MISTA: A={Al} B={Bl} perm={perm} N3={N3} N2={N2}"
              f" — EXCL FALSIFICATA IN GENERALE")
        if N3 > 0 and N2 > 0:
            miste += 1

P(f"\nVERDETTO [base: {len(unici)} coppie x 720 accoppiamenti "
  f"esaustivi]: distribuzione {dict(dist)}")
P(f"  accoppiamenti MISTI: {miste} — "
  + ("EXCL FALSIFICATA IN GENERALE (resta teorema-per-ambiente)"
     if miste else "EXCL SOPRAVVIVE anche a |G|=4: serve un teorema "
     "piu forte del Teorema G"))

with open(os.path.join(L, "fresco-excl.log"), "w",
          encoding="utf-8") as f:
    f.write("\n".join(OUT) + "\n")
