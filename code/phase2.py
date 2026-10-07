"""Phase 2 in detail: how many DISTINCT number sets admit an optimal square,
and is every one of them centred?"""
import time
from bucket_sweep import buckets, bits, feasible
from semibimagic import columnize

M, C = 42, 43
t0 = time.time()
g = buckets(M)
lo_s, hi_s, lo_q, hi_q = feasible(M)
one, top = 1 << 1, 1 << M
on = []
for (S1, S2), v in g.items():
    if S1 != 129 or len(v) < 6:
        continue
    if not (lo_s <= 6 * S1 <= hi_s and lo_q <= 6 * S2 <= hi_q):
        continue
    if not any(m & one for m in v) or not any(m & top for m in v):
        continue
    on.append(((S1, S2), v))
on.sort(key=lambda kv: len(kv[1]))
print(f"S1=129 buckets: {len(on)}  [{time.time()-t0:.0f}s]", flush=True)

sets_found, parts, s2s = {}, 0, set()
for (S1, S2), masks in on:
    with_one = [m for m in masks if m & one]
    n = len(masks)

    def rec(chosen, used, start, has_top):
        global parts
        if len(chosen) == 6:
            if not has_top:
                return
            grid = columnize([bits(m) for m in chosen], S1, S2)
            if grid:
                parts += 1
                s2s.add(S2)
                key = tuple(sorted(v for r in grid for v in r))
                sets_found.setdefault(key, 0)
                sets_found[key] += 1
            return
        for i in range(start, n):
            m = masks[i]
            if m & used:
                continue
            rec(chosen + [m], used | m, i + 1, has_top or bool(m & top))

    for m0 in with_one:
        rec([m0], m0, 0, bool(m0 & top))

print(f"columnizable row-partitions : {parts}")
print(f"distinct number sets        : {len(sets_found)}")
print(f"distinct S2 values          : {sorted(s2s)}")
for k, c in sets_found.items():
    omitted = [x for x in range(1, M + 1) if x not in k]
    sym = all(C - v in k for v in k)
    print(f"  omits {omitted}  centred={sym}  ({c} partitions)")
print(f"\nALL CENTRED: {all(all(C - v in k for v in k) for k in sets_found)}"
      f"   [{time.time()-t0:.0f}s]")
