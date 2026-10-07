"""SEDUTA INVARIANTE 156x32 (coda, seduta 2) — Bersaglio 2: SALITA A
N=26 col floor-check PRE-DISEGNO. MISURA, non teoria.

FASE A (floor-check, stampato PRIMA del disegno della fase B):
- costo del censimento MISURATO con questo stesso codice a N=22 e
  N=24; C(26,6) esatto; proiezione coppie e tempo dai rapporti
  misurati QUI (mai ereditati); CAP DERIVATO = 3 x tempo proiettato
  (fattore di sicurezza 3, dichiarato); BUDGET di seduta per B2:
  900 s, dichiarato qui prima della misura. GO se CAP <= BUDGET.

FASE B (solo se GO):
- censimento completo a N=26: distribuzione |G| su tutte le coppie
  disgiunte same-bucket;
- coppie |G|=4 NUOVE (non presenti a N=24, ricostruito in fase A),
  classificate per FORMA d'incidenza canonica congiunta:
  TRASVERSALE (riferimento: calcolato in-run su una coppia delle 156)
  / HALF-SUM (riferimento: in-run su una coppia d'oro) / ALTRA;
- firma su 720 per OGNI nuova; quaterne a N=25 e N=26 (generatore
  di B1, ricalcolato qui) e incrocio con le half-sum nuove.

FACCE PRE-SCRITTE:
 B2-a: |G| > 4, se compare, e dato NUOVO: membri e gemelle a
       verbale; se non compare, si verbalizza il tetto 4 fino a 26.
 B2-b: una forma d'incidenza TERZA = dato d'oro coi membri; attese
       dal quadro: solo trasversale e half-sum.
 B2-c (STOP): firma diversa DENTRO una forma nota = falsifica della
       funzione-incidenza (8.17): STOP e verbale coi membri.
 B2-d: half-sum nuove: TUTTE generate da quaterne? attesa dal
       generatore (B1): si, 3 coppie per quaterna; deviazione =
       dato nuovo coi membri.
Log: logs/salita-n26.log
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


def censimento(N):
    """Ritorna (nsest, ncoppie, dist_G, q4, qx) con qx = |G|>4."""
    bucket = defaultdict(list)
    for S in combinations(range(1, N + 1), 6):
        bucket[(sum(S), sum(v * v for v in S))].append(S)
    nsest = sum(len(v) for v in bucket.values())
    dist = Counter()
    npairs = 0
    q4 = []
    qx = []
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
            npairs += 1
            dA = tri[A]
            dB = tri[B]
            g = 0
            for kk, TAs in dA.items():
                TBs = dB.get(kk)
                if TBs:
                    g += len(TAs) * len(TBs)
            dist[g] += 1
            if g >= 4:
                gem = []
                for kk, TAs in dA.items():
                    TBs = dB.get(kk)
                    if TBs:
                        for TA in TAs:
                            for TB in TBs:
                                gem.append((TA, TB))
                (q4 if g == 4 else qx).append((key, A, B, gem))
    return nsest, npairs, dist, q4, qx


# ------------------------------------------------------------------
P("=" * 68)
P("FASE A — FLOOR-CHECK (prima del disegno)")
P("=" * 68)
mis = {}
for N in (22, 24):
    t0 = time.time()
    nsest, npairs, dist, q4, qx = censimento(N)
    dt = time.time() - t0
    mis[N] = (nsest, npairs, dt, q4, qx)
    P(f"  N={N}: sestine {nsest}, coppie {npairs}, |G|=4: {len(q4)}, "
      f"|G|>4: {len(qx)}, tempo {dt:.1f}s")

c266 = 1
for i in range(6):
    c266 = c266 * (26 - i) // (i + 1)
r_c = mis[24][1] / mis[22][1]
r_t = mis[24][2] / max(0.001, mis[22][2])
proj_c = mis[24][1] * r_c
proj_t = mis[24][2] * r_t
CAP = 3 * proj_t
BUDGET = 900.0
P(f"C(26,6) esatto = {c266}")
P(f"rapporti misurati 22->24: coppie x{r_c:.2f}, tempo x{r_t:.2f}")
P(f"proiezione N=26: ~{proj_c:.0f} coppie, ~{proj_t:.0f}s")
P(f"CAP DERIVATO = 3 x {proj_t:.0f}s = {CAP:.0f}s; BUDGET = "
  f"{BUDGET:.0f}s")
GO = CAP <= BUDGET
P(f"DECISIONE (prima della fase B): {'GO' if GO else 'NON APERTO'}")
P()

if not GO:
    P("FASE B NON APERTA: numeri del floor-check a verbale.")
else:
    P("=" * 68)
    P("FASE B — CENSIMENTO N=26, FORME E FIRME DELLE NUOVE")
    P("=" * 68)
    t0 = time.time()
    nsest, npairs, dist, q4_26, qx_26 = censimento(26)
    P(f"N=26: sestine {nsest} (atteso {c266}), coppie {npairs}")
    P(f"distribuzione |G|: {dict(sorted(dist.items()))}  "
      f"[censimento: {time.time()-t0:.0f}s]")
    P("FACCIA B2-a: " + (f"|G| > 4 COMPARE: {len(qx_26)} coppie, "
      "membri e gemelle sotto (dato nuovo)" if qx_26 else
      "|G| <= 4 anche a 26: tetto 4 confermato fin qui"))
    for key, A, B, gem in qx_26:
        P(f"  |G|={len(gem)} {key} A={list(A)} B={list(B)}")
        for TA, TB in sorted(gem):
            P(f"      {list(TA)} / {list(TB)}  inv {inv3(TA)}")
    P()

    def comp(S, T):
        return tuple(v for v in S if v not in T)

    def canon_joint(MA, MB):
        best = None
        for p in permutations(range(4)):
            t = (tuple(tuple(MA[p[i]][p[j]] for j in range(4))
                       for i in range(4)),
                 tuple(tuple(MB[p[i]][p[j]] for j in range(4))
                       for i in range(4)))
            if best is None or t < best:
                best = t
        return best

    def carta(key, A, B, gem):
        gemS = sorted(gem)
        g0 = gemS[0]
        g0b = (comp(A, g0[0]), comp(B, g0[1]))
        resto = [x for x in gemS if x != g0 and x != g0b]
        h0 = resto[0]
        h0b = (comp(A, h0[0]), comp(B, h0[1]))
        ordg = [g0, g0b, h0, h0b]
        MA = [[len(set(ordg[i][0]) & set(ordg[j][0]))
               for j in range(4)] for i in range(4)]
        MB = [[len(set(ordg[i][1]) & set(ordg[j][1]))
               for j in range(4)] for i in range(4)]
        return ordg, canon_joint(MA, MB)

    def firma720(A, B, ordg):
        Al = list(A)
        TAs = [set(t[0]) for t in ordg]
        TBs = [set(t[1]) for t in ordg]
        cnt = Counter()
        for q in permutations(B):
            n3 = n2 = 0
            for i in range(4):
                k = 0
                for j in range(6):
                    if Al[j] in TAs[i] and q[j] in TBs[i]:
                        k += 1
                if k == 3:
                    n3 += 1
                elif k == 2:
                    n2 += 1
            if n3 and n2:
                cnt["misto"] += 1
            elif n3:
                cnt["solo-N3"] += 1
            elif n2:
                cnt["solo-N2"] += 1
            else:
                cnt["nullo"] += 1
        return cnt

    # riferimenti in-run: forma T da una trasversale delle 156,
    # forma H da una coppia d'oro (entrambe dal censimento 24)
    ORO1 = ((1, 2, 13, 17, 18, 21), (3, 6, 7, 11, 22, 23))
    FT = FH = None
    for key, A, B, gem in mis[24][3]:
        cj = carta(key, A, B, gem)[1]
        if (A, B) == ORO1:
            FH = cj
        elif FT is None:
            FT = cj
        if FT and FH:
            break
    P(f"riferimenti in-run: forma T e H calcolate "
      f"(H dalla coppia d'oro {list(ORO1[0])}/{list(ORO1[1])})")
    FIRMA_T = Counter({"solo-N2": 488, "nullo": 160, "solo-N3": 40,
                       "misto": 32})
    FIRMA_H = Counter({"solo-N2": 648, "solo-N3": 72})

    vecchie = {frozenset((A, B)) for key, A, B, gem in mis[24][3]}
    nuove = [x for x in q4_26 if frozenset((x[1], x[2]))
             not in vecchie]
    P(f"coppie |G|=4 a 26: {len(q4_26)}; ritrovate di N=24: "
      f"{len(q4_26) - len(nuove)} (attese {len(mis[24][3])}); "
      f"NUOVE: {len(nuove)}")
    P()
    t0 = time.time()
    forme = Counter()
    stop_c = 0
    terze = []
    hs_nuove = []
    righe = []
    for key, A, B, gem in nuove:
        ordg, cj = carta(key, A, B, gem)
        cnt = firma720(A, B, ordg)
        righe.append((key, A, B,
                      "T" if cj == FT else "H" if cj == FH else "X"))
        if cj == FT:
            forme["trasversale"] += 1
            if cnt != FIRMA_T:
                stop_c += 1
                P(f"  <<< STOP B2-c: firma {dict(cnt)} su TRASVERSALE "
                  f"{key} A={list(A)} B={list(B)}")
        elif cj == FH:
            forme["half-sum"] += 1
            hs_nuove.append((key, A, B))
            if cnt != FIRMA_H:
                stop_c += 1
                P(f"  <<< STOP B2-c: firma {dict(cnt)} su HALF-SUM "
                  f"{key} A={list(A)} B={list(B)}")
        else:
            forme["ALTRA"] += 1
            terze.append((key, A, B, cj, dict(cnt)))
            P(f"  <<< FORMA TERZA (B2-b, dato d'oro): {key} "
              f"A={list(A)} B={list(B)} firma {dict(cnt)}")
            P(f"      lato A: {cj[0]}")
            P(f"      lato B: {cj[1]}")
    P(f"classificazione delle {len(nuove)} nuove per forma: "
      f"{dict(forme)}  [{time.time()-t0:.0f}s]")
    P("FACCIA B2-b: " + ("solo trasversale e half-sum (nessuna "
      "terza forma fino a 26)" if not terze else
      f"<<< {len(terze)} coppie di forma TERZA: membri sopra"))
    P("FACCIA B2-c: " + ("firma = funzione della forma su tutte le "
      "nuove (0 deviazioni)" if stop_c == 0 else
      f"<<< {stop_c} deviazioni: STOP, membri sopra"))
    P()
    P("half-sum nuove coi membri:")
    for key, A, B in hs_nuove:
        P(f"  {key} A={list(A)} B={list(B)}")
    P()
    P("base completa delle nuove coi membri (forma T/H/X):")
    for i, (key, A, B, f_) in enumerate(righe, 1):
        P(f"  [{i:3d}] {f_} {key} A={list(A)} B={list(B)}")
    # quaterne a 25 e 26 e incrocio (B2-d)
    for NN in (25, 26):
        gruppi = defaultdict(list)
        for T in combinations(range(1, NN + 1), 3):
            gruppi[inv3(T)].append(T)
        qt = []
        for k, lst in gruppi.items():
            if len(lst) < 4:
                continue
            for Q in combinations(lst, 4):
                if all(not (set(Q[i]) & set(Q[j]))
                       for i in range(4) for j in range(i + 1, 4)):
                    qt.append((k, Q))
        P(f"quaterne in [1..{NN}]: {len(qt)}")
        for k, Q in qt:
            P(f"    chiave {k}: " + " ".join(str(list(T)) for T in Q))
        if NN == 26:
            genp = set()
            for k, Q in qt:
                for (i, j) in ((0, 1), (0, 2), (0, 3)):
                    resto = [x for x in range(4) if x not in (i, j)]
                    A = tuple(sorted(Q[i] + Q[j]))
                    B = tuple(sorted(Q[resto[0]] + Q[resto[1]]))
                    genp.add(frozenset((A, B)))
            tutte_hs = {frozenset((A, B)) for key, A, B in hs_nuove}
            tutte_hs |= {frozenset(p) for p in (ORO1,)} | {
                frozenset((A, B)) for key, A, B, gem in mis[24][3]
                if carta(key, A, B, gem)[1] == FH}
            P(f"B2-d: coppie generate dalle quaterne di [1..26]: "
              f"{len(genp)}; half-sum censite (24+26): "
              f"{len(tutte_hs)}; generate == censite? "
              f"{genp == tutte_hs}")
    P()
    P("=" * 68)
    P("VERDETTO B2")
    P("=" * 68)
    P(f"floor-check GO (cap {CAP:.0f}s <= budget {BUDGET:.0f}s); "
      f"N=26: {npairs} coppie, |G| {dict(sorted(dist.items()))}")
    P(f"nuove |G|=4: {len(nuove)} = {dict(forme)}; forme terze: "
      f"{len(terze)}; deviazioni di firma: {stop_c}")

with open(os.path.join(LOGS, "salita-n26.log"), "w",
          encoding="utf-8") as f:
    f.write("\n".join(OUT) + "\n")
