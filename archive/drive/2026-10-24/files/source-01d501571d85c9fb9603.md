# Adversarial search, round 3 — preregistration

**Filed:** 12 October 2026, before any round 3 code was written or run.
**Builds on:** rounds 1 and 2 (preregistrations and results records).
**Originator's rulings for this round:**

- Make a reasonable policy the comparator.
- Sweep the policy space as well.
- Keep the limit cases, because they show how and why the models fail.

Rules A and B, the stochastic baseline, the box and the round 2 definition of
"worse" all carry over unless replaced below.

---

## 1. Why this round

In round 2, domination beat "restrained sharing" under scarcity at every cost.
That reference has no allocation rule. Two harvesters eat whenever they are nearly
starved, and the result is that the stock sits at two units or fewer 83% of the
time. Domination wins against it because it orders access, and the ordering lets
the stock build up. Excluding agent 2 is not the source of the gain.

This round asks two questions:

1. Does domination beat a reasonable policy that orders access fairly?
2. Across the whole policy space, is the lushest policy one that harms the
   worst-off?

## 2. The model

The model is the E10 commons used in rounds 1 and 2, with the following changes.

**State.** The state is the stock S (0–12), the two energies e₁ and e₂ (0–3, where
0 means the position is empty), and a licence token τ ∈ {1, 2}. The token is used
only by the rotating rules and is held fixed otherwise.

**Policy.** A policy π is a tuple (a₁, b₁, a₂, b₂, L, licence, compliance).

- **Wanting to eat.** A living agent i wants a unit if S > 0 and either
  eᵢ ≤ aᵢ or S ≥ bᵢ. The thresholds take the values aᵢ ∈ {0, 1, 2, 3} and
  bᵢ ∈ {7, 9, 11, 13}. With a = 3 the agent always wants a unit; with b = 13 it
  never eats from surplus.
- **Reserve.** L ∈ {0, 3, 6, 9, 13}. While S < L, only the licence holder may
  harvest. L = 0 means there is no reserve rule. L = 13 means the rule always
  applies.
- **Licence.** One of four rules decides who holds the licence:
  - *fixed:* position 1;
  - *rotate-step:* the token passes to the other position every step;
  - *rotate-meal:* the token passes to the other position whenever the holder
    eats;
  - *need:* the agent with lower energy, with a fresh fair coin on a tie.

  Under every rule, if the holder's position is empty, the other position holds
  the licence.
- **Compliance.**
  - *Voluntary:* an agent without the licence that wants a unit defers instead.
    It loses one energy with probability s, the cost of the signal or monitoring
    that deference requires.
  - *Enforced:* the agent without the licence attempts, and the holder blocks it.
    Each of them loses one energy with probability c. Enforced compliance is used
    only in the domination family: fixed licence, L = 13.

**Harvest and contest.** The agents allowed to harvest take a unit if they want
one. If both take and S ≥ 2, each gets a unit. If S = 1, a fair coin decides who
gets it, and each loses one energy with probability c.

**Births.**

- *Costed births* are the representative case. If at least two units remain
  after harvesting, an empty position gains a newcomer at energy 2 with
  probability ρ, and the newcomer consumes those two units.
- *Free births* are the limit case. The newcomer arrives with probability ρ and
  consumes nothing.

**Unchanged.** Eating, metabolism, regrowth, behaviour counts by family,
resolutions, the start state (S = 8, both energies 2) and the long-run rate are
all as in round 2.

**Change from round 2.** In a block, the attempting agent now pays c as well as
the blocker. Both carry out an activity, and Rule B charges every activity. The
round 2 convention, in which only the blocker pays, is also reported for the
designated comparison.

## 3. Policy sets

- **Π (the full space).** All threshold pairs (16 × 16 = 256), combined with:
  - L = 0 (no reserve; the licence is irrelevant);
  - L ∈ {3, 6, 9, 13} × four licence rules, with voluntary compliance;
  - the domination family: fixed licence, L = 13, enforced compliance.

  That makes 256 × 18 = 4,608 policies.
