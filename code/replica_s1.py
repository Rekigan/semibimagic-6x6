#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""replica_s1.py — replica INDIPENDENTE della classificazione a max=42.

DICHIARAZIONE D'INDIPENDENZA: questo file e' stato scritto SENZA leggere
nessun altro file di code/. Unico input: il claim da replicare
(4 insiemi, partizioni 8/8/4/4, S2 in {3659,3671,3691,3799}, S1=129 forzato).

FRAMING (diverso dai due algoritmi descritti nel paper, Section 4):
  1. si enumerano gli SCARTI: d = 6 valori omessi da 1..(M-1), M resta;
     filtri di divisibilita' su somma e somma dei quadrati PRIMA di tutto;
  2. per ogni scarto: insieme V fissato -> sestetti (S1,S2) via DFS potata;
  3. partizioni in righe: exact cover sul bit piu' basso scoperto
     (partizioni NON ordinate, contate una volta);
  4. ORTOGONALITA': un quadrato esiste sse esistono colonne = 6 trasversali
     disgiunte delle righe, ognuna con (S1,S2). DFS colonna per colonna.

Uso (Windows: py -3 -X utf8):
  py -3 -X utf8 replica_s1.py --smoke          # 5 bersagli noti a s1=129 (~1 min)
  py -3 -X utf8 replica_s1.py --full           # classificazione intera max=42
  py -3 -X utf8 replica_s1.py --full --max 41  # replica dell'esclusione di 41
  py -3 -X utf8 replica_s1.py --full --s1lo 112 --s1hi 129   # a fette, riprendibile

