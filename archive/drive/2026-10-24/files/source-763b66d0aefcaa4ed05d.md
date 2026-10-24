# 10 — Omega Decision Theory

## Decision architecture

Omega Decision Theory, or ODT, organizes decisions around the difference between the complete consequential object and the model available to an agent. It makes the justification for action, the comparison of options, and the resolution of remaining conflict separately inspectable.

ODT is not a substitute name for expected utility theory, causal decision theory, or a theory of logical counterfactuals. Those approaches address questions that a concrete ODT implementation may still need to answer. ODT's distinctive focus here is the preservation of justified continuation conditions through modeling and choice.

The architecture has three stages:

```text
ODT0 — License actions against the declared continuation corridor.
ODT1 — Compare licensed actions using the supported partial ordering.
ODT2 — Apply explicit arbitration where a decision remains necessary.
```

## The decision frame

Before assessing an action, specify the affected systems, their registered requirements, available interventions, plausible contingencies, resources, and relevant horizons. Record what is known, what is estimated, and which concrete features the model omits.

The frame is revisable. Discovering another affected valuer, a hidden dependence, or a missing repair route can change the licensed set. This revision is part of decision quality, rather than an inconvenience to be suppressed after optimization has started.

GE motivates consideration for possible value under uncertainty. A decision frame records how that commitment is being applied; inclusion in the frame does not automatically require preserving every registered process. Assess the consequences of delay and inaction alongside intervention, including threats to shared continuation and the need for defense. Justifying a requirement and demonstrating that an action satisfies it are distinct tasks.

## ODT0: justification that survives contact with the world

Licensing asks whether an action preserves the justified corridor and whether its supporting argument applies to the concrete system.

Suppose an abstract model claims that a damaged process can always be repaired. That claim is useful only if the abstract repair has a realizable physical counterpart under the stated resources and contingencies. A model can invent a recovery route by dropping a dependency, merging distinct agents, or treating a merely possible intervention as available.

One sufficient pattern is a simulation relation linking abstract states and actions to concrete ones, with verified preservation of the required continuation properties. The exact proof obligation depends on whether the claim is existential, robust, probabilistic, or adversarial. An existential path in an optimistic abstraction cannot establish robust recovery in reality.

Failure of licensing can mean demonstrated violation or insufficient justification. These should remain distinct outputs. Decisions under urgency may require a registered fallback; the framework does not turn missing evidence into a theorem of either safety or catastrophe.

## ODT1: retain justified incomparability

Among licensed options, compare what the evidence and normative commitments actually support. A partial ordering can express dominance without pretending that every tradeoff has a common unit.

For example, suppose two legitimate aims remain. An option that improves both over another can dominate it. One that improves the first while weakening the second may remain incomparable. Lushness is intended as a possible adjudicator of such comparisons through their joint continuation structure. Establishing that role requires a justified relation to value-capable possibility; naming a structural score does not resolve the conflict.

When support, probability, recovery, and horizon matter differently, keep those distinctions visible. A large support containing almost no probability mass and a concentrated high-probability gain need not receive the same assessment.

## ODT2: explicit arbitration

Action sometimes requires choosing from a finite frontier of incomparable options. Arbitration can use a negotiated priority, a voting rule, a fairness criterion, a lottery, or a registered score. The authority and rationale for that rule should be recorded.

If every candidate breaches some requirement, an emergency rule may compare violations. That is a decision under conflict, not a retroactive declaration that all requirements were satisfied. Recording the breach supports later repair and institutional learning.

Finite maximization is mathematically straightforward once a score is supplied. The difficult work is whether the score is legitimate and whether its inputs faithfully describe the world.

## Low-probability claims and large stakes

ODT does not automatically solve Pascal-style problems. A claim involving a tiny probability and enormous consequence must still specify the outcome, evidential support, probability model, scope of aggregation, and possible double counting.

The architecture helps expose where the force of the argument comes from. An unbounded utility, an invented branch count, or a model that treats incompatible scenarios as simultaneously additive can dominate a calculation for reasons unrelated to the physical object. Keeping support, weight, and consequence structure separate makes these failures easier to diagnose.

Lushness research may provide more faithful comparisons of value-capable possibility. A physical profile alone does not determine the realization or ordering of value. Explicit uncertainty, partial orderings, and justified constraints on irreversible foreclosure can guide action while that connection is investigated.

The finite rare-event probe in Part 14 proves L_cov≤βp for a specific bounded-feature ensemble. It establishes sensitivity to occurrence weight under declared normalization. It does not bound every candidate lushness construction, remove calibration choices, or justify ignoring a rare catastrophe. A comparison must retain the physical event weight alongside its conditional consequence.

## Exact maximization as a research comparison

The unrestricted branch evaluates F_θ(a)=L_θ(G_a) over all physically admissible actions in a finite model. Here G_a is the full modeled continuation object and θ specifies a candidate comparison. It adds no independent ethical corridor. Practical ODT retains its stated commitments while this stronger proposal is examined.

For the same exact objective and action set A, restricting actions to a nonempty subset A_R cannot improve the attainable maximum: max_(a∈A_R) F_θ(a)≤max_(a∈A) F_θ(a). A protection can be compatible with an optimum, or help a bounded evaluator pursue the target under error. If establishing a rule changes others' behavior, that commitment is an action with a different continuation; it must be modeled as such.

Separate physical circumstances from evaluation parameters and approximation limits. Map where preferred policies change, including ties and calibration-dependent boundaries. A policy winning across a large region of parameter space is not thereby justified: a percentage requires a defended measure on that space. Candidate value–valuer accounts should supply comparisons independently of the score being assessed, so agreement can be informative rather than built into the definitions.

## Why this matters for alignment

An increasingly capable agent can optimize the wrong representation more effectively. ODT asks it to preserve the relationship between the representation and the continuation it is meant to govern: affected valuers remain represented, recovery claims remain realizable, and correction remains possible.

This is a useful research and governance target even before a universal value measure exists. It can be implemented as concrete modeling obligations, audit questions, and decision records. Success should be tested by whether those obligations catch consequential mistakes, not by whether the system produces more elaborate justifications.

Further reading: quantum and classical process models [R15, R19] inform representation; viability theory [R23] informs corridor conditions. ODT is the program's staged decision architecture.
