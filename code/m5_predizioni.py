"""FINESTRA (d,e) — seduta M5: dati, shuffle-test, predizione-prima.

PREDIZIONI PRE-REGISTRATE (stampate PRIMA di ogni calcolo):
 P1 (shuffle, punto 3 reviewer): permutando la colonna q fra le righe
    (tutte le 120 permutazioni a riga-0 fissa — deterministico), le
    coppie MISTE (omogeneo E affine risolubili) COMPAIONO: nulla di
    combinatorio vieta la coesistenza; l esclusione reale e aritmetica
    dell accoppiamento vero.
 P2 (predizione-prima, punto 4 reviewer; condizione C = claim 21
    promosso a legge): sui mondi MAI censiti a mosse — le due sorelle
    di max=43 e i 7 quadrati pre-hub di max=44 (tutti senza hub:
    matching, dai gradi della corsa hub-hunt) — l enumeratore trovera:
    SAT congiunti = 0 e FRA congiunti = 0 SU OGNI VISTA, con lin-sat
    abbondanti (10-50 per vista). Se un SAT o FRA compare: C e
    falsificata e si dichiara FORTE.

 Parte 0: membri (d, s) dei fratelli e satelliti noti (dati, non
    teoria). Basi dichiarate. Log: logs/m5-predizioni.log
"""
import os, sys
from itertools import combinations, permutations
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


P(__doc__)


def hom_aff(pj, qj):
    """Risolubilita dei due sistemi sui sei (p, q)."""
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


def vista_M(parts, Ei, Qi):
    E, Q = parts[Ei], parts[Qi]
    return [[next(iter(E[j] & Q[c])) for c in range(6)]
            for j in range(6)]


def carica(V):
    s1 = sum(V) // 6
    s2 = sum(v * v for v in V) // 6
    subs = find_subsets(V, 6, s1, s2)
    parts = [tuple(sorted((frozenset(x) for x in p), key=min))
             for p in gp(subs, V)]
    orth = [(i, j) for i in range(len(parts))
            for j in range(i + 1, len(parts))
            if n1(parts[i], parts[j]) == 36]
    return s1, s2, parts, orth


# ---- Parte 0: membri (d, s) dei sistemi risolti (dati)
PF = [[6, 42, 29, 3, 40, 30], [8, 44, 47, 21, 20, 10],
      [33, 31, 41, 37, 1, 7], [19, 17, 13, 9, 43, 49],
      [36, 2, 5, 35, 34, 38], [48, 14, 15, 45, 12, 16]]
V_pf = sorted(v for r in PF for v in r)
s1, s2, parts, orth = carica(V_pf)
P("\nParte 0a — fratelli di pfeffermann, vista E=70 Q=2 [membri (d,s) "
  "delle terne risolventi; base per-coppia]:")
M = vista_M(parts, 70, 2)
for c1, c2 in combinations(range(6), 2):
    pj = [M[j][c1] for j in range(6)]
    qj = [M[j][c2] for j in range(6)]
    dj = [qj[j] - pj[j] for j in range(6)]
    sj = [qj[j] + pj[j] for j in range(6)]
    for J in combinations(range(6), 3):
        if (sum(dj[j] for j in J) == 0 and
                sum(dj[j] * sj[j] for j in J) == 0):
            P(f"  colonne ({c1},{c2}) terna {J}: "
              f"d {[dj[j] for j in J]} s {[sj[j] for j in J]}")
V42 = sorted(v for v in range(1, 43) if v not in {19, 20, 21, 22, 23, 24})
s1, s2, parts, orth = carica(V42)
P("Parte 0b — satelliti di 3799, vista E=38 Q=0 [membri (delta, sigma) "
  "+ K; base per-coppia]:")
M = vista_M(parts, 38, 0)
for c1, c2 in combinations(range(6), 2):
    pj = [M[j][c1] for j in range(6)]
    qj = [M[j][c2] for j in range(6)]
    dj = [qj[j] - pj[j] for j in range(6)]
    sj = [qj[j] + pj[j] for j in range(6)]
    for j1 in range(6):
        for j2 in range(6):
            if j1 == j2:
                continue
            resto = [j for j in range(6) if j not in (j1, j2)]
            for K in combinations(resto, 2):
                if (qj[j1] - pj[j2] + sum(dj[j] for j in K) == 0 and
                        qj[j1] ** 2 - pj[j2] ** 2
                        + sum(dj[j] * sj[j] for j in K) == 0):
                    P(f"  colonne ({c1},{c2}) misto ({j1},{j2}) K={K}: "
                      f"delta {qj[j1]-pj[j2]} sigma {qj[j1]+pj[j2]} "
                      f"dK {[dj[j] for j in K]} sK {[sj[j] for j in K]}")

