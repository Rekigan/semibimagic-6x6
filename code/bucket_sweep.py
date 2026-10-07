"""Smallest semi-bimagic 6x6, done properly.

Instead of looping over every 36-element subset of [1..M] (C(M-2, M-36) of
them, which explodes), enumerate ALL 6-subsets of [1..M] once, bucket them by
(sum, sum of squares), and look inside each bucket for six pairwise disjoint
sextets that can then be columnised.  The number set falls out of the choice.

Two sound restrictions, applied as filters:
  * the partition must use M      (otherwise the max is < M: already covered)
  * the partition must use 1      (semi-bimagic is translation invariant, so a
                                   solution with min > 1 shifts down to a
                                   smaller max: also already covered)
"""
import sys, time
from collections import defaultdict
from semibimagic import columnize, show


def buckets(M):
    g = defaultdict(list)
    sq = [i * i for i in range(M + 1)]
    for a in range(1, M - 4):
        sa, qa, ma = a, sq[a], 1 << a
        for b in range(a + 1, M - 3):
            sb, qb, mb = sa + b, qa + sq[b], ma | 1 << b
            for c in range(b + 1, M - 2):
                sc, qc, mc = sb + c, qb + sq[c], mb | 1 << c
                for d in range(c + 1, M - 1):
                    sd, qd, md = sc + d, qc + sq[d], mc | 1 << d
                    for e in range(d + 1, M):
                        se, qe, me = sd + e, qd + sq[e], md | 1 << e
                        for f in range(e + 1, M + 1):
                            g[(se + f, qe + sq[f])].append(me | 1 << f)
    return g


def bits(m):
    out = []
    while m:
        low = m & -m
        out.append(low.bit_length() - 1)
        m ^= low
    return out


def search_bucket(masks, M, S1, S2):
    """six pairwise disjoint masks, one containing 1, one containing M"""
    one = 1 << 1
    top = 1 << M
    with_one = [m for m in masks if m & one]
    if not with_one:
        return None
    if not any(m & top for m in masks):
        return None
    n = len(masks)

    def rec(chosen, used, start, has_top):
        if len(chosen) == 6:
            if not has_top:
                return None
            rows = [bits(m) for m in chosen]
            return columnize(rows, S1, S2)
        # prune: not enough room left for the numbers still needed
        for i in range(start, n):
            m = masks[i]
            if m & used:
                continue
            r = rec(chosen + [m], used | m, i + 1, has_top or bool(m & top))
            if r:
                return r
        return None

    for m0 in with_one:
        r = rec([m0], m0, 0, bool(m0 & top))
        if r:
            return r
    return None


def feasible(M):
    """the 36 numbers are distinct in [1,M] and include both 1 and M, which
    pins 6*S1 and 6*S2 to narrow windows"""
    mid_lo = list(range(2, 36))                  # 34 smallest fillers
    mid_hi = list(range(M - 34, M))              # 34 largest fillers
    lo_s = 1 + M + sum(mid_lo)
    hi_s = 1 + M + sum(mid_hi)
    lo_q = 1 + M * M + sum(k * k for k in mid_lo)
    hi_q = 1 + M * M + sum(k * k for k in mid_hi)
    return lo_s, hi_s, lo_q, hi_q


def run(M, verbose=True):
    t0 = time.time()
    g = buckets(M)
    lo_s, hi_s, lo_q, hi_q = feasible(M)
    if verbose:
        print(f"M={M}: {sum(len(v) for v in g.values())} sextets in "
              f"{len(g)} (S1,S2) buckets  [{time.time()-t0:.1f}s]")
        print(f"  feasible windows: 6*S1 in [{lo_s},{hi_s}], "
              f"6*S2 in [{lo_q},{hi_q}]", flush=True)
    one, top = 1 << 1, 1 << M
    cand = []
    for (S1, S2), v in g.items():
        if len(v) < 6:
            continue
        if not (lo_s <= 6 * S1 <= hi_s and lo_q <= 6 * S2 <= hi_q):
            continue
        if not any(m & one for m in v) or not any(m & top for m in v):
            continue
        cand.append(((S1, S2), v))
    cand.sort(key=lambda kv: len(kv[1]))
    if verbose:
        print(f"  buckets with >=6 sextets: {len(cand)}", flush=True)
    for (S1, S2), masks in cand:
        res = search_bucket(masks, M, S1, S2)
        if res:
            print(f"\n*** FOUND: max={M}, S1={S1}, S2={S2} "
                  f"[{time.time()-t0:.1f}s] ***")
            show(res)
            return res
    if verbose:
        print(f"  M={M}: NO semi-bimagic square  [{time.time()-t0:.1f}s]",
              flush=True)
    return None


if __name__ == "__main__":
    lo = int(sys.argv[1]) if len(sys.argv) > 1 else 39
    hi = int(sys.argv[2]) if len(sys.argv) > 2 else lo
    for M in range(lo, hi + 1):
        if run(M):
            break
