"""Scenario A or B: must every optimal (max = 42) semi-bimagic square have a
centred number set?

Any optimal solution has min = 1 and max = 42 (translation argument), so if its
set is symmetric the centre must be 21.5, which forces S1 = 3*43 = 129.
Hence:  S1 != 129  =>  NOT centred.

Phase 1 searches every bucket with S1 != 129.  One solution there settles
Scenario B outright.
Phase 2 sweeps the S1 = 129 buckets and tests each solution for symmetry.
"""
import sys, time
from bucket_sweep import buckets, bits, feasible
from semibimagic import columnize, show

M = 42
C = M + 1


def solutions(masks, S1, S2, want_all=False, deadline=None):
    one, top = 1 << 1, 1 << M
    with_one = [m for m in masks if m & one]
    if not with_one or not any(m & top for m in masks):
        return []
    n = len(masks)
    out = []

    def rec(chosen, used, start, has_top):
        if deadline and time.time() > deadline:
            raise TimeoutError
        if len(chosen) == 6:
            if not has_top:
                return False
            g = columnize([bits(m) for m in chosen], S1, S2)
            if g:
                out.append(g)
                return not want_all
            return False
        for i in range(start, n):
            m = masks[i]
            if m & used:
                continue
            if rec(chosen + [m], used | m, i + 1, has_top or bool(m & top)):
                return True
        return False

    for m0 in with_one:
        if rec([m0], m0, 0, bool(m0 & top)):
            break
    return out


def centred(g):
    vals = {v for r in g for v in r}
    return all(C - v in vals for v in vals)


t0 = time.time()
g = buckets(M)
lo_s, hi_s, lo_q, hi_q = feasible(M)
one, top = 1 << 1, 1 << M
cand = []
for (S1, S2), v in g.items():
    if len(v) < 6 or not (lo_s <= 6 * S1 <= hi_s and lo_q <= 6 * S2 <= hi_q):
        continue
    if not any(m & one for m in v) or not any(m & top for m in v):
        continue
    cand.append(((S1, S2), v))
cand.sort(key=lambda kv: len(kv[1]))

off = [c for c in cand if c[0][0] != 129]
on = [c for c in cand if c[0][0] == 129]
print(f"M=42: {len(cand)} feasible buckets  ->  {len(off)} with S1 != 129, "
      f"{len(on)} with S1 = 129   [{time.time()-t0:.0f}s]", flush=True)

print("\nPHASE 1: any solution with S1 != 129 settles Scenario B")
found_b = None
for i, ((S1, S2), masks) in enumerate(off):
    try:
        sols = solutions(masks, S1, S2)
    except TimeoutError:
        continue
    if sols:
        found_b = (S1, S2, sols[0])
        break
    if i % 500 == 0 and i:
        print(f"  ...{i}/{len(off)} buckets, {time.time()-t0:.0f}s", flush=True)

if found_b:
    S1, S2, sq = found_b
    print(f"\n*** SCENARIO B: solution with S1={S1} (not 129) => NOT centred "
          f"[{time.time()-t0:.0f}s] ***")
    show(sq)
    print("  centred:", centred(sq))
else:
    print(f"  none: every optimal solution has S1 = 129 "
          f"[{time.time()-t0:.0f}s]", flush=True)
    print("\nPHASE 2: are all S1=129 solutions symmetric?")
    tot = ncent = 0
    for (S1, S2), masks in on:
        try:
            sols = solutions(masks, S1, S2, want_all=True,
                             deadline=time.time() + 900)
        except TimeoutError:
            print(f"  bucket S2={S2} timed out, partial", flush=True)
            continue
        for sq in sols:
            tot += 1
            if centred(sq):
                ncent += 1
            else:
                print(f"\n*** SCENARIO B: S1=129 but NOT centred ***")
                show(sq)
                sys.exit()
    print(f"  solutions examined: {tot}, all centred: {ncent == tot}")
