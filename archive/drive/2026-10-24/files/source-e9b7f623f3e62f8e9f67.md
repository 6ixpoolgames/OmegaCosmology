# Constraint and domination: locating the boundary between good and bad — design r3

**Date:** 15 October 2026.
**Status:** design for discussion. Expectations are working guesses to learn
from, not pass/fail thresholds (ruling 12).
**Supersedes:** design r2. Iteration 1 of r2 has run (the first friction map).

## Originator's framing

From 14–15 October:

- Suffering is not needed for domination. Benevolent totalitarianism is
  possible. The property to test is reachable state space.
- Score lushness from the dominator's, the dominated's and the whole field's
  perspectives.
- Everything is a valuer in the theory, even gas.

New on 15 October, after the first friction map:

- "Defining domination as bad is a mistake." Being under a rule of law in a good
  society is structurally similar to the paternalist case.
- Lushness's advantage is that a parameter sweep can locate, up to modeling
  resolution, the level of suppression at which domination turns from good to
  bad.
- The current model probably misses the opportunity cost of coercion against
  free exploration. A model that is too simple cannot show it. One that is too
  handmade gives predictable dynamics and equilibria, which is still better
  than nothing.
- Run the sweeps.

**Terminology.** "Domination" and "constraint" name the setup, not a verdict.
The kinds below are named by what the constraint targets. Lushness supplies the
verdict, and the structural account explains it.

## What the first friction map established

- Whole-field lushness separated helpful from harmful constraint by physical
  consequences alone, with no reward for protection or penalty for control.
  From T64 onward, at every cadence:
  - steering away from the trap: +9.5 to +13.2 bits;
  - blocking or redirecting resource access: −6.3 to −8.4;
  - blocking construction: −4.5 to −6.0;
  - steering back into the trap: −7.6 to −9.9.
- The dominated party's own lushness moved with the whole field's in all 20
  cases. The helpful constraint was the one S itself would choose.
- Stocks did not decide the ranking, and total capture did not track breadth.
- The dominator's own lushness was unresolved in every case.

**Why the paternalist result was guaranteed.** The trap was a pure loss: a
low-mobility well with nothing to find in it. The environment was fixed and the
dominator knew it exactly. Steering S away from the trap therefore had no
opportunity cost, so constraint on it could only help. This is the
too-handmade problem in action, and it is why the paternalist case shows no
transition to bad.

## Stage A: complete the sweeps in the current world

Cheap, and needed before anything is added.

- **Strength.** φ on a fine grid from 0 to 0.95, for every target, in both
  modes. Locate any crossing where the whole-field difference from idle changes
  sign.
- **Cost,** including cheap friction, so that extraction can pay the
  dominator. That produces the case where the dominator's own lushness rises
  while the field's falls.
- **Controls:**
  - a random region matched on fuel actually spent, not on φ;
  - neutral states;
  - all transitions.
- **Forced labour:** confinement *in* construction or access states. This is
  constraint that raises measurable output.
- **The swap:** the dominator's slot filled by a regular agent, and by gas.
- **Tighter bounds on D's own history,** so the dominator's perspective
  resolves.
- **One energy-shift realization,** as a check on how friction is implemented.

**Output:** crossing curves φ* by target, cost, κ and supply, reported only
where the sign holds across the cadence corridor.

## Stage B: the opportunity cost of coercion

Each mechanism is physical, and each gives free exploration a value that
constraint can forgo.

1. **Hidden, changing opportunities.** Resource sites move, appear and
   disappear at a rate ν, the novelty rate. The dominator does not observe them
   directly; S encounters them by being there. Free exploration finds them, and
   constraint confines S to where the dominator believes value lies.
2. **Exploration with discovery.** Risky states double as exploration.
   Entering them carries a chance of finding a new site or construction route
   that raises later capture: the adjacent possible. Constraint on risky states
   now has a cost, so a transition from good to bad becomes possible.
3. **The dominator's knowledge.** The dominator's picture lags the environment
   by an update delay, or it sees only a noisy signal. The oracle dominator of
   the first map is the limit case. This is the knowledge test (C11).
4. **Harms among the governed.** Two governed agents can raid each other,
   taking resource or damaging apparatus. Constraint on raiding is protection of
   one party's channels from another. That is the core of a rule of law and of
   the anti-excision clause (ruling 3).
5. **The form of the rule:**
   - **general or discretionary:** conditioned on physical state and applied
     equally to all governed agents, or conditioned on the dominator's own gain
     and aimed at one agent;
   - **reciprocal or exempt:** whether the dominator is bound by the same
     rule.
6. **Who pays.** Friction funded from the dominator's store, or by a levy on
   the governed agents' capture (taxation).

## The central output: a map of good and bad constraint

Plot the whole-field difference from the unconstrained world, and each party's,
against two axes:

- **suppression level:** the realized fraction of the governed agents' native
  flux suppressed or redirected. This is physical, not lushness, so the axis is
  not circular;
- **a world axis:** novelty rate ν, the dominator's knowledge quality, or the
  probability of discovery.

The zero contour separates good constraint from bad. The questions it answers:

- Is there an interior optimum, a level of constraint better than none, beyond
  which constraint turns bad? That would be the shape of a rule of law against
  tyranny.
- Does the optimal level fall as novelty rises or the dominator's knowledge
  degrades?
- Do general, reciprocal rules keep a wider good region than discretionary,
  exempt ones?
- Does protecting the governed from each other stay good at higher suppression
  than constraining an agent's self-regarding risk?
- Where do the perspectives diverge, with the dominator gaining while the field
  loses?

Boundaries are claimed only where the sign holds across admissible grains;
grain-dependent bands are marked as such.

**Findings that would bear on the principle:** a lushness verdict that the
structural account cannot explain. For example, lushness favouring a constraint
that closes the governed agents' generative channels with no compensating access
anywhere in the field, robustly across grains and horizons.

## Avoiding handmade equilibria

- **Random-world ensembles.** Generate many small worlds with site payoffs,
  discovery probabilities, trap depths and coupling drawn at random within
  physical bounds. Classify roles from physics after generation. Report the
  distribution of boundaries across the ensemble rather than the result of one
  designed world. The boundary then belongs to the class of worlds, not to a
  tuned instance.
- **A nonstationary environment,** so no fixed point is designed in.
- **The handmade world and the oracle dominator** are kept as limit cases.

## Compute

- Each world is solved exactly, within about 4,000 states.
- Identical governed agents are represented by counts, as B12 asks, with one
  tagged agent for the self perspective.
- An ensemble of 50–200 small worlds is feasible at the current case cost of
  about 20–40 seconds each.
- Larger worlds wait for the streaming entropy backend.

## Staging

- **Stage A:** sweeps and controls in the current world.
- **Stage B1:** exploration with discovery and moving sites; oracle against
  lagged dominator. The first good-and-bad map, over φ × ν × knowledge.
- **Stage B2:** two governed agents with raids; general against discretionary
  rules; reciprocity; taxation.
- **Stage B3:** random-world ensembles over B1 and B2.
- **Later:** revolt and correction by the governed; concentration (one
  governor, many governed); plural ecology (C6); steering by punishment against
  incentive (C19); spatial worlds.
