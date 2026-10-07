"""SEDUTA INVARIANTE 156x32 — Bersaglio 4: SALITA A N=24 col
floor-check PRE-DISEGNO. MISURA, non teoria.

FASE A (floor-check, stampato PRIMA di ogni disegno della fase B):
- costo del censimento MISURATO con questo stesso codice a
  N = 18, 20, 22 (sestine, coppie disgiunte same-bucket, tempo);
- C(24,6) esatto; proiezione di coppie e tempo a N=24 dai rapporti
  MISURATI qui (mai ereditati da sedute precedenti);
- CAP DERIVATO dalla misura: 3 x tempo proiettato (fattore di
  sicurezza 3, dichiarato); BUDGET di seduta per B4: 600 s,
  dichiarato qui prima della misura. GO se CAP <= BUDGET; altrimenti
  NON APERTO coi numeri del floor-check a verbale.

FASE B (solo se GO):
- censimento completo a N=24: distribuzione |G| su tutte le coppie
  disgiunte same-bucket; coppie |G|=4; NUOVE = non presenti nel
  censimento [1..22] (ricostruito in fase A);
- per OGNI coppia nuova: firma {misti, solo-N3, solo-N2, nulli} su
  720 accoppiamenti e incidenza canonica congiunta, confrontate con
  la carta d'identita delle 156.

FACCE PRE-SCRITTE:
 B4-a: firma diversa da {misti 32, solo-N3 40, solo-N2 488, nulli
       160} su UNA coppia nuova = uniformita FALSIFICATA fuori
       campione (dato d'oro, membri a verbale); firma uguale su tutte
       = estensione out-of-sample dell'uniformita.
 B4-b: incidenza canonica congiunta diversa su una nuova = seconda
       forma della classe (dato d'oro coi membri); uguale su tutte =
       classe unica estesa.
 B4-c: distribuzione |G| a N=24 a verbale, valori oltre 4 compresi:
       se compaiono, membri a verbale (dato nuovo, fuori dal
       perimetro della firma).
Log: logs/invariante-n24.log
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
    """Bucket, coppie disgiunte same-bucket, |G| per coppia.
    Ritorna (n_sestine, n_coppie, dist_G, lista coppie |G|=4)."""
    bucket = defaultdict(list)
    for S in combinations(range(1, N + 1), 6):
        bucket[(sum(S), sum(v * v for v in S))].append(S)
    nsest = sum(len(v) for v in bucket.values())
    dist = Counter()
    npairs = 0
    q4 = []
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
            if g == 4:
                gem = []
                for kk, TAs in dA.items():
                    TBs = dB.get(kk)
                    if TBs:
                        for TA in TAs:
                            for TB in TBs:
                                gem.append((TA, TB))
                q4.append((key, A, B, gem))
    return nsest, npairs, dist, q4


# ------------------------------------------------------------------
P("=" * 68)
P("FASE A — FLOOR-CHECK (prima del disegno)")
P("=" * 68)
mis = {}
for N in (18, 20, 22):
    t0 = time.time()
    nsest, npairs, dist, q4 = censimento(N)
    dt = time.time() - t0
    mis[N] = (nsest, npairs, dt, q4)
    P(f"  N={N}: sestine {nsest}, coppie {npairs}, |G|=4: {len(q4)}, "
      f"tempo {dt:.1f}s")

c246 = 1
for i in range(6):
    c246 = c246 * (24 - i) // (i + 1)
r_coppie = mis[22][1] / mis[20][1]
r_coppie2 = mis[20][1] / mis[18][1]
r_tempo = mis[22][2] / max(0.001, mis[20][2])
proj_coppie = mis[22][1] * (r_coppie + r_coppie2) / 2
proj_tempo = mis[22][2] * r_tempo
CAP = 3 * proj_tempo
BUDGET = 600.0
P(f"C(24,6) esatto = {c246}")
P(f"rapporti misurati: coppie x{r_coppie2:.2f} (18->20), "
  f"x{r_coppie:.2f} (20->22); tempo x{r_tempo:.2f} (20->22)")
P(f"proiezione N=24: ~{proj_coppie:.0f} coppie, ~{proj_tempo:.0f}s "
  f"di censimento")
P(f"CAP DERIVATO = 3 x {proj_tempo:.0f}s = {CAP:.0f}s; "
  f"BUDGET dichiarato = {BUDGET:.0f}s")
GO = CAP <= BUDGET
P(f"DECISIONE (prima della fase B): {'GO' if GO else 'NON APERTO'}")
P()

if not GO:
    P("FASE B NON APERTA: numeri del floor-check qui sopra a verbale.")
else:
    # ----------------------------------------------------------
    P("=" * 68)
    P("FASE B — CENSIMENTO N=24 e firma delle coppie NUOVE")
    P("=" * 68)
    t0 = time.time()
    nsest, npairs, dist, q4_24 = censimento(24)
    P(f"N=24: sestine {nsest} (atteso {c246}), coppie disgiunte "
      f"same-bucket {npairs}")
    P(f"distribuzione |G|: {dict(sorted(dist.items()))}")
    P(f"coppie |G|=4 a N=24: {len(q4_24)}  "
      f"[censimento: {time.time()-t0:.1f}s]")
    extra = []
    if any(g > 4 for g in dist):
        # membri delle coppie con |G| > 4 (ricalcolo mirato)
        bucket = defaultdict(list)
        for S in combinations(range(1, 25), 6):
            bucket[(sum(S), sum(v * v for v in S))].append(S)
        for key in sorted(bucket):
            lst = bucket[key]
            if len(lst) < 2:
                continue
            for A, B in combinations(lst, 2):
                if set(A) & set(B):
                    continue
                dA = defaultdict(int)
                for T in combinations(A, 3):
                    dA[inv3(T)] += 1
                g = 0
                for T in combinations(B, 3):
                    g += dA.get(inv3(T), 0)
                if g > 4:
                    extra.append((key, A, B, g))
        P(f"coppie con |G| > 4 (B4-c, dato nuovo): {len(extra)}")
        for key, A, B, g in extra[:40]:
            P(f"  |G|={g} {key} A={list(A)} B={list(B)}")
    vecchie = {frozenset((A, B)) for key, A, B, gem in mis[22][3]}
    nuove = [x for x in q4_24 if frozenset((x[1], x[2]))
             not in vecchie]
    P(f"coppie |G|=4 NUOVE (non in [1..22]): {len(nuove)}; "
      f"ritrovate delle 156: {len(q4_24) - len(nuove)}")
    ctrl = sum(1 for key, A, B, gem in nuove
               if max(A[-1], B[-1]) < 23)
    P(f"ricontrollo per appartenenza: nuove senza 23/24: {ctrl} "
      f"(attesa 0)")
    P()

    # carta d'identita e firma su ogni nuova (stesse convenzioni di
    # invariante_156.py)
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

    FIRMA = Counter({"solo-N2": 488, "nullo": 160, "solo-N3": 40,
                     "misto": 32})

    def carta(key, A, B, gem):
        gset = set(gem)
        chiuso = all((comp(A, TA), comp(B, TB)) in gset
                     for TA, TB in gem)
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
        return chiuso, ordg, canon_joint(MA, MB), MA[0][2], MB[0][2]

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

    t0 = time.time()
    # riferimento: incidenza canonica delle 156 (misurata in fase A)
    rif = None
    for key, A, B, gem in mis[22][3]:
        ch, ordg, cj, a_i, b_i = carta(key, A, B, gem)
        if rif is None:
            rif = cj
    firme_dev = []
    inc_dev = []
    chiuse_dev = 0
    celle = Counter()
    for key, A, B, gem in nuove:
        ch, ordg, cj, a_i, b_i = carta(key, A, B, gem)
        if not ch:
            chiuse_dev += 1
            P(f"  <<< CHIUSURA COMPLEMENTO VIOLATA: A={list(A)} "
              f"B={list(B)}")
        celle[min((a_i, b_i), (3 - a_i, 3 - b_i))] += 1
        if cj != rif:
            inc_dev.append((key, A, B))
            P(f"  <<< INCIDENZA DIVERSA (B4-b, dato d'oro): "
              f"{key} A={list(A)} B={list(B)}")
            P(f"      lato A: {cj[0]}")
            P(f"      lato B: {cj[1]}")
        cnt = firma720(A, B, ordg)
        if cnt != FIRMA:
            firme_dev.append((key, A, B, dict(cnt)))
            P(f"  <<< FIRMA DIVERSA (B4-a, dato d'oro): {key} "
              f"A={list(A)} B={list(B)} {dict(cnt)}")
    P(f"nuove con firma diversa da 32/40/488/160: {len(firme_dev)} "
      f"su {len(nuove)}")
    P(f"nuove con incidenza canonica diversa: {len(inc_dev)}")
    P(f"chiusura complemento violata: {chiuse_dev}")
    P(f"celle (a,b) normalizzate sulle nuove: "
      f"{dict(sorted(celle.items()))}")
    P(f"[firme nuove: {time.time()-t0:.1f}s]")
    P()
    P("elenco delle coppie NUOVE coi membri (key, A, B):")
    for i, (key, A, B, gem) in enumerate(nuove, 1):
        P(f"  [{i:3d}] {key} A={list(A)} B={list(B)}")
    P()
    P("=" * 68)
    P("VERDETTO B4")
    P("=" * 68)
    P(f"floor-check: GO (cap {CAP:.0f}s <= budget {BUDGET:.0f}s)")
    P(f"B4-c: distribuzione |G| a N=24: {dict(sorted(dist.items()))}")
    P("B4-a: " + (f"firma 32/40/488/160 su TUTTE le {len(nuove)} "
      "nuove coppie: uniformita ESTESA out-of-sample"
      if not firme_dev else
      f"<<< {len(firme_dev)} coppie nuove con firma diversa: "
      "uniformita FALSIFICATA fuori campione, membri sopra"))
    P(f"B4-b: " + ("incidenza canonica congiunta IDENTICA su tutte "
      "le nuove: classe unica estesa" if not inc_dev else
      f"<<< {len(inc_dev)} nuove con incidenza diversa: seconda "
      "forma, membri sopra"))

with open(os.path.join(LOGS, "invariante-n24.log"), "w",
          encoding="utf-8") as f:
    f.write("\n".join(OUT) + "\n")
