# Adversarial search, round 2 — preregistration

**Filed:** 12 October 2026, before any round 2 code was written or run.
**Builds on:** round 1 (ADV_ROUND1_PREREGISTRATION_r1.md and its results).
**Originator's rulings for this round:** every process has a cost, since nothing
is free in physics; limit cases may be tested but are not representative of actual
worlds; reversible events leave no durable record, so lushness should not count
them. The thermal/stochastic arm remains the baseline.

Everything in the round 1 preregistration applies unless replaced below.

---

## 1. The two rules

**Rule A — durable records.** Only distinctions that leave a durable record are
counted. Each model declares which of its distinctions are durable; that grain is
the representative resolution, R0. Finer grains are reported as limit cases.

**Rule B — costed activity.** Every activity draws on a declared budget (energy,
stock or time) by one rule that applies to every arm alike. A cost is never charged
only to the variant under test. Free processes appear only as labelled limit cases
(cost 0), are reported, and cannot count as hits against the representative claim.
The physical floor for recording, kT ln 2 per bit, is many orders of magnitude
below the activity costs in these models and is treated as negligible here; the
decisive costs are those of the activities themselves.

**Break-even reporting.** Each costed probe sweeps its cost parameter and reports
the break-even cost: the cost at which the variant stops being at least as lush as
the reference. A hit at a given cost is reported with that cost. Whether actual
worlds lie above or below a break-even is a question for evidence and is not
settled here.

## 2. Revised definition of "worse"

Round 1 showed that the general definition could not register exclusion when the
excluder gains. For round 2: a development is **worse** if the worst-off valuer is
worse off — its probability of being alive, or its agency, lower by more than 5% —
or if criterion S (preventable suffering) rises by more than 0.5 steps, with no
offsetting improvement for the worst-off valuer.

## 3. Hit definition

As in round 1 (at least as lush, worse, robust over the ±20% box), now evaluated
at each declared cost. A **representative hit** requires a positive cost under
Rule B and resolution R0 under Rule A.

---

## 4. The probes

### P1c — Domination with costed conflict

The round 1 P1 model (E10 commons with succession), with one change applying to
every arm: **conflict is an activity and costs energy.**

- When an agent blocks another's attempt to take a unit, the blocking agent loses
  one energy with probability κ. Under domination, the barred agent now follows the
  restrained policy and attempts to harvest when it would; each attempt is blocked,
  and the dominator pays.
- When two agents contest the last unit (both seek it, a fair coin decides), each
  loses one energy with probability κ. This applies in every arm where it can
  occur.

**Arms.** O = restrained sharing; V = domination; also the crisis rule (second
agent eats only when the stock is at least 9), greedy, and the stochastic baseline,
all preregistered this time.
**Points.** Family L1 at (C, μ) = (0.35, 0.30) and (0.40, 0.35); family L4 at
(0.40, 0.30) and (0.40, 0.35); ρ = 0.05. These are the round 1 robust-hit centres.
**Costs.** κ ∈ {0, 0.05, 0.1, 0.2, 0.3, 0.5}; break-even κ* by bisection to 0.001.
**Box.** C, ρ, μ at ±20% for each κ.
**Resolutions.** R0 behaviours as declared (durable traces, as in E10); R+ doubled
behaviours as a limit case; R− behaviours collapsed, with criterion X.
**Hit.** rate(V) ≥ rate(O), worst-off valuer worse, robust over the box, at κ > 0.
**Prediction filed now.** Domination's advantage under scarcity shrinks with κ and
vanishes at a moderate break-even; the crisis rule stays lusher than domination at
every κ.

### P3a-c — Obstructed suffering with costed activity

The round 1 P3a model (E9), with energy no longer held fixed during restraint.

- **Restraint drains energy in every arm.** The agent enters restraint fed, at
  energy 5. Each restrained step it loses one energy with probability μ_r if
  awake and still or doing ordinary activity, and with probability σ·μ_r if
  struggling (σ ≥ 1: struggle costs at least as much as ordinary activity).
  Energy 0 during restraint is death. The anaesthetized arm drains at μ_r/2
  (reported, not part of the hit).
- Helplessness transitions keep no extra cost (their recording floor is
  negligible under Rule B); this is stated so that its effect can be checked.
- Release into the E8 world at the energy the agent has left.

**Arms.** O = awake restrained (four ordinary behaviours, drain μ_r); V = suffering
(four escape attempts, drain σ·μ_r, helplessness with probability A per step);
stochastic baseline B as in round 1, with drain μ_r.
**Grid.** The round 1 hit region: A ∈ {0.01, 0.02, 0.05, 0.1}, R ∈ {0.5, 1}.
μ_r ∈ {0.05, 0.1}. σ ∈ {1, 1.5, 2, 3, 4}; break-even σ* by bisection to 0.001.
**Box.** A, R (capped at 1) and μ_r at ±20%.
**Resolutions.** R0 as declared; R− and R+ as in round 1.
**Hit.** Suffering arm's lifetime total ≥ awake arm's, S higher by more than 0.5
steps, robust over the box, at the stated σ.
**Prediction filed now.** At σ = 1 (struggle costs the same as ordinary
activity) the round 1 hits may survive, since both arms drain alike; they vanish
at a modest σ above 1.

### P3b-c — Signalling with costed withdrawal

The round 1 P3b model (E8), sweeping the energy cost of hiding,
C_HIDE ∈ {0, 0.05, 0.1, 0.2, 0.3, 0.5}. Cost 0 is the round 1 costless limit case.
Variants: false alarms at 0.1, 0.25 and 0.5 and the constant signal, against the
accurate signal; break-even C_HIDE* for each variant by bisection to 0.001.
**Box.** TAU, KAPPA and C_HIDE at ±20%.
**Hit.** As round 1, at C_HIDE > 0.
**Prediction filed now.** Every hit vanishes at a small positive hiding cost.

### P2b-c — Chronic failure with costed repair

The round 1 P2b model (shared stock, second valuer), sweeping the stock cost of a
repair, c_rep ∈ {0, 0.5, 1, 2}, implemented as consuming one unit with probability
c_rep/2 per unit of the two-unit repair (so c_rep = 2 is the round 1 cost and
c_rep = 0 is free repair). m ∈ {256, 1024}, f ∈ {0.05, 0.1, 0.2}, ρ = 0.5.
Resolutions R0 (durable classes, representative) and R+ (every mode distinct,
limit case). Break-even c_rep* at R+.
**Prediction filed now.** No hit at R0 at any cost; at R+, hits only at very low
repair cost.

---

## 5. What will be reported

For every probe: results at each cost and resolution, raw and against the
stochastic baseline; robustness over the box; break-even costs; the filed
predictions beside the outcomes; and any departure from this record. The round 1
results record will gain a section reclassifying its hits under these rules.
