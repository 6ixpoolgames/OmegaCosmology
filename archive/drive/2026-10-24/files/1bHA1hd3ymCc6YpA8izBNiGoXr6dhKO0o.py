from fractions import Fraction as F
from itertools import product
from math import comb
q = F(2,3)  # heavy branch relative weight
def w(path):  # path: tuple of 'h'/'l'
    r = F(1)
    for s in path: r *= q if s == 'h' else 1-q
    return r
# Example A: conservation and thinning
for n in (1,5,10):
    tot = sum(w(p) for p in product('hl', repeat=n))
    spec = w(('h',)*n)
    coarse = sum(w(p) for p in product('hl', repeat=n) if p.count('h') >= n/2)
    print(f"n={n}: total={tot}, all-heavy path={spec} ({float(spec):.4f}), >=half heavy={float(coarse):.4f}")
# Example B: frame consistency (tower property)
E = lambda p: p[:3].count('h') >= 2   # event decided by depth 3
mu_root = sum(w(p) for p in product('hl', repeat=3) if E(p))
avg_children = sum(w((c,)) * sum(w(p)/w((c,)) for p in product('hl', repeat=3) if p[0]==c and E(p)) for c in 'hl')
print("B: mu_root(E) =", mu_root, "; weighted avg of child frames =", avg_children)
mu_h = sum(w(p) for p in product('hl', repeat=3) if p[0]=='h' and E(p))/w(('h',))
mu_l = sum(w(p) for p in product('hl', repeat=3) if p[0]=='l' and E(p))/w(('l',))
print("   child frames: mu_h(E) =", mu_h, " mu_l(E) =", mu_l)
# Example C: population scoring and excision
# Q: valuer j exists in branches of weight 1/2, requirement met in 3/4 of those
# P: creates additional weight: j exists with weight 3/4, requirement met 2/3
# X: excises j everywhere
cases = {"Q": (F(1,2), F(3,4)), "P": (F(3,4), F(2,3)), "X (excision)": (F(0), None)}
for k, (ex, sat) in cases.items():
    total = ex * sat if ex else F(0)
    cond = sat if ex else "undefined"
    print(f"C: {k}: exists-weight={ex}, total score={total}, conditional score={cond}")
# Example D: horizon sums diverge; horizon-indexed values don't
v = F(1,2)  # expected per-time value, constant
print("D: horizon sums:", [str(v*H) for H in (10,100,1000)], "per-time:", str(v))
# Example C extended: viability V = mu(exists), flourishing total F = mu(exists & flourish), conditional F|exists
ex = {"Q": (F(1,2), F(3,8)), "P": (F(3,4), F(1,2)), "Y (eliminate j where it would not flourish)": (F(3,8), F(3,8)), "X (eliminate j everywhere)": (F(0), F(0))}
for k,(V,Ft) in ex.items():
    print(f"C2: {k}: V={V}, F_total={Ft}, F_cond={'undefined' if V==0 else Ft/V}")
