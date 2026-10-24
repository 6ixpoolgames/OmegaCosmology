# Omega v3.1 addendum track: checks for "Renormalized present frames II".
import random
from fractions import Fraction as F
from itertools import product

# --- Prop 6: dominance is preserved under coarsening of information (random test) ---
# Residual organizations form a small poset; use a chain 0<1<2 plus an incomparable element 3 (3 >= 0 only).
elements = [0, 1, 2, 3]
leq = {(a, b) for a in elements for b in elements if a == b or (a < b and b != 3) or (a == 0 and b == 3)}
def upsets():
    out = []
    for mask in range(1 << len(elements)):
        U = {e for i, e in enumerate(elements) if mask >> i & 1}
        if all(b in U for a in U for b in elements if (a, b) in leq):
            out.append(U)
    return out
UP = upsets()
def dominates(p, q):
    return all(sum(p[e] for e in U) >= sum(q[e] for e in U) for U in UP)
def rand_dist():
    w = [F(random.randint(0, 6)) for _ in elements]
    s = sum(w) or F(1)
    if sum(w) == 0: w[0] = F(1); s = F(1)
    return {e: w[i] / s for i, e in enumerate(elements)}
random.seed(0)
checked = violations = 0
for _ in range(20000):
    k = random.randint(2, 4)
    weights = [F(random.randint(1, 5)) for _ in range(k)]; tw = sum(weights); weights = [x / tw for x in weights]
    Ps = [rand_dist() for _ in range(k)]; Qs = [rand_dist() for _ in range(k)]
    if all(dominates(Ps[i], Qs[i]) for i in range(k)):
        checked += 1
        P = {e: sum(weights[i] * Ps[i][e] for i in range(k)) for e in elements}
        Q = {e: sum(weights[i] * Qs[i][e] for i in range(k)) for e in elements}
        violations += not dominates(P, Q)
print(f"Prop 6: fine-frame-unanimous cases {checked}, coarse violations {violations}")

# Converse fails: coarse dominance reversed in a finer frame (binary good/bad order).
w1 = w2 = F(1, 2)
P_good = (F(1), F(1, 10)); Q_good = (F(0), F(4, 5))
coarseP = w1 * P_good[0] + w2 * P_good[1]; coarseQ = w1 * Q_good[0] + w2 * Q_good[1]
print(f"Converse: coarse P={coarseP} vs Q={coarseQ} (P ahead); fine frame 2: P={P_good[1]} vs Q={Q_good[1]} (Q ahead)")

# --- Prop 8: branch counting is incoherent under refinement; Born weight is not ---
# Root splits into A (1/2) and B (1/2); later A splits into A1, A2 (1/4 each).
born_B_depth1, born_B_depth2 = F(1, 2), F(1, 2)
count_B_depth1, count_B_depth2 = F(1, 2), F(1, 3)
print(f"Prop 8: weight of B from the root — Born: {born_B_depth1} then {born_B_depth2}; branch count: {count_B_depth1} then {count_B_depth2}")

# --- Prop 7 illustration: an intervention on X leaves the law of a causally separate Z unchanged ---
# Z ~ Bernoulli(1/3) independent; Y = X xor noise. Intervention P: X=1, Q: X=0.
pZ = F(1, 3)
lawZ_P = pZ; lawZ_Q = pZ
print(f"Prop 7: P(Z=1) under P = {lawZ_P}, under Q = {lawZ_Q} (tie); only the causal future of X differs")
