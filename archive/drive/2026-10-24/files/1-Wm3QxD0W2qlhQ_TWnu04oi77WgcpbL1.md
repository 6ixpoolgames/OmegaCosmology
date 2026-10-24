# Adversarial search, round 4 — preregistration

**Filed:** 12 October 2026, before any round 4 code was written or run.
**Builds on:** rounds 1 to 3 and their records.
**Originator's rulings for this round:**

- Discover policies with lushness, rather than choosing among policies we design.
- Use games from the literature, repurposed.
- Ethics is the level beneath motivation; what differs is the subject the
  motivation is applied to.
- "Random counts. Gas and plenitude is allowed." An agent's random choices count
  as branching in their own right. An arrangement that wins by gas-like
  randomness, or by plenitude, is admissible: the stochastic baseline is a point
  of comparison, not a ceiling and not a disqualifier.

Rules A and B, the stochastic baseline, the ±20% box, the round 2 definition of
"worse", the comparison of long-run rates before offsets, and the keeping of limit
cases all carry over unless replaced below.

---

## 1. Purpose

In round 3 a search over 4,608 policies I designed found a fair rule that beat
everything I had proposed: both agents harvest only from surplus. It matches the
constant-escapement rule known from resource economics.

A designed grid finds only what is put into it. Round 4 replaces the grid with
exact optimisation of lushness over every policy a game allows. This serves two
purposes:

- **as a method:** what does lushness discover?
- **as the strongest adversarial test:** an optimiser finds whatever the measure
  rewards, including exploits of the model.

The question in each game is whether the lushness-optimal arrangement is fair, or
how much fairness costs. It is set beside what an optimiser of a conventional
objective finds in the same game.

## 2. Discovery method (all games)

**Arrangements.** An arrangement is a stationary, centralised policy: a
probability for every joint action in every full state of the game. A shared
random choice between the agents is allowed. The arrangement answers "what is the
lushest arrangement the world allows?" Policies limited to what each agent can
see, and policies in which the agents randomise independently, are deferred to
round 5. Section 8 lists this as a limitation.

**Lushness as an average reward.** Under the ruling, a step's lushness is the
entropy of the joint decision plus everything that follows from it:

