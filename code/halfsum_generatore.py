"""SEDUTA INVARIANTE 156x32 (coda, seduta 2) — Bersaglio 1: IL
GENERATORE DELL'HALF-SUM. MISURA, non teoria.

Oggetti (definizioni stampate prima di ogni calcolo):
 - half-split: sestina S di [1..N] con terna T: 2*somma(T) = s1(S) e
   2*sommaq(T) = s2(S); equivalente: S = T1 U T2 disgiunte con
   inv3(T1) = inv3(T2) (inv3 = (somma, somma quadrati));
 - quaterna: 4 terne di [1..N] MUTUAMENTE disgiunte a inv3 IDENTICO
   (il generatore: ogni quaterna da 3 coppie half-sum, 8.17).
Griglia: N = 14..24 TUTTI (pari e dispari): i dispari servono alla
faccia a N=23 e al primo-N esatto (scelta dichiarata qui).

FACCE PRE-SCRITTE:
 F1-a (bug-stop): quaterne in [1..22] = 0 — il censimento riscontrato
   ha 0 coppie half-sum in [1..22] e ogni quaterna ne genera 3: una
   quaterna a 22 e un BUG, STOP e verbale.
 F1-b: quaterne attese: 1 a N=23 (la quaterna d'oro, chiave (36,614))
   e 2 a N=24 (+ (39,689)); numeri diversi = dato nuovo coi membri.
 F1-c (relazione a-b): per N, split estendibili a quaterna vs no;
   esempi di half-split NON estendibili coi membri (descrittiva).
 F1-d: primo N di ogni oggetto coi membri (descrittiva).
Controllo per appartenenza: a N=24 le coppie generate dalle quaterne
(3 per quaterna) devono essere ESATTAMENTE le 6 coppie d'oro di
8.17, con |G|=4 e gemelle = le 2x2 meta (ricalcolo diretto qui).
Log: logs/halfsum-generatore.log
"""
import os
import time
from itertools import combinations
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


t0 = time.time()
prima_hs = None
prima_qt = None
riepilogo = []
qt_per_N = {}
for N in range(14, 25):
    gruppi = defaultdict(list)
    for T in combinations(range(1, N + 1), 3):
        gruppi[inv3(T)].append(T)
    split = []          # (chiave, T1, T2) non ordinate, disgiunte
    for k, lst in gruppi.items():
        if len(lst) < 2:
            continue
        for T1, T2 in combinations(lst, 2):
            if not (set(T1) & set(T2)):
                split.append((k, T1, T2))
    sest = defaultdict(list)   # sestina -> lista di split
    for k, T1, T2 in split:
        S = tuple(sorted(T1 + T2))
        sest[S].append((k, T1, T2))
    multi = {S: v for S, v in sest.items() if len(v) > 1}
    quaterne = []
    for k, lst in gruppi.items():
        if len(lst) < 4:
            continue
        for Q in combinations(lst, 4):
            if all(not (set(Q[i]) & set(Q[j]))
                   for i in range(4) for j in range(i + 1, 4)):
                quaterne.append((k, Q))
    qt_per_N[N] = quaterne
    # estendibilita degli split: esiste una quaterna della stessa
    # chiave che contiene {T1, T2}?
    qk = defaultdict(list)
    for k, Q in quaterne:
        qk[k].append(set(Q))
    est = 0
    non_est_esempi = []
    for k, T1, T2 in split:
        if any(T1 in Qs and T2 in Qs for Qs in qk.get(k, ())):
            est += 1
        elif len(non_est_esempi) < 3 and N == 24:
            non_est_esempi.append((k, T1, T2))
    riepilogo.append((N, len(sest), len(split), len(multi),
                      len(quaterne), est))
    if prima_hs is None and sest:
        prima_hs = (N, sorted(sest))
    if prima_qt is None and quaterne:
        prima_qt = (N, quaterne)
    if N in (22, 23, 24):
        P(f"N={N}: quaterne {len(quaterne)}"
          + ("".join(f"\n    chiave {k}: " + " ".join(str(list(T))
             for T in Q) for k, Q in quaterne) if quaterne else ""))
    if N == 24 and non_est_esempi:
        P("esempi di split NON estendibili a quaterna (N=24):")
        for k, T1, T2 in non_est_esempi:
            P(f"    chiave {k}: {list(T1)} | {list(T2)}")