# ---- Parte 1: shuffle-test (P1)
P("\nParte 1 — shuffle esaustivo (120 permutazioni a riga-0 fissa) "
  "[base: 15 coppie x 2 viste campione]:")
CAMPIONI = [("3799 E=38 Q=0 (A)", V42, 38, 0),
            ("pfeffermann E=70 Q=2 (B)", V_pf, 70, 2)]
for label, V, Ei, Qi in CAMPIONI:
    s1, s2, parts, orth = carica(V)
    M = vista_M(parts, Ei, Qi)
    tot = Counter()
    for c1, c2 in combinations(range(6), 2):
        pj = [M[j][c1] for j in range(6)]
        qj = [M[j][c2] for j in range(6)]
        for perm in permutations(range(1, 6)):
            pi = (0,) + perm
            q2 = [qj[pi[j]] for j in range(6)]
            h, a = hom_aff(pj, q2)
            tot[(h, a)] += 1
    P(f"  {label}: {{(hom,aff): conteggio}} = "
      f"{ {k: v for k, v in sorted(tot.items())} }  "
      f"MISTE {tot[(True, True)]}"
      + ("  -> P1 CONFERMATA (la coesistenza e' combinatoriamente "
         "lecita)" if tot[(True, True)] else "  -> P1 FALSIFICATA"))

# ---- Parte 2: predizione-prima sui mondi nuovi (P2)
P("\nParte 2 — l enumeratore DOPO la predizione [base per-vista]:")
NUOVI = [
    ("sorella-3659 (max43)", sorted(v for v in range(1, 44)
     if v not in {4, 11, 18, 22, 26, 33, 40})),
    ("sorella-3691 (max43)", sorted(v for v in range(1, 44)
     if v not in {10, 11, 12, 22, 32, 33, 34})),
    ("m44-a", sorted(v for v in range(1, 45)
     if v not in {2, 7, 10, 21, 24, 35, 38, 43})),
    ("m44-b", sorted(v for v in range(1, 45)
     if v not in {2, 10, 12, 14, 31, 33, 35, 43})),
    ("m44-c", sorted(v for v in range(1, 45)
     if v not in {2, 19, 21, 22, 23, 24, 26, 43})),
    ("m44-d", sorted(v for v in range(1, 45)
     if v not in {4, 11, 15, 19, 26, 30, 34, 41})),
    ("m44-e", sorted(v for v in range(1, 45)
     if v not in {4, 11, 18, 22, 23, 27, 34, 41})),
    ("m44-f", sorted(v for v in range(1, 45)
     if v not in {7, 8, 15, 22, 23, 30, 37, 38})),
    ("m44-g", sorted(v for v in range(1, 45)
     if v not in {10, 11, 12, 22, 23, 33, 34, 35})),
]
esiti_C = []
for label, V in NUOVI:
    s1, s2, parts, orth = carica(V)
    for (a, b) in orth:
        for (Ei, Qi) in ((a, b), (b, a)):
            E, Q = parts[Ei], parts[Qi]
            sat = fra = linsat = 0
            for c1, c2 in combinations(range(6), 2):
                T = sorted(Q[c1] | Q[c2])
                anchor = T[0]
                rest = [v for v in T if v != anchor]
                Tset = set(T)
                for comb in combinations(rest, 5):
                    A = frozenset((anchor,) + comb)
                    if sum(A) != s1:
                        continue
                    B = frozenset(Tset - A)
                    if {A, B} == {Q[c1], Q[c2]}:
                        continue
                    pat = tuple(sorted((len(A & E[j]) for j in range(6)),
                                       reverse=True))
                    quad = sum(v * v for v in A) == s2
                    if pat == (2, 1, 1, 1, 1, 0):
                        linsat += 1
                        if quad:
                            sat += 1
                    elif pat == (1, 1, 1, 1, 1, 1) and quad:
                        fra += 1
            ok = (sat == 0 and fra == 0)
            esiti_C.append(ok)
            P(f"  {label} E={Ei} Q={Qi}: SAT {sat} FRA {fra} "
              f"lin-sat {linsat}"
              + ("" if ok else "  <<< C FALSIFICATA QUI"))
P(f"\nVerdetto C [base: {len(esiti_C)} viste nuove]: "
  f"{'CONFERMATA su tutte' if all(esiti_C) else 'FALSIFICATA'} — "
  f"il calcolo ha tentato di smentire una regola gia formulata.")

with open(os.path.join(L, "m5-predizioni.log"), "w",
          encoding="utf-8") as f:
    f.write("\n".join(OUT) + "\n")
