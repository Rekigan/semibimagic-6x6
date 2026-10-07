"""SEDUTA INVARIANTE 156x32 (coda, seduta 2) — Bersaglio 3: TABELLA
FINE DAL MODELLO ASTRATTO, per ENTRAMBE le incidenze canoniche
(trasversale e half-sum). Chiude il test funzione-incidenza al
livello fine. MISURA e conteggio finito, non teoria.

Modello: punti astratti 0..5 per lato, nessuna aritmetica; gemella
i = (T_i, U_i) dalle realizzazioni della matrice d'incidenza; per
ogni biiezione psi delle 720: k_i = |psi(T_i) int U_i|; tabella
(kg, kh) = (k della gemella 1, k della gemella 3) su 720.

FACCE PRE-SCRITTE (attesi stampati qui, prima di ogni calcolo):
 B3-a TRASVERSALE: tabella modello attesa IDENTICA alla misurata
   della seduta 1 (invariante-156.log, unica x156):
   riga kg=0: 0,16,16,4 | kg=1: 16,128,164,16 | kg=2: 16,164,128,16
   | kg=3: 4,16,16,0 — celle (0,0) e (3,3) vuote, marginali
   36/324/324/36.
 B3-b HALF-SUM: tabella attesa ANTI-DIAGONALE kh = 3-kg (dal vettore
   derivato (k,3-k,3-k,k) di 8.17): (3,0)=36, (2,1)=324, (1,2)=324,
   (0,3)=36, tutte le altre celle 0.
 B3-c: tabella IDENTICA su TUTTE le combinazioni di realizzazioni
   enumerate di ciascuna forma (A-canonica x tutte le B e viceversa,
   dichiarato). Tabella diversa dall'attesa o non unica =
   CONTROESEMPIO: STOP e verbale coi membri.
Log: logs/modello-tabella-fine.log
"""
import os
import time
from itertools import combinations, permutations
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
LOGS = os.path.join(HERE, "..", "logs")
OUT = []


def P(msg=""):
    OUT.append(msg)
    print(msg, flush=True)


P(__doc__)

FORMA_T = (((3, 0, 1, 2), (0, 3, 2, 1), (1, 2, 3, 0), (2, 1, 0, 3)),
           ((3, 0, 2, 1), (0, 3, 1, 2), (2, 1, 3, 0), (1, 2, 0, 3)))
FORMA_H = (((3, 0, 0, 3), (0, 3, 3, 0), (0, 3, 3, 0), (3, 0, 0, 3)),
           ((3, 0, 3, 0), (0, 3, 0, 3), (3, 0, 3, 0), (0, 3, 0, 3)))
ATTESA_T = {(0, 1): 16, (0, 2): 16, (0, 3): 4,
            (1, 0): 16, (1, 1): 128, (1, 2): 164, (1, 3): 16,
            (2, 0): 16, (2, 1): 164, (2, 2): 128, (2, 3): 16,
            (3, 0): 4, (3, 1): 16, (3, 2): 16}
ATTESA_H = {(3, 0): 36, (2, 1): 324, (1, 2): 324, (0, 3): 36}


def realizzazioni(M):
    univ = set(range(6))
    out = []
    for T1t in combinations(range(6), 3):
        T1 = set(T1t)
        T2 = univ - T1
        for T3t in combinations(range(6), 3):
            T3 = set(T3t)
            T4 = univ - T3
            cand = [T1, T2, T3, T4]
            if all(len(cand[i] & cand[j]) == M[i][j]
                   for i in range(4) for j in range(4)):
                out.append(cand)
    return out


def tabella(RA, RB):
    tab = Counter()
    for q in permutations(range(6)):
        ks = []
        for i in (0, 2):
            ks.append(sum(1 for j in range(6)
                          if j in RA[i] and q[j] in RB[i]))
        tab[(ks[0], ks[1])] += 1
    return tab


def stampa_tab(tab):
    P("        kh=0   kh=1   kh=2   kh=3")
    for kg in range(4):
        P(f"  kg={kg}  " + "  ".join(f"{tab.get((kg, kh), 0):5d}"
                                     for kh in range(4)))


t0 = time.time()
for nome, (MAc, MBc), attesa in (("TRASVERSALE", FORMA_T, ATTESA_T),
                                 ("HALF-SUM", FORMA_H, ATTESA_H)):
    RAs = realizzazioni([list(r) for r in MAc])
    RBs = realizzazioni([list(r) for r in MBc])
    P("=" * 68)
    P(f"FORMA {nome}: realizzazioni lato A {len(RAs)}, lato B "
      f"{len(RBs)}")
    tabs = Counter()
    prove = 0
    for RB in RBs:
        tabs[tuple(sorted(tabella(RAs[0], RB).items()))] += 1
        prove += 1
    for RA in RAs:
        tabs[tuple(sorted(tabella(RA, RBs[0]).items()))] += 1
        prove += 1
    P(f"tabelle distinte su {prove} combinazioni (A-canonica x tutte "
      f"le B, B-canonica x tutte le A): {len(tabs)}")
    tab = dict(list(tabs)[0])
    stampa_tab(tab)
    uni = (len(tabs) == 1)
    eq = uni and Counter(tab) == Counter(attesa)
    m_ = tab.get((3, 2), 0) + tab.get((2, 3), 0)
    n3_ = sum(n for (a, b), n in tab.items()
              if (a == 3 or b == 3) and not (a == 2 or b == 2))
    n2_ = sum(n for (a, b), n in tab.items()
              if (a == 2 or b == 2) and not (a == 3 or b == 3))
    nul_ = sum(n for (a, b), n in tab.items()
               if a not in (2, 3) and b not in (2, 3))
    P(f"classi ricontate dalla tabella: misti {m_}, solo-N3 {n3_}, "
      f"solo-N2 {n2_}, nulli {nul_} (somma {m_ + n3_ + n2_ + nul_})")
    P(f"FACCIA {nome}: " + ("tabella UNICA e IDENTICA all'attesa — "
      "la tabella fine e funzione della sola incidenza e si deriva "
      "per conteggio" if eq else
      "<<< CONTROESEMPIO: tabella non unica o diversa dall'attesa, "
      "STOP e verbale"))
    P()

P(f"VERDETTO B3: vedi facce sopra. [{time.time()-t0:.1f}s]")

with open(os.path.join(LOGS, "modello-tabella-fine.log"), "w",
          encoding="utf-8") as f:
    f.write("\n".join(OUT) + "\n")