Output: righe di testo + JSON in ../logs/replica-<modo>-<max>.json
Zero dipendenze fuori dalla stdlib. Deterministico. Nessun RNG.
"""
from __future__ import annotations
import argparse, json, os, sys, time
from itertools import combinations

# ---------------------------------------------------------------- utilita'

def subsets_k(vals, k, sum_t, sq_lo, sq_hi):
    """Tutti i k-sottoinsiemi di vals (ordinati) con somma sum_t e
    somma dei quadrati in [sq_lo, sq_hi]. DFS con potatura su entrambe."""
    vals = sorted(vals)
    n = len(vals)
    pre = [0]*(n+1)
    qre = [0]*(n+1)
    for i, v in enumerate(vals):
        pre[i+1] = pre[i] + v
        qre[i+1] = qre[i] + v*v
    out = []
    chosen = []

    def rec(i, k, s, q):
        if k == 0:
            if s == sum_t and sq_lo <= q <= sq_hi:
                out.append(tuple(chosen))
            return
        if i + k > n:
            return
        # potatura somma: min = k piu' piccoli da i; max = k piu' grandi in coda
        if s + (pre[i+k] - pre[i]) > sum_t:
            return
        if s + (pre[n] - pre[n-k]) < sum_t:
            return
        # potatura quadrati (vals ordinati -> quadrati ordinati)
        if q + (qre[i+k] - qre[i]) > sq_hi:
            return
        if q + (qre[n] - qre[n-k]) < sq_lo:
            return
        # includi vals[i]
        chosen.append(vals[i])
        rec(i+1, k-1, s + vals[i], q + vals[i]*vals[i])
        chosen.pop()
        # salta vals[i]
        rec(i+1, k, s, q)

    rec(0, k, 0, 0)
    return out


def partizioni_righe(V, s1, s2):
    """Partizioni NON ordinate di V in 6 sestetti con (s1, s2) esatti.
    Ritorna (numero, lista di partizioni come tuple di sestetti)."""
    idx = {v: i for i, v in enumerate(V)}
    sest = subsets_k(V, 6, s1, s2, s2)
    if not sest:
        return 0, []
    masks = []
    for s in sest:
        m = 0
        for v in s:
            m |= 1 << idx[v]
        masks.append((m, s))
    by_bit = [[] for _ in range(len(V))]
    for m, s in masks:
        b = (m & -m).bit_length() - 1
        by_bit[b].append((m, s))
    FULL = (1 << len(V)) - 1
    trovate = []
    stack = []

    def cover(c):
        if c == FULL:
            trovate.append(tuple(stack))
            return
        b = ((~c) & (c+1)).bit_length() - 1   # bit piu' basso scoperto
        for m, s in by_bit[b]:
            if m & c == 0:
                stack.append(s)
                cover(c | m)
                stack.pop()

    cover(0)
    return len(trovate), trovate


def quadrato_da_righe(part, s1, s2):
    """Data una partizione in righe, cerca 6 colonne trasversali con (s1,s2).
    ESAUSTIVA con backtracking pieno: un None qui significa che NESSUN
    quadrato ha quelle righe. Canonicalizzazione: ogni colonna deve
    contenere il minimo valore ancora libero (uccide il 6! delle colonne).
    Ritorna la matrice 6x6 (righe nell'ordine dato) o None."""
    rows = [set(r) for r in part]
    colonne = []

    def transversali():
        """Tutte le trasversali (un valore per riga) con (s1,s2) esatti,
        vincolate a contenere il minimo globale ancora libero."""
        m = min(min(r) for r in rows)
        i_m = next(i for i in range(6) if m in rows[i])
        ordine = [i_m] + sorted((i for i in range(6) if i != i_m),
                                key=lambda i: len(rows[i]))
        arr = [[m]] + [sorted(rows[i]) for i in ordine[1:]]
        # suffissi min/max per potatura su somma e quadrati
        smin = [0]*7; smax = [0]*7; qmin = [0]*7; qmax = [0]*7
        for d in range(5, -1, -1):
            smin[d] = smin[d+1] + arr[d][0]
            smax[d] = smax[d+1] + arr[d][-1]
            qmin[d] = qmin[d+1] + arr[d][0]**2
            qmax[d] = qmax[d+1] + arr[d][-1]**2
        out = []
        cur = []

        def rec(d, s, q):
            if d == 6:
                if s == s1 and q == s2:
                    out.append(list(cur))
                return
            if s + smin[d] > s1 or s + smax[d] < s1:
                return
            if q + qmin[d] > s2 or q + qmax[d] < s2:
                return
            for v in arr[d]:
                cur.append((ordine[d], v))
                rec(d+1, s+v, q+v*v)
                cur.pop()

        rec(0, 0, 0)
        return out

    def rec_cols(j):
        if j == 6:
            return True
        for t in transversali():
            for i, v in t:
                rows[i].discard(v)
            colonne.append(t)
            if rec_cols(j+1):
                return True
            colonne.pop()
            for i, v in t:
                rows[i].add(v)
        return False

    if rec_cols(0):
        M = [[None]*6 for _ in range(6)]
        for j, t in enumerate(colonne):
            for i, v in t:
                M[i][j] = v
        return M
    return None


def verifica_quadrato(M, s1, s2):
    ok = True
    vals = [x for r in M for x in r]
    ok &= len(set(vals)) == 36
    for r in M:
        ok &= sum(r) == s1 and sum(x*x for x in r) == s2
    for j in range(6):
        c = [M[i][j] for i in range(6)]
        ok &= sum(c) == s1 and sum(x*x for x in c) == s2
    return ok

# ------------------------------------------------------------------ motore

def classifica(M_max, s1_lo, s1_hi, s2_only=None, log=print):
    """Enumera per scarti. Ritorna la lista dei reperti."""
    tot = M_max*(M_max+1)//2
    totq = M_max*(M_max+1)*(2*M_max+1)//6
    k_drop = M_max*M_max - 0  # non usato: |V|=36 fisso
    n_drop = M_max - 36       # 6 per M=42, 5 per M=41
    reperti = []
    t0 = time.time()
    n_cand = 0
    for s1 in range(s1_lo, s1_hi+1):
        dropsum = tot - 6*s1
        if dropsum < sum(range(1, n_drop+1)):
            continue
        if dropsum > sum(range(M_max-n_drop, M_max)):
            continue
        # scarti da 1..M-1 (M deve restare), divisibilita' gia' imposta da s1
        drops = subsets_k(range(1, M_max), n_drop, dropsum, 0, 10**9)
        # raggruppa per somma dei quadrati scartata -> s2
        per_q = {}
        for d in drops:
            q = sum(x*x for x in d)
            if (totq - q) % 6:
                continue
            s2 = (totq - q)//6
            if s2_only is not None and s2 not in s2_only:
                continue
            per_q.setdefault(s2, []).append(d)
        for s2 in sorted(per_q):
            for d in per_q[s2]:
                n_cand += 1
                V = [v for v in range(1, M_max+1) if v not in set(d)]
                n_part, parts = partizioni_righe(V, s1, s2)
                if n_part == 0:
                    continue
                quadro = None
                for p in parts:
                    quadro = quadrato_da_righe(p, s1, s2)
                    if quadro is not None:
                        assert verifica_quadrato(quadro, s1, s2), "QUADRATO NON VALIDO"
                        break
                rep = {"max": M_max, "s1": s1, "s2": s2,
                       "omette": sorted(d), "partizioni": n_part,
                       "quadrato_esiste": quadro is not None,
                       "quadrato": quadro}
                reperti.append(rep)
                log(f"  REPERTO s1={s1} s2={s2} omette={sorted(d)} "
                    f"partizioni={n_part} quadrato={'SI' if quadro else 'NO'}")
        if s1 % 4 == 0:
            log(f"  ... s1={s1} fatto, {n_cand} candidati visti, "
                f"{time.time()-t0:.0f}s")
    log(f"TOTALE: {n_cand} insiemi candidati esaminati in {time.time()-t0:.0f}s; "
        f"{len(reperti)} con almeno una partizione in righe.")
    return reperti


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--max", type=int, default=42)
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--targets", action="store_true",
                    help="verifica diretta dei 5 insiemi noti (veloce)")
    ap.add_argument("--full", action="store_true")
    ap.add_argument("--s1lo", type=int)
    ap.add_argument("--s1hi", type=int)
    args = ap.parse_args()

    M = args.max
    tot = M*(M+1)//2
    n_drop = M - 36
    s1_min = (tot - sum(range(M-n_drop, M))) // 6
    while (tot - 6*s1_min) > sum(range(M-n_drop, M)):
        s1_min += 1
    s1_max = (tot - sum(range(1, n_drop+1))) // 6

    if args.targets:
        modo = "targets"
        # verifica diretta: i 4 insiemi del claim + il negativo 3459
        bersagli = [((4,11,18,25,32,39), 3659, 8),
                    ((7,8,21,22,35,36), 3671, 4),
                    ((10,11,12,31,32,33), 3691, 4),
                    ((19,20,21,22,23,24), 3799, 8),
                    ((2,3,4,39,40,41), 3459, 0)]
        rep = []
        ok_tutti = True
        for drop, s2_att, np_att in bersagli:
            V = [v for v in range(1, 43) if v not in set(drop)]
            s1 = sum(V)//6
            s2 = sum(x*x for x in V)//6
            t0 = time.time()
            n_part, parts = partizioni_righe(V, s1, s2)
            quadro = None
            n_ext = 0
            for p in parts:
                q = quadrato_da_righe(p, s1, s2)
                if q is not None:
                    n_ext += 1
                    if quadro is None:
                        assert verifica_quadrato(q, s1, s2), "NON VALIDO"
                        quadro = q
            # IPOTESI DI LETTURA: il claim conta le partizioni CHE SI
            # ESTENDONO a un quadrato, non tutte le partizioni in righe.
            ok = (s2 == s2_att and n_ext == np_att and
                  (quadro is not None) == (np_att > 0))
            ok_tutti &= ok
            print(f"omette {drop}: s2={s2} (atteso {s2_att}) "
                  f"part_righe={n_part} di cui ESTENDIBILI={n_ext} "
                  f"(attese {np_att}) quadrato={'SI' if quadro else 'NO'} "
                  f"[{time.time()-t0:.1f}s] {'OK' if ok else '<<< SCARTO'}")
            rep.append({"omette": list(drop), "s1": s1, "s2": s2,
                        "partizioni_righe": n_part,
                        "partizioni_estendibili": n_ext,
                        "quadrato_esiste": quadro is not None,
                        "quadrato": quadro, "concorda_col_claim": ok})
        print()
        print(f"VERDETTO targets: {'5/5 CONCORDANO' if ok_tutti else 'DISCREPANZE - vedi sopra'}")
    elif args.smoke:
        # i 5 bersagli noti a s1=129: i 4 del claim + il negativo 3459
        modo = "smoke"
        rep = classifica(42, 129, 129,
                         s2_only={3459, 3659, 3671, 3691, 3799})
        attesi = {(3659, (4,11,18,25,32,39), 8),
                  (3671, (7,8,21,22,35,36), 4),
                  (3691, (10,11,12,31,32,33), 4),
                  (3799, (19,20,21,22,23,24), 8)}
        visti = {(r["s2"], tuple(r["omette"]), r["partizioni"]) for r in rep}
        print()
        print("CONFRONTO COL CLAIM:")
        print(f"  attesi e trovati : {sorted(attesi & visti)}")
        print(f"  attesi NON trovati: {sorted(attesi - visti)}")
        print(f"  trovati NON attesi: {sorted(visti - attesi)}")
        neg = [r for r in rep if r["s2"] == 3459]
        print(f"  negativo 3459: {'NESSUNA partizione (atteso)' if not neg else neg}")
        quadri = all(r["quadrato_esiste"] for r in rep)
        print(f"  quadrato costruito per ogni insieme: {quadri}")
    elif args.full:
        lo = args.s1lo if args.s1lo else s1_min
        hi = args.s1hi if args.s1hi else s1_max
        modo = "full" if (lo, hi) == (s1_min, s1_max) else f"full-s1_{lo}-{hi}"
        print(f"CLASSIFICAZIONE max={M}: s1 in [{lo},{hi}] "
              f"(range teorico [{s1_min},{s1_max}])")
        rep = classifica(M, lo, hi)
    else:
        ap.print_help(); return 2

    logdir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          "..", "logs")
    os.makedirs(logdir, exist_ok=True)
    out = os.path.join(logdir, f"replica-{modo}-{M}.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(rep, f, ensure_ascii=False, indent=1)
    print(f"JSON: {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
