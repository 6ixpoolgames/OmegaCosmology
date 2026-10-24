# 04 — Consequence and faithful compression

## What a difference leaves behind

Consequence is the difference a physical condition makes to continuation. A distinction can alter the next interaction, remain dormant in a record, become amplified much later, or change which regimes can ever be reached. The relevant object includes these dependencies, not only the next observable state.

Let Υ_P^h denote the residual continuation process at perspective P given physically meaningful conditioning information h. Depending on the setting, this may be a conditional stochastic process, a quantum process tensor, or a suitable histories or algebraic construction.

The superscript does not assume that every quantum possibility belongs to a single classical history. It identifies the boundary records, outcomes, or conditions through which the continuation is being specified.

## Continuation equivalence

Two conditions are continuation-equivalent within a declared physical domain when they generate the same statistics under every admissible continuation test:

```text
h ~_P h′  iff  p(y | T, h) = p(y | T, h′)
                 for every admissible tester T and outcome y.
```

This gives an exact equivalence relation and a quotient by consequential redundancy. The resulting object Γ_P contains distinctions that survive this comparison, together with their inherited physical relations.

The equivalence is prospective and domain-relative. It does not say that h and h′ are the same historical event, the same person, or the same global physical state. An environment outside the chosen domain can retain a distinction that the reduced continuation cannot reveal. Enlarging the domain can separate conditions previously grouped together.

Classical computational mechanics provides a close precedent: histories are grouped by their conditional distributions of futures, yielding predictive causal states. Controlled quantum processes require the corresponding richer response structure. [R19, R15]

## Why future context matters

Two qubit states can agree on all measurements in one basis yet disagree after a rotation and another measurement. If the rotation is an admissible continuation, the states cannot be merged in an exact consequence representation.

The same principle applies to practical systems. Two seeds may look identical today but respond differently to drought. Two institutions may make identical decisions under routine conditions but differ under a succession crisis. A compression that preserves their current outputs can erase their most important future distinction.

Faithful compression therefore preserves the effects of permitted future composition. For an abstract representation q and a concrete update F_a, the desired relationship is:

```text
q(F_a(x)) = F̄_a(q(x))
```

where F̄_a is the corresponding abstract update. In stochastic and quantum models the statement concerns compatible transition laws or process maps. This relation must be checked; equality on a narrow set of current observations does not guarantee it.

A three-bit example makes the requirement exact. Let X, Y, Z take values ±1, with joint law P_t(x,y,z)=(1+txyz)/8 for −1≤t≤1. Every preparation has zero means and covariance I₃. Apply the reversible gate (X,Y,Z)→(X,Y,XYZ). The output means become (0,0,t) and its covariance becomes diag(1,1,1−t²). One identical input summary would have to produce different output summaries under the same gate. No exact abstract update exists on means and covariance alone for this family.

The full joint representation predicts the result. The repair is also determined by the continuation: pulling the future last-bit readout back through the gate requires the observable XYZ. Retaining it alongside the constant, single-bit, and pair-product observables completes a basis for all functions on these eight states. This is an instance of closure under permitted future tests, rather than a decision to reward correlation.

Part 13 extends the example to a conditional information-transfer capability. Even the complete unconditional output state can conceal that relation when the input is averaged away. A faithful response object retains the conditional laws and their physical input correlations. A scalar comparison need not preserve every distinction, but it cannot substitute for the full process when predicting its continuation.

## Horizon and resolution

At horizon H, compare the tests whose relevant output can occur within H. Increasing H expands the questions and can reveal delayed distinctions. Under nested test domains, the resulting equivalence classes refine as the horizon increases.

A useful discrepancy is:

```text
d_P,H(x, y) = sup_T TV[p(· | T, x), p(· | T, y)],
```

where TV is total variation distance and the supremum ranges over the stated testers. This is a pseudometric before quotienting. For unrestricted single-system state discrimination, the corresponding distance is trace distance. Multi-round processes have their own discrimination constructions. [R06, R07, R15]

An approximation tolerance ε can bound the error in relevant predictions. Pairwise closeness alone should not be treated as exact identity: “within ε” is generally not transitive. Use an explicit partition, cover, or encoding with a verified distortion bound.

## The global target

The full object is approached through enlarging physical domains, richer admissible interactions, longer horizons, and finer controlled descriptions. There may be no finite computable representation containing all of it. That is a limitation on our access, not an instruction to redefine consequence as whatever a convenient model notices.

This is also where the proposed ultimate resolution belongs. At the most complete level, distinctions stop mattering to consequence only when the full applicable physical theory makes them continuation-equivalent. Quantum incompatibility helps determine the structure of that theory. A numerical Planck-length cutoff is not needed to define the target.

Calling the quotient “quantization” can gesture at removing spurious multiplicity, but exact equivalence need not produce finitely many discrete classes. Quantum state spaces themselves contain continuous families. The rigorous work is the identification of physically meaningful distinctions and their composition, followed by controlled approximation.

## Preserved structure

Γ_P should retain more than a set of labels. Depending on the realization, it carries distances, causal relations, coherent combinations, physical weights, permitted transformations, and conditional continuation. A successful compression retains the parts required to reconstruct consequential behavior within its domain.

This is the bridge to lushness: once redundant descriptions have been removed without discarding real consequence, ask what richness remains.

Further reading: predictive causal states [R19]; quantum process descriptions [R15, R16]; operational distinguishability [R06, R07, R36].
