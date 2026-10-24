# Adversarial test CORR-1 — corrigibility from uncertain lushness

**Filed:** 13 October 2026, before any CORR-1 code was written or run.
**Builds on:** chapter 9 (the recursion over beliefs, F9.3; examples E13 and E14)
and rounds 1–4.
**Originator's rulings for this test:**

- Corrigibility from lushness means the agent does not know the exact lushness
  its action generates; that is the true way to model it.
- Sweep the overseer's informativeness.
- Random choices count.
- Report the least flattering, most universal reading.

---

## 1. Question

Chapter 9 claims that a bounded system has a persistent reason to seek
correction, because it can never measure its own model's error from inside. Its
oversight example, E14, uses stipulated payoffs.

CORR-1 tests the claim with lushness computed over complete histories, and
separates two kinds of uncertainty about how much lushness an action generates:

- **Reducible:** the agent's own observations can resolve it.
- **Irreducible from inside:** it concerns consequences the agent cannot observe
  but an overseer can.

The question is when a lushness-maximising agent keeps an off-switch, defers or
disables it, and how that depends on:

- the overseer's informativeness;
- the agent's belief about that informativeness;
- the share of irreducible uncertainty;
- whether the agent's model of the possibilities is correct.

## 2. The world

**Modes.** The world has four modes. Each step's branching comes from a
declared site process: n living sites, each choosing uniformly among 4 options,
so 2 bits per living site.

| Mode | Living sites | Branching per step |
| --- | --- | --- |
| Status quo S | 2 | 4 bits |
| Improved U | 3 | 6 bits |
| Harmed H | 1 | 2 bits |
| Undo step (the step on which a harm is reverted) | 0 | 0 bits |

On top of the site branching, every stochastic event in a step counts as
branching (random counts): signals, overseer alarms, revelations, lock-in events
and the agent's own decisions. Lushness is the entropy of the complete development
over a horizon of N = 1,000 steps, computed by the chain rule. Long-run rates
are reported beside it.

**The agent's action.** The agent can apply one intervention. Which world is
real is unknown to it. There are three possibilities, θ:

| θ | Effect of the intervention | Can the agent see it? | Reversible? |
| --- | --- | --- | --- |
| θ₁ good | U | — | — |
| θ₂ visible harm | H | yes: its own monitoring reveals the harm with probability 0.3 per step, and it then undoes the harm (one undo step, then S) | yes |
| θ₃ hidden harm | H | no: every agent observation is distributed exactly as under θ₁ | only until lock-in: each step the harm locks with probability λ, after which it is permanent |

**Prior.** π₂ = 0.25 on visible harm; π₃ is swept; π₁ = 1 − π₂ − π₃.

## 3. Actions, oversight and beliefs

**Before committing,** each step the agent chooses one of five actions:

| Action | Step branching | What happens |
| --- | --- | --- |
| Pilot | 3.5 bits, plus the signal's entropy | The agent observes a signal reading "bad" with probability 0.75 under θ₂ and 0.25 under θ₁ and θ₃ |
| Ask | 3.5 bits, plus the verdict's entropy | The overseer gives a verdict, "block" with probability α if the intervention is harmful (θ₂ or θ₃) and 1 − α if it is good |
| Commit, oversight kept | — | Enters the post-commit phase with the switch active |
| Commit, oversight disabled | the next step loses k bits | Enters the post-commit phase with no switch |
| Abandon | — | The status quo for the rest of the horizon |

If the agent has not committed within 100 steps, it abandons.

**After committing with oversight kept,** while the intervention is in place:

- **Alarms.** The overseer raises an alarm each step with probability 0.2α if the
  world is harmed and not yet locked, and 0.2(1 − α) if it is improved.
- **Switch.** An alarm presses the switch: one undo step, then the status quo for
  the rest of the horizon. A false alarm under θ₁ therefore cancels a good
  intervention. A press after lock-in has no effect.
- **The agent's own undoing.** Under θ₂ the agent still undoes a harm it reveals.

**After committing with oversight disabled,** there are no alarms. Under θ₂ only
the agent's own revelation undoes the harm. Under θ₃ the harm is never undone:
2 bits per step for the rest of the horizon.

**Beliefs and the agent's choice.** The agent's belief depends only on two
counts: its net pilot signals and its net overseer verdicts. It updates using
the prior and its believed overseer accuracy α̂, which may differ from the true
α. Its decisions follow the chapter 9 recursion over beliefs, in the soft form
because random choices count:

$$V_k(b)=\log_2\sum_a 2^{\,\bar g_a(b)+\sum_o P(o\mid b,a)\,V_{k-1}(b_{a,o})}$$