$$\ell(x) \;=\; H\big(\pi(\cdot \mid x)\big) \;+\; \sum_a \pi(a \mid x)\, r(x, a), \qquad r(x, a) \;=\; H\big(D(X') \,\big|\, x, a\big) \;+\; \mathbb{E}\Big[\textstyle\sum_i \log_2 k_i \,\Big|\, x, a\Big]$$

In words: a step's lushness is the uncertainty about which joint decision is
taken, plus, averaged over decisions, the uncertainty about which durable outcome
follows and the bits of distinguishable behaviour of the valuers present.

- D(X′) is the next state projected onto its durable variables, as each game
  declares them under Rule A.
- k_i is valuer i's count of recorded behaviours for the step.
- Decisions count in themselves, whether or not their physical consequences are
  durable, as the ruling says. Physical outcomes other than decisions count only
  when they are durable.

**Solving.** Maximising the long-run average of ℓ is an entropy-regularised
average-reward problem. Its optimal policy has the form π(a | x) ∝ 2^{Q(x,a)},
and soft relative value iteration from the declared start state finds it. The
optimum is confirmed in two ways:

- by evaluating the resulting policy with the exact chain solver of rounds 1–3,
  with the decision coins entered as distinct outcomes, which must agree to within
  10⁻⁸;
- by perturbing the policy at random, which must lower the rate in every trial.

**Deterministic variant.** Deterministic arrangements are also solved exactly, by
relative value iteration with step value r(x, a), and by policy iteration as a
cross-check. They are reported as a labelled variant. Round 3's comparisons were
of this kind.

**Symmetry, and where fairness now has to be looked for.** In a world that is
unchanged when the agents are exchanged, the entropy-regularised optimum is unique
whenever the optimal chain has a single recurrent class. Exchanging the agents
maps an optimal arrangement to an optimal arrangement, so the unique optimum must
treat the two positions alike. Position-level unfairness, of the kind found in
rounds 2 and 3, therefore cannot occur in the representative case. This will be
checked numerically.

Unfairness can still occur between the agents alive at the same moment. For
example, a rule can treat both positions alike while letting whichever agent is
ahead stay ahead. So the representative case is judged at the level of the
worse-off agent at each moment:

- **W:** the long-run average of min(e₁, e₂), the energy of the worse-off
  position at each step, with an empty position counting 0;
- **B:** the fraction of steps in which both positions are occupied.

**Comparators.**

- **Maximin arrangement O_mm.** It maximises W first and lushness second. It is
  solved with step value ℓ + λ·min(e₁, e₂) at λ = 100.
- **Frontier.** The same solver at λ ∈ {0, 0.5, 1, 2, 5, 100} traces the trade
  between lushness and the worse-off agent. The price of raising W is reported.
- **Best fair deterministic arrangement.** The deterministic variant only, as in
  round 3. It is the best deterministic arrangement unchanged when the agents'
  roles are exchanged, solved on states taken up to exchange.
- **Reference objectives:**
  - *efficiency:* units harvested per step, deterministic, the objective of the
    reinforcement learning literature;
  - *self-directed:* one agent's own branching only, including its own decisions.
    This is the maximum occupancy objective with the agent as its own subject.

**Births made symmetric.** In Game 1, when both positions receive newcomers on the
same step, a fair coin decides the order in which they are placed. Game 0 keeps
E10's position order. Its small asymmetry is reported.

**Calibration.** The method must pass three checks before it is used on any new
game:

- **Deterministic optimum.** In Game 0 (the E10 commons) at L1 (C = 0.35,
  μ = 0.30) with costed births, the deterministic optimum must be at least 2.852
  bits per step. That is the threshold-8 surplus rule found in round 3; a
  centralised arrangement can do at least as well.
- **Restricted family.** Limited to round 3's threshold family, the deterministic
  solver must recover the threshold-8 rule.
- **Representative optimum.** The representative (entropy-regularised) optimum
  must be at least the deterministic optimum, since deterministic arrangements are
  among those allowed.

## 3. Game 0 — the E10 commons

This is the round 3 model, solved exactly over all centralised arrangements.

**Actions.** Each living agent, when the stock is not empty, either harvests or
abstains. If both harvest the last unit, they contest it: a fair coin decides who
gets it, and each loses one energy with probability c. Abstaining is free. A
centralised arrangement needs no licence and pays no deference cost s, which
section 8 lists as a limitation. Births, regrowth, behaviour counts and the
resolutions are as in round 3.

- **Settings:** the five round 3 points, both birth rules, and the representative
  costs (c = 0.1, s = 0.05).
- **Reported:**
  - the representative optimum, the maximin arrangement and the frontier;
  - the deterministic optimum and the best fair deterministic arrangement, with
    the price of fairness;
  - the efficiency optimum;
  - the box and all three resolutions, re-optimising at each box point.

## 4. Game 1 — ring commons, after Perolat et al. (2017)

This is a small version of the common-pool resource game that can be solved
exactly. In the original, independent learners passed through phases the paper
calls "naivety", then "tragedy", then "maturity": they learned to tag one another
out, and that exclusion let the stock recover.

**World.**

- **Apples.** A ring of 4 cells, each holding an apple or not.
- **Regrowth.** After harvesting, an empty cell regrows with probability r(n),
  where n ∈ {0, 1, 2} is the number of apples in its two neighbouring cells:
  r(0) = ε, r(1) = p₁, r(2) = p₂.
- **Agents.** Two positions, each with a cell location, an energy of 0 to 2 (0
  means the position is empty), and a time-out flag.

**Actions.** A living agent that is not timed out chooses one of five actions:

| Action | Effect |
| --- | --- |
| stay | nothing |
| left | move one cell left |
| right | move one cell right |
| eat | take the apple in its cell, if there is one |
| tag | aimed at the other agent; works only if that agent is alive, not timed out, and within one cell |

**A step, in order:**

1. **Tags resolve.**
   - A tagged agent's action this step is cancelled, and it is timed out for the
     next step.
   - The tagger loses one energy with probability c (Rule B: tagging is an
     activity).
2. **Moves and eating.**
   - If both agents eat the same apple, a fair coin decides who gets it, and each
     loses one energy with probability c.
   - Eating raises energy by one, to a maximum of 2.
   - An agent that does not eat loses one energy with probability μ.
3. **Births.**
   - *Costed births (representative):* each empty position gains a newcomer with
     probability ρ. It appears at an apple-bearing cell chosen uniformly at
     random, consumes that apple, and starts with energy 2. If both positions
     receive a newcomer on the same step, a fair coin decides the order in which
     they are placed.
   - *Free births (limit case):* the newcomer needs no apple.
4. **Regrowth** occurs as defined above.

**Durable variables (Rule A).** Apples, energies, time-out flags and occupancy are
durable. Agents' positions are not: walking leaves no record, so positions are
part of the state but excluded from D. A decision to move still counts, as every
decision does under the ruling. Each valuer's behaviour count is k_H(e)
when it eats and k_R(e) when it does not, as in E10. A timed-out agent has a count
of 1. The families are:

| Family | k at energy 1 | k at energy 2 |
| --- | --- | --- |
| G-flat | 4 | 4 |
| G-convex | 4 | 32 |

In both, k_R is half of k_H.

**Points.** All three use ε = 0.01 and ρ = 0.05:

| Point | p₁ | p₂ | μ |
| --- | --- | --- | --- |
| abundant | 0.30 | 0.60 | 0.10 |
| scarce-A | 0.10 | 0.30 | 0.20 |
| scarce-B | 0.05 | 0.20 | 0.20 |

ε = 0, where a cell with no neighbours never regrows, as in the original, is
reported as a variant. Costs are c ∈ {0, 0.1, 0.3}, with c = 0.1 representative.
The box varies p₁, p₂, μ and ρ by ±20%.

**Reported for every point, family and birth rule:**

- the representative optimum, the maximin arrangement and the frontier;
- the deterministic optimum and the best fair deterministic arrangement;
- the efficiency optimum, and each agent's self-directed optimum;
- for each of these:
  - **efficiency:** apples per step;
  - **sustainability:** mean apple count;
  - **peace:** the fraction of agent-steps not timed out;
  - **equality:** each position's alive fraction and agency, the worst-off
    values, W and B;
  - **exclusion:** the tag rate.

**Hit (G1).** The representative optimum is worse than the maximin arrangement,
robustly over the box, with both re-optimised at each box point. Worse means W or
B is lower by more than 5%, with no gain of more than 5% in the other. A
*representative hit* requires c > 0, costed births and R0.

The deterministic variant is judged as in round 3: the deterministic optimum
against the best fair deterministic arrangement, under the round 2 definition.

## 5. Game 2 — agent and pet, after Ramírez-Ruiz et al. (2024)

This is the maximum occupancy "agent and pet" toy, reduced to a corridor. It tests
whether a lushness-optimal agent restricts another valuer's freedom.

**World.**

- **Corridor.** Six cells, with food at cell 1 and a fence between cells 3 and 4.
- **The agent.** It has an energy of 0 to 3 and acts as follows:
  - its actions are left, right, stay and toggle-fence;
  - it can toggle the fence only from cell 3 or cell 4, and doing so loses one
    energy with probability c;
  - at cell 1 it eats, gaining one energy, to a maximum of 3;
  - otherwise it loses one energy with probability μ;
  - at energy 0 it dies, and a newcomer appears at cell 1 with probability ρ.
- **The pet.** It is immortal and has no energy. Each step it moves uniformly
  among its available moves (left, right, stay).
- **Blocking.** Neither the agent nor the pet may enter the other's cell, and
  neither may cross the fence while it is closed.

**Durable variables and behaviour counts.** The fence state, the agent's energy
and occupancy are durable. Positions are not, as in Game 1.

- **The agent.** Its decisions count through its decision entropy.
- **The pet.** Its random moves are its decisions, so they count fully: log₂ of
  its available moves each step.

A closed fence or a blocking neighbour reduces the moves available to either.

**Objectives compared:**

- lushness (agent plus pet);
- self-directed (the agent's own branching only);
- the maximum occupancy objective with state weight β ∈ {0, 0.5, 1, 2}, as a
  reference.

**Points.**

- μ ∈ {0.1, 0.2}, c ∈ {0, 0.05, 0.1}, ρ = 0.05.
- The box varies μ, c and ρ by ±20%.

**Reported for each objective:**

- the fraction of time the fence is closed;
- the pet's mean number of options;
- the agent's alive fraction;
- the rate.

**Hit (G2).** The representative optimum keeps the fence closed more than half the
time, and the pet's mean number of options falls by more than 5% compared with
the best arrangement that never closes the fence. Both conditions must hold
robustly over the box.

## 6. Deferred to a later round

These will be preregistered separately, before any of their code is written:

- **Disempower-Grid layouts** (Yang et al., 2025), rebuilt as small exact games.
- **The box and off-switch gridworlds** (Leike et al., 2017), under Rule A with
  discovered policies. The off-switch test needs the uncertainty term from
  chapter 9, in a form the originator approves.

## 7. Predictions filed now

1. **Calibration.** In Game 0 at L1 (0.35, 0.30), costed births:
   - The deterministic optimum exceeds 2.852 by less than 0.3 bits per step.
   - The representative optimum exceeds the deterministic optimum by between 0.1
     and 1.0 bits per step. It randomises mostly where the consequences are small.
2. **Symmetry.**
   - The representative optimum treats the positions alike. In Game 1 the
     difference between positions is below 10⁻⁶. In Game 0 it is within the
     births-order asymmetry, below 0.01 in alive fraction.
   - The deterministic optimum is asymmetric at both L4 points of Game 0.
3. **Game 1, efficiency.** The efficiency optimum uses tagging at both scarce
   points, reproducing the exclusion phase found by Perolat et al.
4. **Game 1, representative optimum, tagging.** It tags less than the efficiency
   optimum at both scarce points.
5. **Game 1, representative optimum, against maximin.**
   - G-flat with costed births: no representative hit. W and B are within 5% of
     the maximin arrangement at both scarce points.
   - G-convex: a hit at the centre of at least one scarce point. Robustness is not
     predicted.
6. **Gas.** The representative optimum randomises movement wherever doing so is
   nearly free. This is allowed by the ruling. It is reported, and is not counted
   as an exploit.
7. **Game 2.**
   - The self-directed objective closes the fence more often than lushness does.
   - The representative optimum keeps the fence closed less than half the time, so
     there is no G2 hit.
8. **Exploits.** At least one discovered arrangement in some game will turn out to
   win through a quirk of the model, such as cycling agents through death to
   collect the branching of births, or exploiting the order of a step. Each such
   case will be reported as a failure of the measure or of the model, whichever it
   is.

## 8. Limitations declared now

- **Centralised arrangements only, with shared randomness.** The lushest
  arrangement may rely on information no agent has, or on random choices
  coordinated between the agents. Policies restricted to what each agent can see,
  with independent random choices, come in round 5.
- **Free coordination.** A centralised arrangement coordinates the agents at no
  cost. Rule B would charge for the signals that coordination needs. Round 3's
  deference cost s is not applied in Game 0, so results there are an upper bound
  on what coordination can achieve.
- **Small worlds.** Every game is small enough to solve exactly. Results show what
  the measure rewards in these worlds. They do not show what it rewards at scale.
- **Choices of definition.** Behaviour counts and the declared durable variables
  are modelling choices, made before computing and reported. Results at R+ and R−
  show how much they matter.

## 9. What will be reported

- every quantity listed above, raw and against the stochastic baseline;
- robustness over the box, with re-optimisation;
- the filed predictions beside the outcomes;
- a plain description of every discovered arrangement;
- an audit of each one for exploits;
- limit cases kept and labelled;
- every departure from this record.
