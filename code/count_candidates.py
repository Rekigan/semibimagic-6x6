"""Recompute the per-slot numbers of EXAMINED candidate sets of the
independent replication at MaxNb = 42 (Remark 4 of the paper), without
the 35-hour run.

The replication (replica_s1.py, function classifica) examines, for each
S1 in a slot, every 6-subset d of {1, ..., 41} (42 always stays in the
set) whose sum is 903 - 6*S1 and whose sum of squares q makes
(22631 - q) divisible by 6. This script counts those subsets in two
ways:
  (a) with the same enumeration routine (replica_s1.subsets_k) and the
      same conditions as classifica();
  (b) independently, by brute force over all C(41, 6) = 4,496,388
      subsets.
Expected, written before the run (the TOTALE lines of the four
replication runs, logs/replica-full-totals.md): 84948, 76605, 76605,
84948 for the slots 112-126, 127-129, 130-132, 133-147.

Usage:  python code/count_candidates.py  > logs/count-candidates.log
"""
import os
import sys
import time
from itertools import combinations

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from replica_s1 import subsets_k

M = 42
TOT = M * (M + 1) // 2                      # 903
TOTQ = M * (M + 1) * (2 * M + 1) // 6       # 25585
SLOTS = [(112, 126), (127, 129), (130, 132), (133, 147)]
EXPECTED = [84948, 76605, 76605, 84948]

print(__doc__)
t0 = time.time()

# (a) same routine and conditions as replica_s1.classifica()
count_a = {}
for s1 in range(112, 148):
    dropsum = TOT - 6 * s1
    if dropsum < sum(range(1, 7)) or dropsum > sum(range(M - 6, M)):
        count_a[s1] = 0
        continue
    drops = subsets_k(range(1, M), 6, dropsum, 0, 10 ** 9)
    count_a[s1] = sum(1 for d in drops
                      if (TOTQ - sum(x * x for x in d)) % 6 == 0)

# (b) brute force over all 6-subsets of {1..41}
count_b = {}
for d in combinations(range(1, M), 6):
    s = TOT - sum(d)
    if s % 6:
        continue
    if (TOTQ - sum(x * x for x in d)) % 6:
        continue
    s1 = s // 6
    count_b[s1] = count_b.get(s1, 0) + 1

ok = True
for (lo, hi), exp in zip(SLOTS, EXPECTED):
    a = sum(count_a.get(s1, 0) for s1 in range(lo, hi + 1))
    b = sum(count_b.get(s1, 0) for s1 in range(lo, hi + 1))
    good = (a == b == exp)
    ok &= good
    print(f"slot S1 {lo}-{hi}: (a) {a}  (b) {b}  expected {exp}  "
          f"{'OK' if good else 'MISMATCH'}")
outside = sum(v for s1, v in count_b.items() if not 112 <= s1 <= 147)
print(f"candidates with S1 outside [112, 147]: {outside}")
print(f"total examined: {sum(count_a.values())}")
print(f"mirror identity S1 <-> 259 - S1 on the per-stratum counts: "
      f"{all(count_b.get(s1, 0) == count_b.get(259 - s1, 0) for s1 in range(112, 148))}")
print("RESULT:", "AS EXPECTED" if ok else "DIFFERENT FROM EXPECTED")
print(f"time {time.time() - t0:.0f}s")
