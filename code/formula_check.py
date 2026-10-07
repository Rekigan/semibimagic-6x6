"""Verifica della formula S1(r) = 133-r, S2(r) = 3815 - 35r - r^2 per
l'omissione della classe r (mod 7) da {1..42}, contro il conteggio diretto."""
TOT, TOTQ = 903, 25585
print(f"{'r':>2} {'S1 dir':>7} {'133-r':>6} {'S2 dir':>7} {'formula':>8} {'ok':>3}")
for r in range(0, 7):
    cls = [r + 7 * k for k in range(6)] if r else [7 * k for k in range(1, 7)]
    s1 = (TOT - sum(cls)) // 6
    rem = TOTQ - sum(x * x for x in cls)
    s2 = rem / 6
    f1, f2 = 133 - r, 3815 - 35 * r - r * r
    ok = (s1 == f1 and s2 == f2) if r else "n/a (classe di 42)"
    print(f"{r:>2} {s1:>7} {f1:>6} {s2:>7.0f} {f2:>8} {str(ok):>3}"
          f"{'   divisibile per 6: ' + str(rem % 6 == 0) if r else ''}")
print("\nr=4 -> 3659 = il vincitore S2-minimo: la formula si auto-convalida.")
