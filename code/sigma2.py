"""Chiusura dei due fili.

A. sigma-struttura dei quadrati ottimali:
   - 3799/3659 (5 coppie, dispari): la coppia sigma-fissa da' un quadrato
     AUTO-COMPLEMENTARE (43-M = M a meno di permutazioni di righe/colonne)
   - 3671/3691 (2 coppie in un'orbita): i due quadrati sono SCAMBIATI dal
     complemento (43-M1 ~ M2)
B. dicotomia dei difetti sull'INTERA popolazione delle coppie a n1=32
   (30 in tutto il campo simmetrico): somme delle celle-2 uguali nei
   vincitori, disuguali nei quasi-vincitori?
"""
from semibimagic import find_subsets, partitions

def get_parts(omit):
    nums = [x for x in range(1, 43) if x not in omit]
    S1, S2 = sum(nums) // 6, sum(x * x for x in nums) // 6
    subs = find_subsets(nums, 6, S1, S2)
    return [tuple(sorted((frozenset(s) for s in p), key=min))
            for p in partitions(subs, nums)]

def n1(P, Q):
    return sum(1 for a in P for b in Q if len(a & b) == 1)

def square(P, Q):
    return [[next(iter(P[r] & Q[c])) for c in range(6)] for r in range(6)]

def same_up_to_perms(A, B):
    """B = A a meno di permutazioni di righe e colonne?"""
    rowsA = [frozenset(r) for r in A]
    rowsB = [frozenset(r) for r in B]
    if sorted(rowsA, key=min) != sorted(rowsB, key=min):
        return False
    colsA = [frozenset(A[r][c] for r in range(6)) for c in range(6)]
    colsB = [frozenset(B[r][c] for r in range(6)) for c in range(6)]
    return sorted(colsA, key=min) == sorted(colsB, key=min)

print("--- A. sigma-struttura dei quadrati ---")
P37 = get_parts([19, 20, 21, 22, 23, 24])
M = square(P37[13], P37[32])
C = [[43 - v for v in row] for row in M]
print("3799, coppia fissa (13,32): 43-M = M a meno di permutazioni:",
      same_up_to_perms(M, C))

P71 = get_parts([7, 8, 21, 22, 35, 36])
M1 = square(P71[4], P71[38])
M2 = square(P71[12], P71[31])
C1 = [[43 - v for v in row] for row in M1]
print("3671, orbita {(4,38),(12,31)}: 43-M1 = M2 a meno di permutazioni:",
      same_up_to_perms(C1, M2))

P91 = get_parts([10, 11, 12, 31, 32, 33])
N1_ = square(P91[1], P91[38])
N2_ = square(P91[12], P91[27])
D1 = [[43 - v for v in row] for row in N1_]
print("3691, orbita {(1,38),(12,27)}: 43-M1 = M2 a meno di permutazioni:",
      same_up_to_perms(D1, N2_))

print("\n--- B. dicotomia dei difetti (tutte le 30 coppie a n1=32) ---")
HOSTS = [("VINCE 3799", [19, 20, 21, 22, 23, 24]),
         ("VINCE 3659", [4, 11, 18, 25, 32, 39]),
         ("VINCE 3671", [7, 8, 21, 22, 35, 36]),
         ("VINCE 3691", [10, 11, 12, 31, 32, 33]),
         ("QUASI a=7", [7, 8, 9, 34, 35, 36]),
         ("QUASI 2-4", [2, 4, 19, 24, 39, 41])]
tot = {"vincitori": [0, 0], "quasi": [0, 0]}   # [somme uguali, disuguali]
for label, omit in HOSTS:
    parts = get_parts(omit)
    kind = "vincitori" if label.startswith("V") else "quasi"
    for i in range(len(parts)):
        for j in range(i + 1, len(parts)):
            if n1(parts[i], parts[j]) == 32:
                twos = [sorted(a & b) for a in parts[i] for b in parts[j]
                        if len(a & b) == 2]
                sums = [sum(c) for c in twos]
                eq = sums[0] == sums[1]
                tot[kind][0 if eq else 1] += 1
print(f"vincitori : celle-2 a somme uguali {tot['vincitori'][0]}, "
      f"disuguali {tot['vincitori'][1]}")
print(f"quasi     : celle-2 a somme uguali {tot['quasi'][0]}, "
      f"disuguali {tot['quasi'][1]}")
print("\n(30 coppie = popolazione completa del campo simmetrico, non campione)")
