"""Bersaglio 1b — TERZA implementazione del vaglio UNICITA 1.078
(riscritta da specifica).

FACCE PRE-SCRITTE (stampate prima dei calcoli):
  attese 1.078 coppie distinte di blocchi; |G| {0: 811, 2: 267};
  complementarita 267/267; zero violazioni di UNICITA.
  Per mondo (vuote+non vuote): 3799 85+29; 3659 83+31; 3671 46+14;
  3691 44+16; hub-44 62+28; pfeffermann 128+72; boyer 126+74;
  w648 29+1; m330 28+2; altri sei 30+0.
  OGNI scarto FERMA e si verbalizza, non si adatta.

Base: coppie NON ORDINATE distinte di blocchi delle partizioni che
entrano in coppie ortogonali, 15 mondi di bound_mondi.
Log: logs/terza-vaglio-unicita.log
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


P(__doc__)

PF = [[6, 42, 29, 3, 40, 30], [8, 44, 47, 21, 20, 10],
      [33, 31, 41, 37, 1, 7], [19, 17, 13, 9, 43, 49],
      [36, 2, 5, 35, 34, 38], [48, 14, 15, 45, 12, 16]]
BOYER = [[41, 35, 6, 2, 37, 47], [5, 42, 33, 39, 46, 3],
         [38, 7, 45, 43, 1, 34], [22, 55, 13, 11, 49, 18],
         [53, 10, 17, 23, 14, 51], [9, 19, 54, 50, 21, 15]]
MORG72 = [[72, 18, 17, 16, 49, 47], [13, 52, 36, 5, 50, 63],
          [38, 35, 7, 66, 15, 58], [20, 53, 34, 39, 69, 4],
          [55, 1, 57, 56, 26, 24], [21, 60, 68, 37, 10, 23]]
W408 = [[17, 36, 55, 124, 62, 114], [58, 40, 129, 50, 111, 20],
        [108, 135, 34, 44, 38, 49], [87, 98, 92, 102, 1, 28],
        [116, 25, 86, 7, 96, 78], [22, 74, 12, 81, 100, 119]]
W618 = [[1, 62, 78, 138, 186, 153], [94, 126, 193, 25, 154, 26],
        [124, 173, 76, 184, 21, 40], [166, 185, 22, 130, 33, 82],
        [180, 52, 181, 13, 80, 112], [53, 20, 68, 128, 144, 205]]
W648 = [[23, 82, 151, 190, 109, 93], [99, 75, 135, 159, 166, 14],
        [90, 215, 102, 39, 97, 105], [111, 119, 177, 114, 1, 126],
        [202, 50, 57, 81, 141, 117], [123, 107, 26, 65, 134, 193]]
W714 = [[18, 48, 126, 145, 204, 173], [110, 161, 237, 88, 92, 26],
        [184, 101, 86, 216, 14, 113], [125, 224, 22, 152, 137, 54],
        [212, 146, 150, 1, 77, 128], [65, 34, 93, 112, 190, 220]]
M330 = [[9, 83, 105, 84, 15, 34], [27, 101, 26, 5, 76, 95],
        [109, 78, 28, 13, 17, 85], [32, 1, 97, 82, 25, 93],
        [54, 11, 67, 103, 91, 4], [99, 56, 7, 43, 106, 19]]
RLIB = [[257, 263, 239, 13, 31, 317], [71, 281, 37, 277, 107, 347],
        [331, 73, 167, 337, 193, 19], [17, 359, 53, 271, 197, 223],
        [307, 97, 383, 59, 173, 101], [137, 47, 241, 163, 419, 113]]
RASS = [[337, 293, 1867, 2089, 2003, 1601], [1933, 929, 2129, 433, 523, 2243],
        [2143, 2281, 373, 1847, 977, 569], [2161, 1753, 883, 2357, 449, 587],
        [487, 2207, 2297, 601, 1801, 797], [1129, 727, 641, 863, 2437, 2393]]
MONDI = [
    ("3799", sorted(v for v in range(1, 43) if v not in {19, 20, 21, 22, 23, 24})),
    ("3659", sorted(v for v in range(1, 43) if v not in {4, 11, 18, 25, 32, 39})),
    ("3671", sorted(v for v in range(1, 43) if v not in {7, 8, 21, 22, 35, 36})),
    ("3691", sorted(v for v in range(1, 43) if v not in {10, 11, 12, 31, 32, 33})),
    ("hub-44", sorted(v for v in range(1, 45) if v not in {13, 20, 21, 22, 23, 24, 25, 32})),
    ("pfeffermann", sorted(v for r in PF for v in r)),
    ("boyer", sorted(v for r in BOYER for v in r)),
    ("morgenstern-72", sorted(v for r in MORG72 for v in r)),
    ("wroblewski-408", sorted(v for r in W408 for v in r)),
    ("wroblewski-618", sorted(v for r in W618 for v in r)),
    ("wroblewski-648", sorted(v for r in W648 for v in r)),
    ("wroblewski-714", sorted(v for r in W714 for v in r)),
    ("morgenstern-330", sorted(v for r in M330 for v in r)),
    ("rouanet-libero", sorted(v for r in RLIB for v in r)),
    ("rouanet-assoc", sorted(v for r in RASS for v in r)),
]

ATTESI = {"3799": (85, 29), "3659": (83, 31), "3671": (46, 14),
          "3691": (44, 16), "hub-44": (62, 28), "pfeffermann": (128, 72),
          "boyer": (126, 74), "wroblewski-648": (29, 1),
          "morgenstern-330": (28, 2)}
tot = Counter()
comp_ok = comp_tot = viol = 0
scarti = []
for label, V in MONDI:
    s1 = sum(V) // 6
    s2 = sum(v * v for v in V) // 6
    subs = find_subsets(V, 6, s1, s2)
    parts = [tuple(sorted((frozenset(x) for x in p), key=min))
             for p in gp(subs, V)]
    orth = [(i, j) for i in range(len(parts))
            for j in range(i + 1, len(parts))
            if n1(parts[i], parts[j]) == 36]
    indici = sorted(set(i for ab in orth for i in ab))
    coppie = set()
    for i in indici:
        for X, Y in combinations(parts[i], 2):
            coppie.add(frozenset((X, Y)))
    vuote = nonv = 0
    for cp in coppie:
        X, Y = tuple(cp)
        G = []
        for TA in combinations(sorted(X), 3):
            for TB in combinations(sorted(Y), 3):
                if (sum(TA) == sum(TB) and
                        sum(v * v for v in TA) == sum(v * v for v in TB)):
                    G.append((frozenset(TA), frozenset(TB)))
        if not G:
            vuote += 1
            continue
        nonv += 1
        if len(G) == 2:
            (Ta, Tb), (Tc, Td) = G
            comp_tot += 1
            if Tc == frozenset(X) - Ta and Td == frozenset(Y) - Tb:
                comp_ok += 1
        else:
            viol += 1
            P(f"  <<< |G|={len(G)} a {label}: blocchi "
              f"{sorted(X)} / {sorted(Y)} — VIOLAZIONE O CASO NUOVO")
    tot["tot"] += len(coppie)
    tot[0] += vuote
    tot[2] += nonv
    att = ATTESI.get(label, (30, 0))
    riga = f"  {label}: coppie {len(coppie)} = vuote {vuote} + nonv {nonv}"
    if (vuote, nonv) != att:
        scarti.append(label)
        riga += f"  <<< SCARTO (attese {att})"
    P(riga)

ok = (tot["tot"] == 1078 and tot[0] == 811 and tot[2] == 267 and
      comp_ok == 267 and viol == 0 and not scarti)
P(f"\nVERDETTO 1b: coppie {tot['tot']} (attese 1078), vuote {tot[0]} "
  f"(811), non vuote {tot[2]} (267), complementari {comp_ok}/267, "
  f"violazioni {viol}")
P("  ATTESI CENTRATI — terza implementazione concorde" if ok else
  f"  <<< SCARTO: STOP e verbale (mondi in scarto: {scarti})")

with open(os.path.join(L, "terza-vaglio-unicita.log"), "w",
          encoding="utf-8") as f:
    f.write("\n".join(OUT) + "\n")
