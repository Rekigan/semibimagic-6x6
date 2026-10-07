"""Il laboratorio gemello + la sigma-struttura.

sigma: x -> 43-x agisce sulle partizioni di ogni candidato simmetrico
(preserva somma 129 e sqsum delle sestine, e preserva n1).  Quindi:
  - le partizioni si dividono in sigma-fisse e coppie scambiate
  - le coppie ortogonali vengono in orbite di sigma: conteggio DISPARI
    (5 nei vincitori 3799/3659) FORZA una coppia sigma-fissa
    -> un quadrato con simmetria di complemento esplicita
Domande:
  A. gli estendibili dei vincitori e gli hub dei quasi-vincitori sono
     sigma-fissi?
  B. anatomia dei difetti del gemello a=7: i quattro 32 dell'hub #50
     falliscono sempre sugli stessi elementi?
"""
import json, glob, os
from semibimagic import find_subsets, partitions

def get_parts(omit):
    nums = [x for x in range(1, 43) if x not in omit]
    S1, S2 = sum(nums) // 6, sum(x * x for x in nums) // 6
    subs = find_subsets(nums, 6, S1, S2)
    out = []
    for p in partitions(subs, nums):
        out.append(tuple(sorted((frozenset(s) for s in p), key=min)))
    return out

def canon(P):
    return frozenset(P)

def sigma(P):
    return tuple(sorted((frozenset(43 - x for x in s) for s in P), key=min))

def n1(P, Q):
    return sum(1 for a in P for b in Q if len(a & b) == 1)

CANDS = [
    ("VINCE 3799 {19..24}", [19, 20, 21, 22, 23, 24]),
    ("VINCE 3659 mod7", [4, 11, 18, 25, 32, 39]),
    ("VINCE 3671 coppie", [7, 8, 21, 22, 35, 36]),
    ("VINCE 3691 a=10", [10, 11, 12, 31, 32, 33]),
    ("QUASI a=7", [7, 8, 9, 34, 35, 36]),
    ("QUASI {2,4,19,24,39,41}", [2, 4, 19, 24, 39, 41]),
]

for label, omit in CANDS:
    parts = get_parts(omit)
    idx = {canon(P): i for i, P in enumerate(parts)}
    fixed = [i for i, P in enumerate(parts) if idx[canon(sigma(P))] == i]
    orth, near = [], []
    for i in range(len(parts)):
        for j in range(i + 1, len(parts)):
            v = n1(parts[i], parts[j])
            if v == 36:
                orth.append((i, j))
            elif v >= 29:
                near.append((i, j, v))
    print(f"\n=== {label}: {len(parts)} partizioni, sigma-fisse {len(fixed)} "
          f"{fixed}")
    for (i, j) in orth:
        si, sj = idx[canon(sigma(parts[i]))], idx[canon(sigma(parts[j]))]
        kind = ("ENTRAMBE FISSE" if (si, sj) == (i, j) else
                "SCAMBIATE (sigmaP=Q)" if {si, sj} == {i, j} else
                f"orbita con ({si},{sj})")
        print(f"  ortogonale ({i:>3},{j:>3})  sigma: {kind}")
    for (i, j, v) in near:
        si, sj = idx[canon(sigma(parts[i]))], idx[canon(sigma(parts[j]))]
        fi = "F" if si == i else "m"
        fj = "F" if sj == j else "m"
        print(f"  quasi n1={v} ({i:>3}{fi},{j:>3}{fj})", end="")
        # anatomia del difetto
        P, Q = parts[i], parts[j]
        twos = [(sorted(a & b)) for a in P for b in Q if len(a & b) == 2]
        print(f"  celle-2: {twos}")

# quadrato sigma-fisso esplicito dal vincitore 3799 (conteggio dispari)
print("\n--- quadrato con simmetria di complemento (da coppia sigma-fissa) ---")
parts = get_parts([19, 20, 21, 22, 23, 24])
idx = {canon(P): i for i, P in enumerate(parts)}
for i in range(len(parts)):
    for j in range(i + 1, len(parts)):
        if n1(parts[i], parts[j]) == 36:
            si, sj = idx[canon(sigma(parts[i]))], idx[canon(sigma(parts[j]))]
            if {si, sj} == {i, j}:
                P, Q = parts[i], parts[j]
                M = [[(P[r] & Q[c]).__iter__().__next__() for c in range(6)]
                     for r in range(6)]
                for row in M:
                    print("   ", " ".join(f"{v:>2}" for v in row))
                comp_rows = {frozenset(43 - v for v in row) for row in M}
                cols = {frozenset(M[r][c] for r in range(6)) for c in range(6)}
                print("    43-M ha per righe le colonne di M:",
                      comp_rows == cols,
                      f"  (tipo: {'scambiata' if si == j else 'fisse'})")
                break
    else:
        continue
    break