P()
P("tabella per N: (half-split distinte, split totali, sestine con "
  "piu split, quaterne, split estendibili):")
for N, nh, ns, nm, nq, ne in riepilogo:
    P(f"  N={N}: half-split {nh}, split {ns}, multi-split {nm}, "
      f"quaterne {nq}, estendibili {ne}")
P()
P(f"F1-d primo N con half-split: "
  + (f"{prima_hs[0]}, {len(prima_hs[1])} membri: "
     f"{[list(S) for S in prima_hs[1][:10]]}"
     if prima_hs else "nessuno fino a 24"))
P(f"F1-d primo N con quaterna: "
  + (f"{prima_qt[0]}" if prima_qt else "nessuno fino a 24"))
P()

# facce a/b
q22 = len(qt_per_N[22])
q23 = len(qt_per_N[23])
q24 = len(qt_per_N[24])
P(f"FACCIA F1-a: quaterne in [1..22] = {q22} "
  + ("(0 atteso: coerente col censimento — nessun BUG)" if q22 == 0
     else "<<< BUG-STOP: quaterna dove il censimento dice zero "
     "coppie half-sum: si verbalizza senza interpretare"))
P(f"FACCIA F1-b: quaterne a 23 = {q23} (attesa 1), a 24 = {q24} "
  f"(attese 2)"
  + ("" if (q23, q24) == (1, 2) else " <<< NUMERO DIVERSO: dato "
     "nuovo, membri sopra"))
P()

# controllo per appartenenza a N=24: coppie generate = le 6 d'oro
ORO = [
    ((1, 2, 13, 17, 18, 21), (3, 6, 7, 11, 22, 23)),
    ((1, 3, 11, 17, 18, 22), (2, 6, 7, 13, 21, 23)),
    ((1, 6, 7, 17, 18, 23), (2, 3, 11, 13, 21, 22)),
    ((2, 3, 14, 18, 19, 22), (4, 7, 8, 12, 23, 24)),
    ((2, 4, 12, 18, 19, 23), (3, 7, 8, 14, 22, 24)),
    ((2, 7, 8, 18, 19, 24), (3, 4, 12, 14, 22, 23)),
]
gen = []
for k, Q in qt_per_N[24]:
    for (i, j) in ((0, 1), (0, 2), (0, 3)):
        resto = [x for x in range(4) if x not in (i, j)]
        A = tuple(sorted(Q[i] + Q[j]))
        B = tuple(sorted(Q[resto[0]] + Q[resto[1]]))
        gen.append((min(A, B), max(A, B)))
ok_ins = Counter(gen) == Counter((min(a, b), max(a, b))
                                 for a, b in ORO)
P(f"coppie generate dalle quaterne di N=24: {len(gen)}; "
  f"= le 6 coppie d'oro di 8.17? {ok_ins}")
gver = 0
for A, B in gen:
    gA = defaultdict(int)
    for T in combinations(A, 3):
        gA[inv3(T)] += 1
    g = 0
    for T in combinations(B, 3):
        g += gA.get(inv3(T), 0)
    if g == 4:
        gver += 1
P(f"ricalcolo |G| diretto sulle 6 generate: |G|=4 in {gver}/6")
P()
P(f"VERDETTO B1: quaterne (4 terne disgiunte a inv3 identico): "
  f"{q22} in [1..22], {q23} in [1..23], {q24} in [1..24]; coppie "
  f"generate a 24: {len(gen)} (= oro: {ok_ins}); half-split ed "
  f"estendibilita: tabella sopra.")
P(f"[{time.time()-t0:.1f}s]")

with open(os.path.join(LOGS, "halfsum-generatore.log"), "w",
          encoding="utf-8") as f:
    f.write("\n".join(OUT) + "\n")
