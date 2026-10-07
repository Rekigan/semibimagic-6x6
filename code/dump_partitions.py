"""For each optimal set (and the 3459 negative): count ALL row partitions,
count those that extend to a square, and dump both in canonical JSON for a
cross-membership check against the expected counts.
"""
import json, os, time
from semibimagic import find_subsets, partitions, columnize

SETS = {
    "3799": [19, 20, 21, 22, 23, 24],
    "3659": [4, 11, 18, 25, 32, 39],
    "3671": [7, 8, 21, 22, 35, 36],
    "3691": [10, 11, 12, 31, 32, 33],
    "3459-negative": [2, 3, 4, 39, 40, 41],
}

out = {}
for label, omit in SETS.items():
    nums = [k for k in range(1, 43) if k not in omit]
    S1 = sum(nums) // 6
    S2 = sum(x * x for x in nums) // 6
    t0 = time.time()
    subs = find_subsets(nums, 6, S1, S2)
    total = 0
    extendable = []
    for part in partitions(subs, nums):
        total += 1
        if columnize(part, S1, S2):
            extendable.append(sorted(sorted(row) for row in part))
    out[label] = {
        "omitted": omit, "S1": S1, "S2": S2,
        "bimagic_sextets": len(subs),
        "row_partitions_total": total,
        "row_partitions_extendable": len(extendable),
        "extendable_partitions": extendable,
    }
    print(f"{label:>14}: sextets {len(subs):>3}  partitions {total:>3}  "
          f"extendable {len(extendable)}  [{time.time()-t0:.1f}s]", flush=True)

tot = sum(v["row_partitions_total"] for k, v in out.items()
          if k != "3459-negative")
ext = sum(v["row_partitions_extendable"] for k, v in out.items()
          if k != "3459-negative")
print(f"\nfour optimal sets: {tot} row partitions total, {ext} extendable")
print("expected         : 324 total (132+50+83+59), 24 extendable, "
      "and 6/0 for the negative")

path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data",
                    "partitions-max42.json")
with open(path, "w") as f:
    json.dump(out, f, indent=1)
print("\ndumped to data/partitions-max42.json")
