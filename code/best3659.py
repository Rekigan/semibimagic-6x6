"""Extract an optimal square on the S2-minimal set:
{1..42} minus the arithmetic progression {4,11,18,25,32,39}."""
from semibimagic import solve, show
from records import audit

nums = [k for k in range(1, 43) if k not in (4, 11, 18, 25, 32, 39)]
assert len(nums) == 36
g = solve(nums)
if g:
    show(g)
    audit(g, "\nOPTIMAL SQUARE, S2-minimal set (42, 129, 3659)")
