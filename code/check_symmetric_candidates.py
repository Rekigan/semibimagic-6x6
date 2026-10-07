"""Arithmetic facts on the mirror-symmetric candidate sets at MaxNb = 42
(Section 5 of the paper: "Where candidates die").

Facts checked:
  1. among triples of complementary pairs (a, 43-a) with omitted sqsum 3631,
     exactly 8 exist, one of which contains the pair {1,42} -> 7 admissible
  2. our S2-minimal omitted set {4,11,18,25,32,39} is one of those 7
  3. 546 symmetric triples pass the necessary arithmetic conditions
  4. the example omit-{2,3,4,39,40,41}: IS it centred? what S2 would it give?
"""
from itertools import combinations

TOT_SQ = sum(k * k for k in range(1, 43))     # 25585
pairs = [(a, 43 - a) for a in range(1, 22)]   # 21 complementary pairs

# --- claims 1 and 2 ---
trip3631 = []
for t in combinations(pairs, 3):
    vals = [x for p in t for x in p]
    if sum(x * x for x in vals) == 3631:
        trip3631.append(sorted(vals))
print(f"symmetric triples with omitted sqsum 3631 : {len(trip3631)}")
with142 = [t for t in trip3631 if 1 in t]
print(f"  of which containing the pair (1,42)     : {len(with142)}")
print(f"  admissible (without 1,42)               : {len(trip3631) - len(with142)}")
ours = [4, 11, 18, 25, 32, 39]
print(f"  ours {ours} among them                  : {ours in trip3631}")

# --- claim 3: necessary conditions on a symmetric triple ---
# S1 = 129 automatic (each pair sums 43). Remaining sqsum divisible by 6,
# and the pair (1,42) must NOT be omitted (1 and 42 must be in the square).
ok = []
for t in combinations(pairs, 3):
    vals = [x for p in t for x in p]
    if 1 in vals:
        continue
    if (TOT_SQ - sum(x * x for x in vals)) % 6 == 0:
        ok.append(vals)
print(f"\nsymmetric triples passing necessary conditions: {len(ok)}"
      f"   (expected 546)")

# --- claim 4 ---
ex = [2, 3, 4, 39, 40, 41]
centred = all((43 - v) in ex for v in ex)
S2 = (TOT_SQ - sum(x * x for x in ex)) // 6
print(f"\nomit {ex}: centred = {centred}, would give S2 = {S2}")
print("  (it is centred: 2+41=3+40=4+39=43)")
print(f"  S2 = {S2} < 3659, arithmetic allows it, enumeration excludes it:")
print("  the reduction to four sets is empirical content.")

# --- bonus: S2 landscape of admissible symmetric triples ---
s2s = sorted({(TOT_SQ - sum(x * x for x in v)) // 6 for v in ok})
print(f"\nS2 values arithmetic allows: {len(s2s)}, min {s2s[0]}, max {s2s[-1]}")
print(f"realised by actual squares  : [3659, 3671, 3691, 3799]  (4 of {len(ok)})")
