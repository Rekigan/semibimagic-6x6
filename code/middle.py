"""The middle number: of the 546 arithmetic candidates (symmetric triples),
how many admit at least one row partition?  How many at least one square?

This also independently re-confirms 'exactly 4' WITHIN the symmetric class
(phase 1 already covered the non-symmetric side exhaustively).
"""
import json, os, time
from itertools import combinations
from semibimagic import find_subsets, partitions, columnize

TOT_SQ = sum(k * k for k in range(1, 43))
pairs = [(a, 43 - a) for a in range(2, 22)]   # 20 pairs, (1,42) never omitted

cands = []
for t in combinations(pairs, 3):
    omit = sorted(x for p in t for x in p)
    if (TOT_SQ - sum(x * x for x in omit)) % 6 == 0:
        cands.append(omit)
print(f"arithmetic candidates: {len(cands)}", flush=True)

t0 = time.time()
stats = {"no_sextet_cover": 0, "no_partition": 0,
         "partition_no_square": 0, "square": 0}
detail = []
for i, omit in enumerate(cands):
    nums = [k for k in range(1, 43) if k not in omit]
    S1 = 129
    S2 = (TOT_SQ - sum(x * x for x in omit)) // 6
    subs = find_subsets(nums, 6, S1, S2)
    total = ext = 0
    for part in partitions(subs, nums):
        total += 1
        if ext == 0 and columnize(part, S1, S2):
            ext += 1          # one square is enough for the middle number
    if total == 0:
        stats["no_partition" if subs else "no_sextet_cover"] += 1
    elif ext == 0:
        stats["partition_no_square"] += 1
        detail.append({"omit": omit, "S2": S2, "partitions": total})
    else:
        stats["square"] += 1
        detail.append({"omit": omit, "S2": S2, "partitions": total,
                       "square": True})
    if (i + 1) % 50 == 0:
        print(f"  {i+1}/{len(cands)}  [{time.time()-t0:.0f}s]  {stats}",
              flush=True)

print(f"\nFINAL  [{time.time()-t0:.0f}s]")
print(f"  546 arithmetic candidates")
print(f"  with >=1 row partition : "
      f"{stats['partition_no_square'] + stats['square']}")
print(f"  with >=1 square        : {stats['square']}")
print(f"  breakdown: {stats}")

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data",
                       "middle-number.json"), "w") as f:
    json.dump({"stats": stats, "sets_with_partitions": detail}, f, indent=1)
print("dumped middle-number.json")
