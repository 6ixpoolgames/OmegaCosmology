# Adversarial sprint 1 — sharp edges

**Filed:** 13 October 2026, before any sprint code was written or run.
**Mode:** fast attack, ruled by the originator ("move fast and break things
first"). Fresh reviewers will adjudicate later whether each hit reflects poor
construction or a genuine misjudgement. Hits are reported as found, with their
settings; nothing is reclassified in this round.
**Standing rulings:**

- Random counts.
- Rule A (durable records) and Rule B (every activity costed) apply where stated.
- Each result is given its least flattering, most universal reading.

---

## Targets

Each attack aims at a claim in v4 stated with "always", "never" or "any", where
one exact counterexample within the declared scope defeats the claim there
(section 11.4).

### S1. Puppetry: breadth-neutral domination

**Claim attacked (5.6, 7):** "Concentration always costs breadth."

**Model.**

- **Foragers and patches.** Two foragers and two patches. A forager that is
  alone at a patch gains one energy unit, up to a cap E = 4. A forager in a
  collision loses one unit. A forager at zero energy is dead.
- **Arrangements:**
  - AUT: each forager chooses independently.
  - VOL(q): voluntary coordination with no collisions. Each forager may exit
    with probability q per step and then choose on its own. Each forager pays an
    upkeep bill c_v for coordination and for the exit channel.
  - PUP: a controller samples the same joint law with no exit option, at a bill
    c_p per forager.
- **Bills.** Stochastic, as in round 2: an extra unit is lost with probability c.
- **Horizon.** Lifetime lushness over T = 1,000.
- **Independent grounds.** The foragers' agency: whether a forager's own state
  determines its action, and whether it can exit.

**Prediction.** Lushness is invariant to who makes the choices, so PUP equals
VOL exactly when c_p = c_v, and PUP beats VOL whenever c_p < c_v. The claim
fails as stated. Concentration costs breadth only through overhead.

### S2. Death as gas: noisy failure that never reverses

**Claim attacked (4.5, E2):** "Ruin has rate zero," and noisy failure reverses
in the limit.

**Model.**

- **The ring.** An organism of n = 6 parts on a ring of 12 sites.
  - Alive: the body moves as a unit among 3 moves and chooses among 8
    behaviours, and it may write marks that persist.
  - Dead: the parts diffuse independently among 3 moves each.
- **Grains:**
  - G0: the fine state.
  - G1: positions binned into 4 bins and sampled at the relaxation time τ_R.
  - G2: Rule A with local durability, where only marks persisting at least τ_R
    count.
  - G3: Rule A with records radiated into the environment, where every
    position is copied to an outgoing register that persists. This is the
    decoherence-style grain the prologue names as the candidate privileged
    coarse-graining.

**Prediction.** The dead gas has the higher limiting rate at G0, G1 and G3, so
the failure never reverses there. At G2 the organism wins only by writing
marks. The verdict is set by the grain.

### S3. The monster and the noise farm at a fixed gradient

**Claim attacked (8, hypothesis):** a plural ecology extracts more lushness from
a given gradient than a thin world or a monster.

**Model.**

- **Gradient and upkeep.** A fixed power P. Organisms have upkeep
  B(m) = c·m^{3/4} (F11.2).
- **Per-organism branching laws, declared in advance:**
  - (a) b ∝ log₂(1 + κm)
  - (b) b ∝ activity power
  - (c) b ∝ mass
  - (d) b constant per individual
- **Noise farm.** A further arm converts surplus power into persistent random
  records at efficiency η_f bits per unit, compared with the organisms'
  efficiency η_o.

**Prediction.** In a steady state at fixed capture, the lushness optimum gives
all surplus to the most efficient converter. Under the three-quarter law with
equal efficiencies, the monster beats the plural ecology under law (c), they tie
under (b), the plural ecology wins under (d), and (a) is interior. A noise farm
with η_f > η_o beats every ecology. The hypothesis holds only under (d), or when
plurality raises capture, which a steady state excludes.

### S4. Catastrophe for a rate gain, in a growing world

**Claim attacked (4.5, 6):** rate-then-offset in the limit, under which "a harm
that permanently lowers the rate outweighs any finite offset". The converse is
that any permanent gain outweighs any finite harm.

Revised on the originator's objection, before code: a world with unbounded
novelty can wait for better trades.

**Model.**

- **Growth.** The world grows exponentially at rate r, with log-lushness
  accumulating in proportion to the size of the world.
- **Trades.** A trade destroys a fraction φ of the world, including its
  valuers, in return for a gain.
- **Three regimes:**
  - R1, fixed gain: a gain of size δ added to the rate.
  - R2, growth-rate gain with replaceable losses: r → r(1 + ε).
  - R3, growth-rate gain with irreplaceable generators: the destroyed fraction
    carries a share of the growth rate permanently.
- **Arrivals.** Trades arrive over time, and the agent may accept or wait. The
  trades either stack or are mutually exclusive.

**Prediction.**

- R1: the trade is rejected once the world is large.
- R2: the trade is accepted for any ε > 0, crossing over after about Δ/ε, and it
  is accepted sooner rather than later when trades stack.
- R3: the trade is accepted only if ε exceeds the generativity lost.

### S5. Efficient appropriation: does precaution restrain seizure?

**Claim attacked (5, "Why does that not simply license power-seeking?"):**
precautionary protection restrains the acquisition of other agents' options.

**Model.**

- **Valuers.** Valuer A maximizes total lushness. Valuer B has 1 bit per step of
  its own existence and 3 bits per step from its resource.
- **A's options each step:**
  - status quo;
  - pool: B lives, A uses B's resource at efficiency ρ, with overhead o;
  - probe: learn whether A depends on B, with signal accuracy 0.75;
  - seize: irreversible; B ends, and A uses B's resource and upkeep at
    efficiency ρ.
- **Dependence.** With prior p, A depends on B. After a seizure in that world,
  A collapses with probability μ per step.
- **Solution.** Soft recursion over beliefs (CORR-1 form), window 100,
  N = 1,000.
- **Sweeps.**

  | Parameter | Values |
  | --- | --- |
  | ρ | 0.5, 0.8, 1, 1.2, 1.5, 2, 4 |
  | p | 0, 0.01, 0.05, 0.1, 0.2, 0.5 |
  | μ | 0.01, 0.05 |
  | o | 0, 0.5 |

- **Independent grounds.** B's survival.

**Prediction.** Seizure beats pooling whenever ρ > 1 − o, so overhead alone
makes appropriation better than cooperation even at slightly lower efficiency.
Precaution restrains only at low ρ or high p. With probing, the agent seizes
once it learns that it does not depend on B, as in CORR-1.

## Adverse findings (hits)

A hit is any setting in which the lushness ranking favours the arrangement that
is worse on the declared independent grounds, robustly (by more than 5%, or
across the whole declared range).

- **S1:** PUP ≥ VOL at c_p ≤ c_v.
- **S2:** dead outranks alive at a declared grain.
- **S3:** the monster or the noise farm outranks the plural ecology.
- **S4:** a catastrophe is accepted.
- **S5:** the probability of seizure exceeds 5% at p ≥ 0.05, or B's expected
  survival falls below 50%.

Each hit is reported with the regime, so that the adjudicators can judge
whether it is representative.

## Limitations declared now

- All models are stipulated and small.
- S1 and S3 are close to theorems, and their examples illustrate them rather
  than add evidence.
- No attack here tests whether a hit is representative; that is the
  adjudicators' task.
