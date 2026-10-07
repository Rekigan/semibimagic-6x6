"""Independent check of Proposition 5 (lifting of the mirror symmetry),
written 2026-08-08 to close the two gaps of the sigma-struttura log.

Il log di sigma2.py testava: 3799 auto-complementare (True), 3671 complemento
liscio (True), 3691 complemento liscio (False) - e NON testava 3659 ne' il
trasposto per 3691. Qui: per OGNI vincitore, tutte le coppie ortogonali,
azione di sigma, e per ogni orbita/fissa ENTRAMBE le forme (43-M ~ M2 e
43-M ~ M2^T). Il teorema di sollevamento e' verificato solo se ogni riga
scatta in almeno una forma.
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


def transpose(M):
    return [[M[c][r] for c in range(6)] for r in range(6)]


def comp(M):
    return [[43 - v for v in row] for row in M]


def same_up_to_perms(A, B):
    rowsA = [frozenset(r) for r in A]
    rowsB = [frozenset(r) for r in B]
    if sorted(rowsA, key=min) != sorted(rowsB, key=min):
        return False
    colsA = [frozenset(A[r][c] for r in range(6)) for c in range(6)]
    colsB = [frozenset(B[r][c] for r in range(6)) for c in range(6)]
    return sorted(colsA, key=min) == sorted(colsB, key=min)


def sigma_part(P):
    return tuple(sorted((frozenset(43 - x for x in s) for s in P), key=min))


WINNERS = [("3799", [19, 20, 21, 22, 23, 24]),
           ("3659", [4, 11, 18, 25, 32, 39]),
           ("3671", [7, 8, 21, 22, 35, 36]),
           ("3691", [10, 11, 12, 31, 32, 33])]

all_ok = True
for name, omit in WINNERS:
    parts = get_parts(omit)
    idx = {p: i for i, p in enumerate(parts)}
    orto = [(i, j) for i in range(len(parts)) for j in range(i + 1, len(parts))
            if n1(parts[i], parts[j]) == 36]
    print(f"== {name}: {len(parts)} partizioni, {len(orto)} coppie ortogonali "
          f"{orto}")
    seen = set()
    for (i, j) in orto:
        si, sj = idx[sigma_part(parts[i])], idx[sigma_part(parts[j])]
        pair_img = (min(si, sj), max(si, sj))
        key = frozenset([(i, j), pair_img])
        if key in seen:
            continue
        seen.add(key)
        M1 = square(parts[i], parts[j])
        if {si, sj} == {i, j}:
            ok_self = same_up_to_perms(comp(M1), M1)
            ok_selfT = same_up_to_perms(comp(M1), transpose(M1))
            verdict = ok_self or ok_selfT
            all_ok &= verdict
            print(f"  ({i},{j}) SIGMA-FISSA: 43-M ~ M: {ok_self} ; "
                  f"43-M ~ M^T: {ok_selfT}  -> {'OK' if verdict else 'BUCO'}")
        else:
            assert pair_img in orto, "l'immagine sigma non e' ortogonale?!"
            M2 = square(parts[pair_img[0]], parts[pair_img[1]])
            ok = same_up_to_perms(comp(M1), M2)
            okT = same_up_to_perms(comp(M1), transpose(M2))
            verdict = ok or okT
            all_ok &= verdict
            print(f"  ({i},{j}) orbita con {pair_img}: 43-M1 ~ M2: {ok} ; "
                  f"43-M1 ~ M2^T: {okT}  -> {'OK' if verdict else 'BUCO'}")

print()
print("TEOREMA DI SOLLEVAMENTO:",
      "VERIFICATO SU TUTTE LE COPPIE" if all_ok else "HA UN BUCO - vedi sopra")
