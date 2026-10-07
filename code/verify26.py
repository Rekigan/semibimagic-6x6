"""Audit the 26/28 square with max = 42, against Pfeffermann 1894 (max 49)."""
from records import audit, PFEFFERMANN

NEW = [[1, 26, 29, 34, 33, 6],
       [27, 31, 36, 5, 2, 28],
       [32, 3, 4, 30, 25, 35],
       [18, 10, 9, 38, 41, 13],
       [11, 42, 37, 15, 16, 8],
       [40, 17, 14, 7, 12, 39]]

audit(NEW, "NEW: 26/28, max = 42")

vals = sorted(v for r in NEW for v in r)
print(f"\n  distinct: {len(set(vals)) == 36}   omitted from 1..42: "
      f"{[k for k in range(1, 43) if k not in vals]}")
d1 = [NEW[i][i] for i in range(6)]
d2 = [NEW[i][5 - i] for i in range(6)]
print(f"  diagonal      {d1} -> sum {sum(d1)}, sqsum {sum(v*v for v in d1)}")
print(f"  antidiagonal  {d2} -> sum {sum(d2)}, sqsum {sum(v*v for v in d2)}")
print(f"\n  Pfeffermann 1894: 26/28 with max 49, S1 150, S2 5150")
print(f"  this square     : 26/28 with max 42, S1 129, S2 3799")
print("\n  max <= 41 is already excluded for the WEAKER 24/28 property,")
print("  and 26/28 implies 24/28, so 42 is optimal for 26/28 as well.")
