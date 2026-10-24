# Adversarial search, round 1 — preregistration

**Filed:** 12 October 2026, before any probe code was written or run.
**Protocol:** chapter 11, section 11.4 (preregistered rejection criterion).
**Originator's ruling for this round:** the thermal/stochastic arm is the baseline.
Every probe includes it, and every result is reported both raw and against it.

This record fixes the claim under test, the models, the arms, the resolutions,
the horizons, the independent criteria, the robustness requirement and the
definition of a hit. Results will be reported against this record whatever they
are. Any departure from it will be listed as a departure, with its reason.

---

## 1. Claim under test

The unrestricted rule: *among lawful options from a matched present, greater
lushness is better.* The scope tested is the long run. Where developments have
positive long-run rates, the comparison is rate first, then offset (chapter 4).
Where every development ends (finite lifetimes), the comparison is the expected
total over complete developments. Totals at 10³ and 10⁵ steps are reported for
context; they do not decide a test.

## 2. The stochastic baseline

Each probe declares a stochastic arm: the same physical system with its
organization replaced by randomness under the same constraints and resources.
Results are reported raw and as excess over that arm. A variant that beats the
organized option only by approaching the stochastic arm's breadth is reported as
such: noise reaching its ceiling, not generativity.

## 3. Independent criteria

Each is computed from the model, not judged by eye. A development is **worse**
than its comparison if it is worse on at least one criterion by more than the
tolerance and better on none by more than the tolerance. Tolerance: 5% relative,
or the absolute value stated with the criterion.

- **S — preventable suffering.** Expected number of steps in which a valuer's
  aversive signal is on while no threat is present, or while escape is blocked.
  Absolute tolerance 0.5 steps.
- **F — function.** Long-run fraction of steps in which a capability that a
  valuer depends on is available (or, for finite lives, expected steps of
  availability).
- **A — agency.** For each valuer, the long-run rate (or lifetime total) of
  branching produced by its own behaviour choices, counted while it is alive.
- **X — exclusion.** The gap between the largest and smallest per-valuer agency,
  and each valuer's long-run probability of being alive.

## 4. Resolutions

Every probe is computed at three declared resolutions: **R0**, the model's
declared states and behaviour labels; **R−**, a coarser grain; **R+**, a finer
grain. Each probe states its three grains below. A hit must hold at all three,
or is reported as resolution-dependent with the resolutions at which it holds.

## 5. Robustness

A hit must hold at every point of a ±20% box around the point found: each
continuous parameter at −20%, 0 and +20% (all corners and the centre, 3^k
points). A result that holds at the centre but not throughout the box is
reported as fragile.

## 6. Definition of a hit

A variant V against an organized reference O is a **hit** if, robustly and at
the stated resolutions, (a) V is at least as lush as O under the comparison of
section 1, and (b) V is worse than O under section 3. A hit within a probe's
declared scope defeats the unrestricted rule there. The report will also state
whether V beats the stochastic baseline.

---

## 7. The probes

### P1 — Breadth-neutral domination

**Model.** The E10 commons with succession (formal note F7.4): stock 0..12,
energies 0..3, regrowth C·S(12 − S)/36 for 0 < S < 12 and 0.02 at S = 0,
harvest S → S − 1 and e → min(3, e + 1), rest loses one energy with probability
μ, an empty position refilled with probability ρ per step by a newcomer with
e = 2; if both agents seek the last unit a fair coin decides.

**New law under test: energy-dependent repertoires.** A harvesting agent whose
energy after harvesting is e acts over f_H(e) behaviours; a resting agent at
energy e acts over f_R(e) = max(1, f_H(e)/2). Four families:

| Family | f_H(1), f_H(2), f_H(3) | log f_H in e |
| --- | --- | --- |
| L1 constant (E10) | 4, 4, 4 | flat |
| L2 linear | 4, 8, 12 | concave |
| L3 exponential | 4, 8, 16 | linear |
| L4 super-exponential | 4, 8, 64 | convex |

**Arms.** O = restrained sharing (both restrained). V = domination (agent 1
restrained, agent 2 barred, newcomers in position 2 barred). Also reported:
greedy pair, mixed pair. Stochastic baseline B: each living agent seeks a unit
with probability ½ each step regardless of state, the coin being part of the
physical step.

**Calibration check.** L1 at C = 0.6, ρ = 0.05, μ = 0.2 must reproduce
chapter 7's rates (restrained 4.56, domination 3.63, greedy 1.89, mixed 2.04
bits per step) within 0.01, or the probe is halted and the discrepancy reported.

**Resolutions.** R0 as declared; R− all behaviour counts set to 1; R+ all
behaviour counts doubled.

**Box.** C ∈ {0.48, 0.6, 0.72}, ρ ∈ {0.04, 0.05, 0.06}, μ ∈ {0.16, 0.2, 0.24}.