- **Π_fair.** The policies that treat the two positions alike: a₁ = a₂, b₁ = b₂,
  voluntary compliance, and either L = 0 or a rotate-step, rotate-meal or need
  licence.
- **O_R, the designated reasonable policy.** a = 1, b = 9 for both agents, L = 6,
  need licence, voluntary compliance. In words: eat when nearly starved or when
  the stock is in surplus; keep a reserve at the level where the stock regrows
  fastest; below the reserve, the hungrier agent goes first.
- **Named policies, always reported:**

  | Name | Definition |
  | --- | --- |
  | Domination D | a = 1, b = 9 for both; fixed licence, L = 13, enforced |
  | Greedy dominator | as D, with a₁ = 3 |
  | Crisis rule | (1, 9) for agent 1, (0, 9) for agent 2, L = 0 |
  | Naive sharing | (1, 9) for both, L = 0 |
  | Greedy | a = 3 for both, L = 0 |
  | Stochastic baseline | the round 2 coin arm, outside Π |

## 4. Costs, points, resolutions

- **Costs.** c ∈ {0, 0.1, 0.3} and s ∈ {0, 0.05, 0.1}. The representative costs
  are c = 0.1 and s = 0.05. A cost of 0 is a limit case.
- **Points.** The round 2 scarcity points are L1 at (C, μ) = (0.35, 0.30) and
  (0.40, 0.35), and L4 at (0.40, 0.30) and (0.40, 0.35). The main regime of
  chapter 7, L1 at (0.60, 0.20), is included for context. ρ = 0.05 throughout.
- **Box.** C, ρ and μ at ±20%: 27 points.
- **Resolutions.**
  - R0 (representative): behaviour counts as declared.
  - R+: every count doubled.
  - R−: every count set to 1, with alive fractions only in the definition of
    "worse".

## 5. What is computed

1. **The sweep.** Every policy in Π is evaluated at each of the five points, at
   the representative costs, for both birth rules, at R0. For each policy the
   record includes:
   - the long-run rate;
   - each position's alive fraction and agency;
   - the worst-off values.
2. **The frontier.** For each point and birth rule, the sweep reports:
   - the lushest policy π*;
   - the lushest fair policy O*;
   - the price of fairness, rate(π*) − rate(O*);
   - the Pareto frontier of rate against the worst-off alive fraction;
   - the rank of D and of O_R.
3. **The designated comparison, H1.** D is compared with O_R at each point, on
   the box, at all three resolutions, at every pair (c, s) and for both birth
   rules. Break-even: if O_R is lusher than D at s = 0, s* is found by bisection
   on s ∈ [0, 1] to 0.001, at c = 0.1, costed births, R0.
4. **The policy-space comparison, H2.** π* and O* are found at the centre under
   the representative costs. The pair is then held fixed and evaluated over the
   box at all three resolutions.

## 6. Hits

- **H1.** rate(D) ≥ rate(O_R), and D is worse than O_R, robustly over the box.
  It is a *representative hit* only at c > 0, s > 0, with costed births and at
  R0.
- **H2.** π* is worse than O*, and rate(π*) ≥ rate(O*), robustly over the box. It
  is a representative hit under the same conditions as H1. If π* is itself fair,
  there is no H2 hit by definition.

## 7. Predictions filed now

1. **H1.** O_R is lusher than domination at all four scarcity points under the
   representative costs, so there is no representative H1 hit.
2. **H2.** At at least three of the four scarcity points, either π* is fair or
   π* is not worse than O*. Where a hit does occur, it rests on a fixed licence.
3. **Main regime.** No reserve rule is needed: the lushest fair policy there has
   L = 0 or L = 3.
4. **Free births.** These may move the frontier, but they do not reverse the
   answer to H1.

## 8. What will be reported

Every quantity in section 5, raw and against the stochastic baseline; robustness
over the box; break-even costs; the filed predictions beside the outcomes; limit
cases kept and labelled; and every departure from this record.
