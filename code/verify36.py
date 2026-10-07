"""Independent brute-force check of the 1..36 case."""
from itertools import combinations
from semibimagic import find_subsets, partitions, columnize

S1, S2 = 111, 2701
nums = list(range(1, 37))

# brute force all C(36,6) = 1947792 sextets
brute = [c for c in combinations(nums, 6)
         if sum(c) == S1 and sum(x * x for x in c) == S2]
smart = find_subsets(nums, 6, S1, S2)
print("brute force sextets:", len(brute))
print("pruned search      :", len(smart))
print("identical sets     :", set(brute) == set(smart))

parts = list(partitions(smart, nums))
print("row partitions     :", len(parts))
for i, p in enumerate(parts):
    ok = all(sum(r) == S1 and sum(x * x for x in r) == S2 for r in p)
    covers = sorted(x for r in p for x in r) == nums
    print(f"  #{i+1}: {[list(r) for r in p]}  valid={ok} covers={covers}"
          f"  columnizable={columnize(p, S1, S2) is not None}")