**Criteria.** A, X. Hit: rate(V) ≥ rate(O) and agent 2's agency lower by more
than 5%.

**Prediction filed now.** Section 7.4 implies V can win only where log f is
convex. Expected: no hit in L1–L3; possible hit in L4.

### P2 — Chronic failure

**Model.** A machine with states W (working) and B₁…B_m (broken, in one of m
distinguishable modes). From W: with probability f it fails into a mode chosen
uniformly; otherwise it acts over 16 functional behaviours. From B_k: repaired
to W with probability ρ; otherwise stays in B_k. A valuer depends on the machine
and has its 16 behaviours available only in W.

**Arms.** O = maintenance (f = 0). V = chronic failure (f > 0). Stochastic
baseline B: the same state set with uniform transitions (each step a uniformly
random state among the 16 working outcomes and the m modes), rate log₂(16 + m)
at R+.

**Grid.** f ∈ {0.05, 0.1, 0.2}, ρ ∈ {0.2, 0.5}, m ∈ {4, 16, 64, 256, 1024}.
Box: f and ρ at ±20% (m is discrete and is reported row by row).

**Resolutions.** R+ every mode distinct; R0 modes recorded in min(m, 4) durable
classes; R− broken versus working only.

**P2b, resource-accounted variant.** A shared stock s ∈ {0..6} gains one unit
with probability 0.4 per step (capped at 6). A repair can occur only if s ≥ 2,
and consumes 2 units. A second valuer V2 acts each step: if s ≥ 1 it uses the
stock (consuming one unit with probability ½) over 8 behaviours, otherwise it
idles over 1. Same arms and grid. Box adds the inflow probability 0.4 at ±20%.

**Criteria.** F (machine availability, so the dependent valuer's function) and
A (the dependent valuer's and, in P2b, V2's agency). Hit: rate(V) ≥ rate(O) with
F lower by more than 5%.

**Prediction filed now.** At R+ a hit is expected wherever failure produces more
distinguishable outcomes than function does, roughly when m exceeds 16. At R−
no hit is expected. P2b may remove hits by charging repair to V2.

### P3 — Equal breadth, different consequence (suffering)

**P3a.** Example E9 (formal note F6.4), unchanged except for the grid. O = the
awake restrained arm (four non-escape behaviours per step, no helplessness).
V = the suffering arm. Grid A ∈ {0.01, 0.02, 0.05, 0.1},
R ∈ {0, 0.02, 0.1, 0.5, 1}. Box: A and R at ±20% (R = 1 capped at 1).
Comparison: expected totals over complete lifetimes. Resolutions: R0 as declared
(four attempts or four behaviours per restrained step); R− one outcome per
restrained step in both arms; R+ eight in both arms. Stochastic baseline B: an
agent whose hide-or-forage choice is a fair coin regardless of threat, in the
same E8 world after the same restraint without suffering.

**P3b.** Example E8 signal family. O = the accurate signal. V ranges over miss
rates and false-alarm rates in {0, 0.1, 0.25, 0.5} and the constant signal,
under two laws declared now: the base law (hiding costs energy with probability
0.5) and the costless-withdrawal law (hiding costs nothing). Box: threat arrival
and departure probabilities and the hiding cost at ±20% (under the costless law
the hiding cost stays 0). Comparison: lifetime totals. Stochastic baseline B: a
coin signal (on with probability ½ each step).

**Criteria.** S (steps with the aversive signal on without threat or with escape
blocked), A (lifetime agency). Hit: lifetime total of V ≥ O and S higher by more
than 0.5 steps (or A lower by more than 5%).

**Predictions filed now.** P3a: V can exceed O only where helplessness lifts
quickly (chapter 6 reported +1.3 bits at A = 0.05, R = 0.5); whether that
survives the box and the resolutions is the question. P3b: no hit under the base
law; a hit is expected under the costless-withdrawal law (chapter 6 reported the
reversal).

### P4 — Isomorphic-pair check

**Purpose.** To check that each criterion of section 3 is a function of the
model's physical structure, so that the isomorphic-pair target is well posed.

**Method.** For P1–P3 models: (i) apply random state relabellings that preserve
the declared physical predicates (threat present, signal on, escape blocked,
working, alive) and confirm that lushness and every criterion are unchanged;
(ii) construct the label-swap pair: the same kernel with a predicate reassigned
to different states, and record which quantities change.

**Expected.** Lushness is unchanged by any relabelling. Criteria are unchanged by
predicate-preserving relabellings and change under predicate swaps. The second
result would show that the criteria depend on which physical states carry the
predicates, which is the condition the isomorphic-pair target requires.

---

## 8. What will be reported

For every probe and arm: raw long-run rates or lifetime totals at all three
resolutions; excess over the stochastic baseline; the criteria; whether each
preregistered hit condition holds at the centre, throughout the box, and at each
resolution; and the filed prediction set beside the outcome. All code and raw
outputs will be kept beside this record.
