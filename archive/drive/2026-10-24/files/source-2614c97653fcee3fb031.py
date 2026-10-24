"""Checks for 'The ultimate frame: goodness, horizons and redemption' (addendum, 2026-09-28).

Exact or exhaustive checks of the elementary mathematical claims in the addendum:

  A. Proposition 9 (viability horizon): on random finite control systems, no admissible
     transition leads from outside the viability kernel into it while staying in K;
     every trajectory from outside leaves K within |K| steps; enlarging the control set
     never shrinks the kernel; a recovery control admissible from every state makes the
     kernel all of K.
  B. Merging alternatives (interference): two record-free paths to one outcome do not
     have additive weights; orthogonal records restore additivity.
  C. Composite valuers (Moebius / Harsanyi dividends): dividends sum to the grand
     coalition's value (no double counting); the pair dividend equals the addendum's
     interaction contrast E11 - E10 - E01 + E00; Shapley value = dividends split equally.
  D. Proposition 11 (hazard criterion): P(never turn) = prod(1 - h_n); harmonic hazards
     drive it to 0, inverse-square hazards leave exactly 1/2.

Run: python3 frames_checks_3.py
"""
from fractions import Fraction as F
from itertools import combinations
import math
import random

random.seed(20260928)


# ---------------------------------------------------------------- A. viability horizon
def viability_kernel(K, controls):
    """Greatest subset V of K such that every x in V has some control u with controls[x][u] in V."""
    V = set(K)
    changed = True
    while changed:
        changed = False
        for x in list(V):
            if not any(y in V for y in controls[x]):
                V.discard(x)
                changed = True
    return V


def random_system(n_states, n_controls, k_frac):
    states = list(range(n_states))
    K = set(random.sample(states, max(1, int(k_frac * n_states))))
    controls = {x: [random.randrange(n_states) for _ in range(n_controls)] for x in states}
    return states, K, controls


def check_A(trials=3000):
    one_way_violations = 0
    exit_violations = 0
    monotone_violations = 0
    recovery_violations = 0
    nontrivial = 0
    for _ in range(trials):
        n = random.randint(4, 14)
        states, K, controls = random_system(n, random.randint(1, 3), random.uniform(0.4, 0.9))
        V = viability_kernel(K, controls)
        outside = K - V
        if V and outside:
            nontrivial += 1
        # One-way: from x in K\V, no successor inside V.
        for x in outside:
            if any(y in V for y in controls[x]):
                one_way_violations += 1
        # Finite exit: every trajectory from K\V leaves K within |K| steps.
        for x in outside:
            frontier = {x}
            for _step in range(len(K) + 1):
                frontier = {y for z in frontier for y in controls[z] if y in K}
                if not frontier:
                    break
            if frontier:
                exit_violations += 1
        # Monotonicity in the control set.
        bigger = {x: controls[x] + [random.randrange(n)] for x in states}
        if not V <= viability_kernel(K, bigger):
            monotone_violations += 1
        # Universal recovery control: from every state, a control to a fixed state r in K
        # that can stay put (self-loop added). Kernel becomes all of K.
        r = next(iter(K))
        rescued = {x: controls[x] + [r] for x in states}
        if viability_kernel(K, rescued) != K:
            recovery_violations += 1
    print("A. Viability horizon")
    print(f"   systems: {trials}, with both kernel and outside nonempty: {nontrivial}")
    print(f"   one-way violations (outside -> kernel inside K): {one_way_violations}")
    print(f"   finite-exit violations: {exit_violations}")
    print(f"   kernel shrank when controls were added: {monotone_violations}")
    print(f"   universal recovery control failed to make kernel = K: {recovery_violations}")
    assert one_way_violations == exit_violations == monotone_violations == recovery_violations == 0


