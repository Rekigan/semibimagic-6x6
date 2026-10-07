"""Independent verification of the published order-6 records."""

def audit(g, name):
    n = len(g)
    vals = [v for r in g for v in r]
    lines = {}
    for i, r in enumerate(g):
        lines[f"row{i}"] = r
    for j in range(n):
        lines[f"col{j}"] = [g[i][j] for i in range(n)]
    lines["diag"] = [g[i][i] for i in range(n)]
    lines["anti"] = [g[i][n - 1 - i] for i in range(n)]
    S1 = sum(g[0])
    S2 = sum(v * v for v in g[0])
    good1 = [k for k, L in lines.items() if sum(L) == S1]
    good2 = [k for k, L in lines.items() if sum(v * v for v in L) == S2]
    bad = [k for k in lines if k not in good1] + \
          [k + "^2" for k in lines if k not in good2]
    print(f"\n{name}")
    print(f"  distinct: {len(set(vals)) == len(vals)}  min={min(vals)} max={max(vals)}")
    print(f"  S1={S1}  S2={S2}")
    print(f"  correct sums: {len(good1) + len(good2)} / {2 * len(lines)}"
          f"   bad: {bad if bad else 'none'}")
    return len(good1) + len(good2)


PFEFFERMANN = [[6, 42, 29, 3, 40, 30], [8, 44, 47, 21, 20, 10],
               [33, 31, 41, 37, 1, 7], [19, 17, 13, 9, 43, 49],
               [36, 2, 5, 35, 34, 38], [48, 14, 15, 45, 12, 16]]

BOYER = [[41, 35, 6, 2, 37, 47], [5, 42, 33, 39, 46, 3],
         [38, 7, 45, 43, 1, 34], [22, 55, 13, 11, 49, 18],
         [53, 10, 17, 23, 14, 51], [9, 19, 54, 50, 21, 15]]

WROBLEWSKI = [[17, 36, 55, 124, 62, 114], [58, 40, 129, 50, 111, 20],
              [108, 135, 34, 44, 38, 49], [87, 98, 92, 102, 1, 28],
              [116, 25, 86, 7, 96, 78], [22, 74, 12, 81, 100, 119]]

MORGENSTERN = [[72, 18, 17, 16, 49, 47], [13, 52, 36, 5, 50, 63],
               [38, 35, 7, 66, 15, 58], [20, 53, 34, 39, 69, 4],
               [55, 1, 57, 56, 26, 24], [21, 60, 68, 37, 10, 23]]

for g, n in [(PFEFFERMANN, "Pfeffermann 1894 (max 49)"),
             (BOYER, "Boyer 2005 (max 55)"),
             (WROBLEWSKI, "Wroblewski 2006 (max 135)"),
             (MORGENSTERN, "Morgenstern 2006 (max 72) - claimed optimal")]:
    audit(g, n)
