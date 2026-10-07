"""Find the SMALLEST semi-bimagic square of order 6:
minimise the largest entry M, over all sets of 36 distinct integers in [1, M].
"""
import sys, time
from itertools import combinations
from semibimagic import find_subsets, partitions, columnize, show

def try_set(nums, budget=None):
    tot, totq = sum(nums), sum(x * x for x in nums)
    if tot % 6 or totq % 6:
        return None, 0
    S1, S2 = tot // 6, totq // 6
    subs = find_subsets(nums, 6, S1, S2)
    if len(subs) < 6:
        return None, len(subs)
    n = 0
    for part in partitions(subs, nums):
        n += 1
        g = columnize(part, S1, S2)
        if g:
            return g, len(subs)
        if budget and n > budget:
            return "BUDGET", len(subs)
    return None, len(subs)

def sweep(Mmax=44, Mmin=36):
    for M in range(Mmin, Mmax + 1):
        drop = M - 36
        t0 = time.time()
        tested = considered = 0
        for omit in combinations(range(1, M + 1), drop):
            if M not in omit:  # M itself must be present, else max < M (already tested)
                nums = [x for x in range(1, M + 1) if x not in omit]
                considered += 1
                g, ns = try_set(nums)
                if g == "BUDGET":
                    print(f"M={M} omit={omit} budget exceeded"); continue
                if g:
                    print(f"\n*** SEMI-BIMAGIC FOUND, max entry M={M}, omitting {omit} ***")
                    show(g)
                    return M, omit, g
                if ns >= 6:
                    tested += 1
        print(f"M={M}: {considered} sets, {tested} with enough sextets, "
              f"none works  ({time.time()-t0:.1f}s)", flush=True)
    return None

if __name__ == "__main__":
    sweep(int(sys.argv[1]) if len(sys.argv) > 1 else 44,
          int(sys.argv[2]) if len(sys.argv) > 2 else 36)
