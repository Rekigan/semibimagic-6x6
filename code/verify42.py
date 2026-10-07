"""Independent audit of the max=42 semi-bimagic square found by the sweep."""
from records import audit

G = [[1, 6, 26, 29, 33, 34],
     [27, 28, 31, 36, 2, 5],
     [32, 35, 3, 4, 25, 30],
     [40, 39, 17, 14, 12, 7],
     [11, 8, 42, 37, 16, 15],
     [18, 13, 10, 9, 41, 38]]

audit(G, "sweep result, max = 42")

vals = sorted(v for r in G for v in r)
missing = [k for k in range(1, 43) if k not in vals]
print(f"\n  36 distinct integers in 1..42, omitting {missing}")
print(f"  omitted six sum to {sum(missing)}  (= S1)")
print(f"  total sum   {sum(vals)} = 6*{sum(vals)//6}")
print(f"  total sqsum {sum(v*v for v in vals)} = 6*{sum(v*v for v in vals)//6}")
print(f"  distinct: {len(set(vals)) == 36}, min {min(vals)}, max {max(vals)}")
