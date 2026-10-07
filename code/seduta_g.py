"""SEDUTA G — il grafo delle gemelle: equivalenza, censimento,
(N3, N2) esaustivo.

PREREGISTRAZIONE (stampata prima di ogni calcolo):
 FACCIA: EXCL falsificata se esiste UN accoppiamento con N3 > 0 E
 N2 > 0; confermata-estesa se N3*N2 = 0 su TUTTI. Lo sweep e'
 ESAUSTIVO: 720 accoppiamenti = tutte le biiezioni per coppia.
 RIGIDITA attesa (lama T1): due gemelle della stessa classe di
 invarianti (somma, somma quadrati) condividono al piu' 1 elemento
 per lato (2 condivisi + invarianti uguali forzano il terzo uguale).

Basi: 3 viste campione (tipo A, tipo B, orfano) x 15 coppie di
colonne = 45 coppie-oggetto; per ciascuna: G pairing-indipendente
(terne di A x terne di B a invarianti uguali), poi sweep 720.
Passo 1: equivalenza gemelle <-> hom_aff su ogni accoppiamento.
Log: logs/seduta-g.log
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


def carica(V):
    s1 = sum(V) // 6
    s2 = sum(v * v for v in V) // 6
    subs = find_subsets(V, 6, s1, s2)
    parts = [tuple(sorted((frozenset(x) for x in p), key=min))
             for p in gp(subs, V)]
    return s1, s2, parts


PF = [[6, 42, 29, 3, 40, 30], [8, 44, 47, 21, 20, 10],
      [33, 31, 41, 37, 1, 7], [19, 17, 13, 9, 43, 49],
      [36, 2, 5, 35, 34, 38], [48, 14, 15, 45, 12, 16]]
W648 = [[23, 82, 151, 190, 109, 93], [99, 75, 135, 159, 166, 14],
        [90, 215, 102, 39, 97, 105], [111, 119, 177, 114, 1, 126],
        [202, 50, 57, 81, 141, 117], [123, 107, 26, 65, 134, 193]]
V42 = sorted(v for v in range(1, 43) if v not in {19, 20, 21, 22, 23, 24})
V_pf = sorted(v for r in PF for v in r)
V_w = sorted(v for r in W648 for v in r)
VISTE = [("3799 E=38 Q=0 (A)", V42, 38, 0),
         ("pfeffermann E=2 Q=70 (B, hub in riga)", V_pf, 2, 70),
         ("wroblewski-648 E=2 Q=1 (orfano)", V_w, 2, 1)]

mism = 0
n_acc = 0
falsificata = False
for label, V, Ei, Qi in VISTE:
    s1, s2, parts = carica(V)
    E, Q = parts[Ei], parts[Qi]
    assert n1(E, Q) == 36
    M = [[next(iter(E[j] & Q[c])) for c in range(6)] for j in range(6)]
    P(f"\n=== {label}")
    for c1, c2 in combinations(range(6), 2):
        pj = [M[j][c1] for j in range(6)]
        qj = [M[j][c2] for j in range(6)]
        A, B = pj, qj  # insiemi-colonna nell ordine reale
        # G pairing-indipendente: terne per INDICE di valore
        G = []
        for TA in combinations(range(6), 3):
            sA = sum(A[i] for i in TA)
            qA = sum(A[i] ** 2 for i in TA)
            for TB in combinations(range(6), 3):
                if (sum(B[i] for i in TB) == sA and
                        sum(B[i] ** 2 for i in TB) == qA):
                    G.append((frozenset(TA), frozenset(TB), sA, qA))
        # censimento G: classi di intersezione e rigidita
        cls = Counter()
        viol = []
        for (Ta, Tb, sA, qA), (Tc, Td, sC, qC) in combinations(G, 2):
            ia, ib = len(Ta & Tc), len(Tb & Td)
            cls[(ia, ib)] += 1
            if (sA, qA) == (sC, qC) and (ia == 2 or ib == 2):
                viol.append(((sorted(Ta), sorted(Tb)),
                             (sorted(Tc), sorted(Td))))
        # sweep esaustivo 720
        n3n2 = Counter()
        for perm in permutations(range(6)):
            q2 = [B[perm[j]] for j in range(6)]
            # allineamenti: posizione di B[i] sotto perm: pos tale che
            # perm[pos] = i -> inv
            inv = [0] * 6
            for pos in range(6):
                inv[perm[pos]] = pos
            N3 = N2 = 0
            for (Ta, Tb, _, _) in G:
                posB = frozenset(inv[i] for i in Tb)
                k = len(Ta & posB)
                if k == 3:
                    N3 += 1
                elif k == 2:
                    N2 += 1
            n_acc += 1
            n3n2[(N3 > 0, N2 > 0)] += 1
            if N3 > 0 and N2 > 0:
                falsificata = True
                P(f"  <<< EXCL FALSIFICATA: coppia ({c1},{c2}) "
                  f"perm {perm}: N3={N3} N2={N2}")
            # passo 1: equivalenza (campione: tutte le perm)
            h, a = hom_aff(pj, q2)
            if (h, a) != (N3 > 0, N2 > 0):
                mism += 1
                P(f"  <<< MISMATCH equivalenza ({c1},{c2}) {perm}: "
                  f"gemelle ({N3 > 0},{N2 > 0}) vs hom_aff ({h},{a})")
        P(f"  coppia ({c1},{c2}): |G|={len(G)} classi-int "
          f"{dict(cls) if cls else '{}'} rigidita-viol {len(viol)} | "
          f"sweep 720: {dict(n3n2)}")
        for v in viol[:3]:
            P(f"    VIOLAZIONE RIGIDITA (membri): {v}")

P(f"\nVERDETTI [basi: 45 coppie-oggetto, {n_acc} accoppiamenti "
  f"esaustivi, equivalenza testata su ognuno]:")
P(f"  passo 1 equivalenza gemelle<->hom_aff: mismatch {mism} "
  f"{'(PERFETTA)' if mism == 0 else ''}")
P(f"  passo 3 EXCL: "
  f"{'FALSIFICATA (vedi sopra)' if falsificata else 'N3*N2 = 0 su TUTTI gli accoppiamenti — confermata-estesa, base esaustiva per coppia'}")

with open(os.path.join(L, "seduta-g.log"), "w", encoding="utf-8") as f:
    f.write("\n".join(OUT) + "\n")
