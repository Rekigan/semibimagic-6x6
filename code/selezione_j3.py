"""Seduta SELEZIONE, prima pietra — Lemma J3 e i sistemi gemelli.

LEMMA J3 (derivato in seduta): per una mossa-fratello su una coppia di
colonne, J = {righe che prendono q} e' FORZATO a |J| = 3.
(|J|=1,5: meta' = colonna, vietato dalla definizione di mossa;
|J|=2: Sd=0 e Se=0 con e=d(p+q) forzano q_i=p_j e p_i=q_j — entrate
ripetute, vietato; |J|=4 = complemento di 2.)

CHECK: (a) per TUTTI i fratelli di Pfeffermann e Boyer (dedup per
mossa), |J| stampato — atteso {3}; (b) dicotomia a livello di
COPPIA-DI-COLONNE sulle viste fertili (tipo A + orfani) e tipo B:
nessuna coppia di colonne ospita sia una soluzione satellite sia una
fratello. Basi: per-vista e per-coppia. Log: logs/selezione-j3.log
"""
import os, sys
from itertools import combinations
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from semibimagic import find_subsets, partitions as gp

L = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "logs")
OUT = []


def P(msg=""):
    OUT.append(msg)
    print(msg, flush=True)


def n1(A, B):
    return sum(1 for a in A for b in B if len(a & b) == 1)


PF = [[6, 42, 29, 3, 40, 30], [8, 44, 47, 21, 20, 10],
      [33, 31, 41, 37, 1, 7], [19, 17, 13, 9, 43, 49],
      [36, 2, 5, 35, 34, 38], [48, 14, 15, 45, 12, 16]]
BOYER = [[41, 35, 6, 2, 37, 47], [5, 42, 33, 39, 46, 3],
         [38, 7, 45, 43, 1, 34], [22, 55, 13, 11, 49, 18],
         [53, 10, 17, 23, 14, 51], [9, 19, 54, 50, 21, 15]]
W648 = [[23, 82, 151, 190, 109, 93], [99, 75, 135, 159, 166, 14],
        [90, 215, 102, 39, 97, 105], [111, 119, 177, 114, 1, 126],
        [202, 50, 57, 81, 141, 117], [123, 107, 26, 65, 134, 193]]
M330 = [[9, 83, 105, 84, 15, 34], [27, 101, 26, 5, 76, 95],
        [109, 78, 28, 13, 17, 85], [32, 1, 97, 82, 25, 93],
        [54, 11, 67, 103, 91, 4], [99, 56, 7, 43, 106, 19]]

MONDI = [
    ("3799", sorted(v for v in range(1, 43)
                    if v not in {19, 20, 21, 22, 23, 24})),
    ("3659", sorted(v for v in range(1, 43)
                    if v not in {4, 11, 18, 25, 32, 39})),
    ("hub-44", sorted(v for v in range(1, 45)
                      if v not in {13, 20, 21, 22, 23, 24, 25, 32})),
    ("pfeffermann", sorted(v for r in PF for v in r)),
    ("boyer", sorted(v for r in BOYER for v in r)),
    ("wroblewski-648", sorted(v for r in W648 for v in r)),
    ("morgenstern-330", sorted(v for r in M330 for v in r)),
]

Jsz = Counter()
coppie_miste = 0
n_cp = 0
for label, V in MONDI:
    s1 = sum(V) // 6
    s2 = sum(v * v for v in V) // 6
    subs = find_subsets(V, 6, s1, s2)
    parts = [tuple(sorted((frozenset(x) for x in p), key=min))
             for p in gp(subs, V)]
    orth = [(i, j) for i in range(len(parts))
            for j in range(i + 1, len(parts))
            if n1(parts[i], parts[j]) == 36]
    for (a, b) in orth:
        for (Ei, Qi) in ((a, b), (b, a)):
            E, Q = parts[Ei], parts[Qi]
            M = [[next(iter(E[j] & Q[c])) for c in range(6)]
                 for j in range(6)]
            for c1, c2 in combinations(range(6), 2):
                pj = [M[j][c1] for j in range(6)]
                qj = [M[j][c2] for j in range(6)]
                n_cp += 1
                fra_here = []
                # fratelli: J proprio, somma e quadratica nulle
                for r in range(1, 6):
                    for J in combinations(range(6), r):
                        if (sum(qj[j] - pj[j] for j in J) == 0 and
                                sum(qj[j] ** 2 - pj[j] ** 2
                                    for j in J) == 0):
                            fra_here.append(J)
                for J in fra_here:
                    Jsz[len(J)] += 1
                # satelliti congiunti su questa coppia
                sat_here = 0
                for j1 in range(6):
                    for j2 in range(6):
                        if j1 == j2:
                            continue
                        resto = [j for j in range(6)
                                 if j not in (j1, j2)]
                        for J in combinations(resto, 2):
                            d = (qj[j1] - pj[j2]
                                 + sum(pj[j] - qj[j] for j in J))
                            if d != 0:
                                continue
                            dq = (qj[j1] ** 2 - pj[j2] ** 2
                                  + sum(pj[j] ** 2 - qj[j] ** 2
                                        for j in J))
                            if dq == 0:
                                sat_here += 1
                if fra_here and sat_here:
                    coppie_miste += 1
                    P(f"  <<< COPPIA MISTA a {label} E={Ei} Q={Qi} "
                      f"colonne ({c1},{c2}): fratelli {fra_here} e "
                      f"satelliti {sat_here}")

P(f"\nLemma J3 [base: tutte le coppie di colonne di tutte le viste "
  f"dei 7 mondi, {n_cp} coppie]: taglie |J| dei fratelli trovati: "
  f"{dict(sorted(Jsz.items()))} (attesa: solo 3; il conteggio e' "
  f"per-vista e per-coppia, ogni mossa appare in piu' viste)")
P(f"Dicotomia a livello di coppia-di-colonne: coppie miste "
  f"(fratello E satellite sulla stessa coppia): {coppie_miste}")

with open(os.path.join(L, "selezione-j3.log"), "w",
          encoding="utf-8") as f:
    f.write("\n".join(OUT) + "\n")
