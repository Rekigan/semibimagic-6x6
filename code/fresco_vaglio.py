"""Bersaglio 2 — VAGLIO 2c SU BASE FRESCA (mai aperto prima), con
floor-check obbligatorio PRIMA del disegno.

FASE A (floor-check): per N in {14, 16, 18}: tutte le sestine di
[1, N] (C(N,6)), bucket per (somma, somma-quadrati), conteggio coppie
DISGIUNTE nello stesso bucket, tempo. Da li si DERIVA il cap (mai
ereditato) e si dichiara N massimo e base attesa PRIMA della fase B.

FACCE PRE-SCRITTE (stampate qui, prima di ogni calcolo):
 F-a: una coppia con |G| non in {0,2}, o |G|=2 non complementare,
      FALSIFICA UNICITA sul fresco — la cosa piu importante che il
      vaglio possa dire.
 F-b: ogni violazione VA CLASSIFICATA nella cella (a,b) normalizzata;
      se cade in una cella CHIUSA da 8.15 e un BUG: STOP e verbale,
      niente interpretazione.
 F-c: atteso della congettura: zero violazioni; distribuzione |G| per
      bucket a verbale, vuoti compresi.
Log: logs/fresco-vaglio.log
"""
import os, sys, time
from itertools import combinations
from collections import Counter, defaultdict

L = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "logs")
OUT = []


def P(msg=""):
    OUT.append(msg)
    print(msg, flush=True)


P(__doc__)


def coppie_fresche(N):
    """Bucket delle sestine di [1..N] e coppie disgiunte per bucket."""
    bucket = defaultdict(list)
    for S in combinations(range(1, N + 1), 6):
        bucket[(sum(S), sum(v * v for v in S))].append(frozenset(S))
    coppie = []
    for k, lst in bucket.items():
        if len(lst) < 2:
            continue
        for A, B in combinations(lst, 2):
            if not (A & B):
                coppie.append((A, B, k))
    return bucket, coppie


# FASE A
P("FASE A — floor-check:")
mis = {}
for N in (14, 16, 18):
    t0 = time.time()
    bucket, coppie = coppie_fresche(N)
    dt = time.time() - t0
    mis[N] = (len(bucket), len(coppie), dt)
    P(f"  N={N}: sestine {sum(len(v) for v in bucket.values())}, "
      f"bucket {len(bucket)}, coppie disgiunte {len(coppie)}, "
      f"{dt:.1f}s")

# proiezione: coppie e tempo crescono; costo G-census ~ 400 check/coppia
# stimato dal rapporto misurato; cap dichiarato: 300 s per la fase B.
r1 = mis[18][1] / max(1, mis[16][1])
r2 = mis[16][1] / max(1, mis[14][1])
crescita = (r1 + r2) / 2
proi20 = mis[18][1] * crescita
proi22 = proi20 * crescita
P(f"\nDICHIARAZIONE (prima della fase B): crescita coppie/step "
  f"misurata ~x{crescita:.1f}; proiezione N=20 ~{proi20:.0f} coppie, "
  f"N=22 ~{proi22:.0f}. Costo G-census ~0.1 ms/coppia. CAP: 300 s.")
NMAX = 22 if proi22 * 0.0001 + 60 < 300 else 20
P(f"N MASSIMO DICHIARATO: {NMAX} (base attesa ~"
  f"{proi22 if NMAX == 22 else proi20:.0f} coppie a N={NMAX}, "
  f"piu i livelli sotto)")


def norm_ab(a, b):
    return min((a, b), (3 - a, 3 - b))


# FASE B
P("\nFASE B — vaglio fresco:")
viol = 0
stop_bug = False
for N in range(14, NMAX + 1, 2):
    t0 = time.time()
    bucket, coppie = coppie_fresche(N)
    dist = Counter()
    for A, B, k in coppie:
        Xs, Ys = sorted(A), sorted(B)
        G = []
        for TA in combinations(Xs, 3):
            for TB in combinations(Ys, 3):
                if (sum(TA) == sum(TB) and
                        sum(v * v for v in TA) == sum(v * v for v in TB)):
                    G.append((frozenset(TA), frozenset(TB)))
        dist[len(G)] += 1
        ok = (len(G) == 0 or
              (len(G) == 2 and G[1][0] == A - G[0][0]
               and G[1][1] == B - G[0][1]))
        if not ok:
            viol += 1
            P(f"  <<< VIOLAZIONE a N={N}: A={Xs} B={Ys} |G|={len(G)}")
            g = G[0]
            for (Ta, Tb) in G[1:]:
                if (Ta, Tb) == (A - g[0], B - g[1]):
                    continue
                cella = norm_ab(len(Ta & g[0]), len(Tb & g[1]))
                chiuse = {(0, 1), (1, 0), (0, 2), (1, 3), (1, 1), (2, 2)}
                P(f"      cella (a,b) normalizzata {cella} "
                  + ("<<< CELLA CHIUSA DA 8.15: BUG, STOP"
                     if cella in chiuse else "(cella residua: dato vero)"))
                if cella in chiuse:
                    stop_bug = True
    P(f"  N={N}: coppie {len(coppie)} | distribuzione |G| "
      f"{dict(sorted(dist.items()))} | violazioni cumulative {viol} "
      f"[{time.time()-t0:.0f}s]")
    if stop_bug:
        P("  STOP su cella chiusa: si verbalizza senza interpretare.")
        break

P(f"\nVERDETTO 2c: violazioni {viol} "
  + ("— UNICITA regge sul fresco (F-c centrata)" if viol == 0 else
     "— vedi classificazione F-b sopra"))

with open(os.path.join(L, "fresco-vaglio.log"), "w",
          encoding="utf-8") as f:
    f.write("\n".join(OUT) + "\n")