# ---------------------------------------------------------------- B. interference
def check_B():
    a1 = a2 = 0.5  # amplitudes of two paths to the same outcome
    coherent = abs(a1 + a2) ** 2          # no which-path record: amplitudes add
    incoherent = abs(a1) ** 2 + abs(a2) ** 2  # orthogonal records: weights add
    print("B. Merging alternatives")
    print(f"   record-free merge weight |a1+a2|^2 = {coherent:.4f}; sum of weights = {incoherent:.4f}")
    print(f"   cross-term = {coherent - incoherent:.4f} (additivity fails without records)")
    # With records r1, r2 and overlap <r1|r2> = c, weight = |a1|^2 + |a2|^2 + 2 Re(a1 a2* c)
    for c in (1.0, 0.5, 0.0):
        w = a1 ** 2 + a2 ** 2 + 2 * a1 * a2 * c
        print(f"   record overlap {c:.1f}: weight {w:.4f}")
    assert math.isclose(a1 ** 2 + a2 ** 2 + 2 * a1 * a2 * 0.0, incoherent)


# ---------------------------------------------------------------- C. dividends
def subsets(s):
    s = tuple(sorted(s))
    for k in range(len(s) + 1):
        for c in combinations(s, k):
            yield frozenset(c)


def dividends(v, players):
    d = {}
    for S in subsets(players):
        d[S] = sum(((-1) ** (len(S) - len(T))) * v[T] for T in subsets(S))
    return d


def check_C(trials=2000):
    players = frozenset({"a", "b", "c"})
    worst = F(0)
    for _ in range(trials):
        v = {S: F(random.randint(0, 20)) for S in subsets(players)}
        v[frozenset()] = F(random.randint(0, 5))
        d = dividends(v, players)
        # Efficiency: sum of all dividends over nonempty-or-empty subsets of N equals v(N).
        assert sum(d[S] for S in subsets(players)) == v[players]
        # Pair dividend equals interaction contrast (with third player absent).
        ab = frozenset({"a", "b"})
        contrast = v[ab] - v[frozenset({"a"})] - v[frozenset({"b"})] + v[frozenset()]
        assert d[ab] == contrast
        # Shapley value = own dividends split equally among members.
        for i in players:
            shap_div = sum(d[S] / len(S) for S in subsets(players) if i in S)
            # Direct Shapley from marginal contributions.
            n = len(players)
            direct = F(0)
            others = players - {i}
            for S in subsets(others):
                wgt = F(math.factorial(len(S)) * math.factorial(n - len(S) - 1), math.factorial(n))
                direct += wgt * (v[S | {i}] - v[S])
            # Shapley over dividends ignores d[empty]; marginal form ignores v(empty) offset too.
            worst = max(worst, abs(shap_div - direct))
    print("C. Composite valuers")
    print(f"   {trials} random 3-member value functions: dividends sum to v(N) in every case")
    print("   pair dividend = interaction contrast E11 - E10 - E01 + E00 in every case")
    print(f"   max |Shapley via dividends - Shapley via marginals| = {worst}")
    assert worst == 0


# ---------------------------------------------------------------- D. hazard criterion
def never_turn(hazard, N):
    p = F(1)
    for n in range(1, N + 1):
        p *= 1 - hazard(n)
    return p


def check_D():
    print("D. Hazard criterion")
    for N in (10, 100, 1000):
        harm = never_turn(lambda n: F(1, n + 1), N)
        sq = never_turn(lambda n: F(1, (n + 1) ** 2), N)
        assert harm == F(1, N + 1)
        assert sq == F(N + 2, 2 * (N + 1))
        print(f"   N={N:5d}: harmonic hazard -> P(never) = {harm} ; inverse-square -> {sq} = {float(sq):.6f}")
    print("   limits: harmonic -> 0 (sum diverges); inverse-square -> 1/2 (sum converges)")
    # Constant floor: any fixed epsilon gives geometric decay to 0.
    eps = F(1, 50)
    print(f"   constant hazard 1/50, N=1000: P(never) = {float(never_turn(lambda n: eps, 1000)):.3e}")


if __name__ == "__main__":
    check_A()
    check_B()
    check_C()
    check_D()
    print("All checks passed.")