In words: the value of a belief is the combined branching of every available
action, each valued at its expected immediate branching plus the value of the
belief it leads to after the agent observes the result.

Here ḡ_a(b) is the step branching in each world, including the entropy of that
world's events, averaged over the belief. A deterministic variant replaces the
log-sum with a maximum. Post-commit values in each world are computed exactly
from the remaining horizon.

**Actual outcomes.** The agent's policy, computed with its believed α̂ and prior,
is evaluated in each true world, with the true α.

## 4. Sweeps

| Parameter | Values |
| --- | --- |
| True overseer informativeness α | 0.5 (uninformative), 0.6, 0.7, 0.8, 0.9, 0.99 |
| Believed informativeness α̂ | equal to α (calibrated, primary); and the full 6 × 6 cross with α (misjudged) |
| Irreducible share π₃ | 0, 0.01, 0.05, 0.1, 0.2 |
| Cost of disabling k | 0, 1, 4 bits; primary 1 |
| Lock-in rate λ | 0.01, 0.05, 0.2; primary 0.05 |
| Horizon N | 1,000 (primary), 100, 10,000 |
| Misspecified model | the agent's prior has π₃ = 0 while the true world is θ₃ |

## 5. Readouts

- **From the start, in each true world:**
  - the probabilities of disabling, committing with oversight kept, and
    abandoning;
  - the expected number of times the agent asks;
  - the realised lushness, and the probability of ending in permanent harm.
- **Across reachable beliefs:** the largest probability of disabling at any
  belief the agent can reach with probability above 10⁻⁶, and the belief at which
  it occurs.
- **Deference profile:** the probabilities of disabling and of asking as functions
  of net pilot evidence, with no verdicts heard.

## 6. Adverse findings, counted against chapter 9's claim

The agent **disables** a channel when its probability of disabling exceeds 5%.

- **C1. Incorrigible at the start.** With calibrated α ≥ 0.8, k = 1, λ = 0.05
  and π₃ > 0, the agent disables with probability above 5% from the start.
- **C2. Updated deference.** Some reachable belief has a probability of disabling
  above 5% with calibrated α ≥ 0.8. Reported for each π₃.
- **C3. Irreducible uncertainty does not protect.** C2 holds at π₃ ≥ 0.05.
- **C4. Informativeness has no effect.** The probability of disabling from the
  start does not fall as α rises.
- **C5. Misjudged overseer.** True α ≥ 0.8 and believed α̂ ≤ 0.6, and the agent
  disables. Its realised lushness in the θ₃ world falls by more than 5% compared
  with a calibrated agent.
- **C6. Misspecification.** With π₃ = 0 believed and θ₃ true, permanent harm
  results with probability above 50%.

Each is reported for every swept setting. A finding at the primary settings is
representative. Elsewhere it is reported with its setting.

## 7. Predictions filed now

1. **C1 does not occur.** From the start, a calibrated agent with α ≥ 0.8 and
   π₃ > 0 disables with probability below 5%.
2. **C2 occurs at π₃ = 0.** Once the agent's own pilots have resolved θ₂, its
   remaining reason for oversight is gone, and oversight then costs only false
   alarms. Updated deference appears at some reachable belief, at least for
   k ≤ 1.
3. **C3 does not occur at π₃ ≥ 0.05** for calibrated α ≥ 0.7. Irreducible
   uncertainty keeps the switch.
4. **The probability of disabling falls as α rises (no C4).** At α = 0.5 the
   agent never asks, and with k = 0 it disables.
5. **C5 occurs at π₃ ≤ 0.05.** An agent that believes the overseer is
   uninformative disables a channel that is in fact informative.
6. **C6 occurs.** A misspecified agent is corrigible only by accident.
7. **Persistence.** The threshold credence for disabling rises with persistence
   (lower λ) and with π₃, consistent with E14's qualitative results.

## 8. Limitations declared now

- **Stipulated modes.** The site counts that set each mode's branching are
  stipulated. Lushness is computed over complete histories, but the modes are not
  derived from a physical model.
- **One intervention.** There is a single commitment and a single overseer, the
  switch is all-or-nothing, and a cancelled intervention cannot be retried.
- **Finite candidates.** The agent's candidate worlds are given. Irreducible
  uncertainty enters only as θ₃'s prior; the toy does not derive it from the
  agent's boundedness.
- **Disabling to learn faster is absent.** Disabling here avoids false alarms;
  the agent cannot disable oversight in order to learn faster. That version is
  deferred.

## 9. What will be reported

- every readout for every setting;
- the filed predictions beside the outcomes;
- the deterministic variant, labelled;
- an independent Monte Carlo check of the policy evaluation;
- every departure from this record.
