"""Semi-bimagic squares of order 6: exhaustive machinery.

A 6x6 square is SEMI-BIMAGIC if all 6 rows and all 6 columns have the same
sum S1 and the same sum of squares S2.  (Diagonals not required.)

Strategy:
  1. enumerate all 6-subsets of the given number set with sum S1, sqsum S2
  2. exact-cover them into a row partition (6 disjoint subsets covering all 36)
  3. for each row partition, build the columns one at a time: pick one element
     from each row, with prefix pruning on sum / sum-of-squares
"""
import sys
from itertools import combinations


def find_subsets(nums, k, S1, S2):
    nums = sorted(nums)
    n = len(nums)
    sq = [x * x for x in nums]
    res = []

    def rec(i, kk, s, q, cur):
        if kk == 0:
            if s == S1 and q == S2:
                res.append(tuple(cur))
            return
        if n - i < kk:
            return
        if s + sum(nums[i:i + kk]) > S1 or s + sum(nums[n - kk:]) < S1:
            return
        if q + sum(sq[i:i + kk]) > S2 or q + sum(sq[n - kk:]) < S2:
            return
        for j in range(i, n - kk + 1):
            cur.append(nums[j])
            rec(j + 1, kk - 1, s + nums[j], q + sq[j], cur)
            cur.pop()
    rec(0, k, 0, 0, [])
    return res


def partitions(subsets, nums):
    """Generate all partitions of `nums` into 6 of the given subsets."""
    idx = {v: i for i, v in enumerate(sorted(nums))}
    masks = []
    for s in subsets:
        m = 0
        for v in s:
            m |= 1 << idx[v]
        masks.append((m, s))
    full = (1 << len(nums)) - 1
    by_low = {}
    for m, s in masks:
        low = (m & -m).bit_length() - 1
        by_low.setdefault(low, []).append((m, s))

    def rec(used, acc):
        if used == full:
            yield list(acc)
            return
        low = ((~used) & full)
        low = (low & -low).bit_length() - 1
        for m, s in by_low.get(low, ()):
            if m & used:
                continue
            acc.append(s)
            yield from rec(used | m, acc)
            acc.pop()
    yield from rec(0, [])


def columnize(rows, S1, S2):
    """rows: list of 6 lists. Return a 6x6 grid whose columns also hit S1/S2.

    Columns are interchangeable, so we may demand that the row-0 entries
    increase from left to right: that alone divides the work by 6! = 720.
    """
    rows = [sorted(r) for r in rows]
    sq = [[v * v for v in r] for r in rows]
    avail = [0b111111] * 6            # which positions of each row are free
    grid = [[0] * 6 for _ in range(6)]

    def build_col(c, r, s, q, chosen, lb):
        if r == 6:
            if s == S1 and q == S2:
                for i in range(6):
                    avail[i] &= ~(1 << chosen[i])
                    grid[i][c] = rows[i][chosen[i]]
                if c == 5 or place(c + 1):
                    return True
                for i in range(6):
                    avail[i] |= 1 << chosen[i]
            return False
        lo = hi = loq = hiq = 0
        for i in range(r, 6):
            m = avail[i]
            a = (m & -m).bit_length() - 1     # smallest free position
            b = m.bit_length() - 1            # largest free position
            lo += rows[i][a]; hi += rows[i][b]
            loq += sq[i][a];  hiq += sq[i][b]
        if s + lo > S1 or s + hi < S1 or q + loq > S2 or q + hiq < S2:
            return False
        m = avail[r]
        while m:
            p = (m & -m).bit_length() - 1
            m &= m - 1
            if r == 0 and rows[0][p] < lb:
                continue
            chosen.append(p)
            if build_col(c, r + 1, s + rows[r][p], q + sq[r][p], chosen, lb):
                return True
            chosen.pop()
        return False

    def place(c):
        if c == 6:
            return True
        return build_col(c, 0, 0, 0, [], grid[0][c - 1] + 1 if c else 0)

    if place(0):
        return grid
    return None


def solve(nums, verbose=True, max_parts=None):
    tot = sum(nums)
    totq = sum(x * x for x in nums)
    if tot % 6 or totq % 6:
        if verbose:
            print("  sums not divisible by 6 -> impossible")
        return None
    S1, S2 = tot // 6, totq // 6
    subs = find_subsets(nums, 6, S1, S2)
    if verbose:
        print(f"  S1={S1} S2={S2}  bimagic sextets: {len(subs)}")
    if not subs:
        return None
    cnt = 0
    for part in partitions(subs, nums):
        cnt += 1
        g = columnize(part, S1, S2)
        if g:
            if verbose:
                print(f"  FOUND after {cnt} row-partitions")
            return g
        if max_parts and cnt >= max_parts:
            if verbose:
                print(f"  gave up after {cnt} row-partitions")
            return None
    if verbose:
        print(f"  exhausted: {cnt} row-partitions, none columnizable")
    return None


def show(g):
    for row in g:
        print(" ".join(f"{v:3d}" for v in row))
    print("  row sums   :", [sum(r) for r in g])
    print("  row sqsums :", [sum(v * v for v in r) for r in g])
    cols = list(zip(*g))
    print("  col sums   :", [sum(c) for c in cols])
    print("  col sqsums :", [sum(v * v for v in c) for c in cols])
    d1 = [g[i][i] for i in range(6)]
    d2 = [g[i][5 - i] for i in range(6)]
    print("  diagonals  :", sum(d1), sum(d2), "| squares:",
          sum(v * v for v in d1), sum(v * v for v in d2))


if __name__ == "__main__":
    print("=== normal case: 1..36 ===")
    g = solve(list(range(1, 37)))
    if g:
        show(g)
