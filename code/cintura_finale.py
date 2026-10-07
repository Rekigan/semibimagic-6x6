"""SEDUTA INVARIANTE 156x32 (coda, seduta 2) — Bersaglio 5: CINTURA.
(a) tabella fine MISURATA sulle 6 coppie half-sum di N=24 (verifica
empirica completa del vettore (k, 3-k, 3-k, k)); (b) le coppie
|G|=2 di N=24: gemelle SEMPRE complementari? MISURA, non teoria.

FACCE PRE-SCRITTE:
 B5-a: attesa per OGNUNA delle 6: tabella (kg,kh) ANTI-DIAGONALE
   {(3,0): 36, (2,1): 324, (1,2): 324, (0,3): 36}, uguale al modello
   del Bersaglio 3, e vettori k sempre della forma (k, 3-k, 3-k, k);
   una cella fuori anti-diagonale o conteggi diversi = STOP e
   verbale coi membri.
 B5-b: attesa 0 violazioni di complementarita sulle coppie |G|=2 di
   [1..24] (attese 11.158 dal censimento riscontrato); UNA
   violazione = BUG del censimento: STOP e verbale coi membri.
Log: logs/cintura-finale.log
"""
import os
import time
from itertools import combinations, permutations
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
LOGS = os.path.join(HERE, "..", "logs")
OUT = []


def P(msg=""):
    OUT.append(msg)
    print(msg, flush=True)


P(__doc__)


def inv3(T):
    return (T[0] + T[1] + T[2], T[0] * T[0] + T[1] * T[1] + T[2] * T[2])


def comp(S, T):
    return tuple(v for v in S if v not in T)


# (a) le 6 d'oro (membri di 8.17), gemelle ricalcolate qui
ORO = [
    ((1, 2, 13, 17, 18, 21), (3, 6, 7, 11, 22, 23)),
    ((1, 3, 11, 17, 18, 22), (2, 6, 7, 13, 21, 23)),
    ((1, 6, 7, 17, 18, 23), (2, 3, 11, 13, 21, 22)),
    ((2, 3, 14, 18, 19, 22), (4, 7, 8, 12, 23, 24)),
    ((2, 4, 12, 18, 19, 23), (3, 7, 8, 14, 22, 24)),
    ((2, 7, 8, 18, 19, 24), (3, 4, 12, 14, 22, 23)),
]
ATTESA = {(3, 0): 36, (2, 1): 324, (1, 2): 324, (0, 3): 36}

P("=" * 68)
P("B5-a — TABELLA FINE MISURATA SULLE 6 HALF-SUM DI N=24")
P("=" * 68)
t0 = time.time()
stop_a = 0
for A, B in ORO:
    gem = [(TA, TB) for TA in combinations(A, 3)
           for TB in combinations(B, 3) if inv3(TA) == inv3(TB)]
    gemS = sorted(gem)
    g0 = gemS[0]
    g0b = (comp(A, g0[0]), comp(B, g0[1]))
    resto = [x for x in gemS if x != g0 and x != g0b]
    h0 = resto[0]
    h0b = (comp(A, h0[0]), comp(B, h0[1]))
    ordg = [g0, g0b, h0, h0b]
    Al = list(A)
    TAs = [set(t[0]) for t in ordg]
    TBs = [set(t[1]) for t in ordg]
    tab = Counter()
    forma_viol = 0
    for q in permutations(B):
        ks = []
        for i in range(4):
            ks.append(sum(1 for j in range(6)
                          if Al[j] in TAs[i] and q[j] in TBs[i]))
        if not (ks[1] == ks[0] and ks[2] == 3 - ks[0]
                and ks[3] == ks[2]):
            forma_viol += 1
        tab[(ks[0], ks[2])] += 1
    ok = (Counter(tab) == Counter(ATTESA) and forma_viol == 0)
    if not ok:
        stop_a += 1
    P(f"A={list(A)} B={list(B)}: |G|={len(gem)}, vettori fuori "
      f"forma (k,3-k,3-k,k): {forma_viol}, tabella "
      f"{dict(sorted(tab.items()))} "
      + ("OK" if ok else "<<< STOP: DIVERSA DALL'ATTESA"))
P(f"FACCIA B5-a: " + ("6/6 tabelle = anti-diagonale del modello, "
  "vettori sempre (k,3-k,3-k,k): verifica empirica completa"
  if stop_a == 0 else f"<<< {stop_a} coppie fuori attesa: STOP"))
P(f"[{time.time()-t0:.1f}s]")
P()

# (b) complementarita sulle |G|=2 di [1..24]
P("=" * 68)
P("B5-b — COMPLEMENTARITA SULLE COPPIE |G|=2 DI [1..24]")
P("=" * 68)
t0 = time.time()
bucket = defaultdict(list)
for S in combinations(range(1, 25), 6):
    bucket[(sum(S), sum(v * v for v in S))].append(S)
n2 = 0
viol = 0
for key in sorted(bucket):
    lst = bucket[key]
    if len(lst) < 2:
        continue
    tri = {}
    for S in lst:
        d = defaultdict(list)
        for T in combinations(S, 3):
            d[inv3(T)].append(T)
        tri[S] = d
    for A, B in combinations(lst, 2):
        if set(A) & set(B):
            continue
        dA = tri[A]
        dB = tri[B]
        gem = []
        for kk, TAs in dA.items():
            TBs = dB.get(kk)
            if TBs:
                for TA in TAs:
                    for TB in TBs:
                        gem.append((TA, TB))
        if len(gem) == 2:
            n2 += 1
            T1, U1 = gem[0]
            T2, U2 = gem[1]
            if not (T2 == comp(A, T1) and U2 == comp(B, U1)):
                viol += 1
                P(f"  <<< NON COMPLEMENTARI: {key} A={list(A)} "
                  f"B={list(B)} gemelle {gem}")
P(f"coppie |G|=2 di [1..24]: {n2} (attese 11158)")
P(f"FACCIA B5-b: violazioni di complementarita: {viol} "
  + ("(0 attese: teorema di complementazione confermato per "
     "appartenenza su tutta la base)" if viol == 0 else
     "<<< BUG DEL CENSIMENTO: STOP"))
P(f"[{time.time()-t0:.0f}s]")
P()
P("VERDETTO B5: vedi facce sopra.")

with open(os.path.join(LOGS, "cintura-finale.log"), "w",
          encoding="utf-8") as f:
    f.write("\n".join(OUT) + "\n")
