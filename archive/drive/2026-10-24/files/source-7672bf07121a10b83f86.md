# 13 — Worked examples

These small models show what the framework's distinctions do. Their conclusions are exact within the stated settings. They provide tests for larger constructions, not a numerical definition of value.

## 1. A phase that a coarse description misses

Take two qubit states:

```text
|+⟩ = (|0⟩ + |1⟩)/√2
|−⟩ = (|0⟩ − |1⟩)/√2.
```

A measurement in the 0/1 basis returns equal probabilities for either state. A description retaining only those probabilities merges them.

A measurement in the +/− basis distinguishes them perfectly. If that measurement is an admissible continuation, their difference is consequential. The compression failed because it discarded phase that could influence a later interaction.

If the physical channel first completely dephases both states in the 0/1 basis and access to the environment is excluded, both become I/2 on the system. They are then equivalent for subsequent tests on that reduced output. The difference between these cases is a physical operation and access domain, not a change in descriptive taste.

## 2. The same local present, different continuation

Use two bits S and E, represented as diagonal two-qubit states. Prepare either a matching correlation or an opposite correlation:

```text
ρ_match = (|00⟩⟨00| + |11⟩⟨11|)/2
ρ_opp   = (|01⟩⟨01| + |10⟩⟨10|)/2.
```

In both cases S alone is uniformly random, and so is E. Now apply the reversible interaction S ← S XOR E, leaving E unchanged.

For ρ_match, S becomes 0 with certainty. For ρ_opp, S becomes 1 with certainty. The same local density operator at the first boundary did not determine the later local state. The joint correlation plus dynamics did.

This example needs neither consciousness nor quantum entanglement. It isolates why full continuation can contain information absent from instantaneous marginals.

## 3. Focus in a quantum eraser

Prepare the idealized entangled state:

```text
|Ψ⟩ = (|a⟩|0⟩ + |b⟩|1⟩)/√2,
```

where a and b are orthogonal signal paths. Tracing out the marker yields the signal mixture:

```text
ρ_signal = (|a⟩⟨a| + |b⟩⟨b|)/2.
```

Measure the marker in the +/− basis. Conditional on +, the signal is (a+b)/√2; conditional on −, it is (a−b)/√2. Let ψ_a(x) and ψ_b(x) be the path amplitudes at a screen. The conditional distributions are:

```text
p(x | ±) = |ψ_a(x) ± ψ_b(x)|² / 2.
```

Each marker outcome has probability 1/2. Their mixture is:

```text
p(x) = [|ψ_a(x)|² + |ψ_b(x)|²] / 2.
```

The cross terms cancel. Conditional focus reveals different organized subsets; the unconditional signal statistics remain unchanged. The ideal model captures the central conditional structure of the delayed-choice experiment. [R12]

## 4. Representation duplication and physical redundancy

First, take a physical state x and introduce a thousand names for it. A consequence quotient identifies the names whenever they denote the same process. No physical capability has been added.

Next, store a recoverable classical record in two locations with independent failure probability p. If either surviving location suffices for restoration, total failure has probability p². A single copy fails with probability p.

These are different cases. Independent storage changes the process under disturbance. A common catastrophe that destroys both locations can remove the advantage, so the failure model belongs in the comparison. Arbitrary unknown quantum states cannot simply be duplicated by the classical copying procedure; quantum protection needs an appropriate encoding and noise model.

## 5. Horizon-dependent recovery

Consider a deterministic transition graph with damaged state D, repair state R, and restored state A:

```text
D → R → A.
```

Recovery to A is impossible within one step and possible within two. A short-horizon quotient can therefore hide a real return route.

Now add a transition from A to failure F on the following step unless a resource-consuming maintenance action is taken. Reaching A and remaining viable are different claims. A longer horizon reveals recovery in the first question and a new obligation in the second.

## 6. Everyone individually repairable, no joint repair

Two systems A and B are damaged. A single indivisible resource can repair either one and is consumed. There is no replenishment or sharing within the model.

Each individual has a repair route. There is no route repairing both. Formally, “for each i there exists a successful policy” does not imply “there exists one policy successful for all i.”

A related three-system case has enough resources for any two, but not all three. Every pair is compatible; the whole family is not. Marginal or pairwise summaries lose a decisive constraint.

## 7. A policy atlas needs a selector

There are two unobserved environments, e₀ and e₁, and two policies. Policy π₀ succeeds only in e₀; π₁ succeeds only in e₁. Every environment has a successful policy, but no fixed policy succeeds in both.

The two success regions form a cover. Using that cover robustly requires an available way to identify the relevant region and select its policy. If sensing supplies that information in time, an adaptive policy may solve the problem. Without it, the cover is only an existential catalog.

Nor does needing two policy behaviors imply needing two valuers. One controller can implement both when its architecture and information allow it.

## 8. Breadth at fixed covariance

Compare positive semidefinite matrices with eigenvalues (M,0,…,0) and (M/r,…,M/r,0,…,0), with r nonzero entries, M > 0. They have the same trace M.

For β > 0:

```text
L_narrow = log(1 + βM)
L_broad  = r log(1 + βM/r).
```

For r > 1, L_broad exceeds L_narrow. The statistic detects independent spread at matched total covariance. Whether the chosen covariance faithfully represents consequence is a separate modeling question.

## 9. A decision without invented commensurability

Suppose three licensed actions have validated outcome profiles A=(1,0), B=(0,1), and C=(0,0), where both coordinates are to be increased. A and B each dominate C, while neither dominates the other.

ODT1 removes C from the undominated frontier. ODT2 can select between A and B using an authorized priority or lottery. A chosen weighted sum is an explicit arbitration commitment; it is not a discovery that the two aims were secretly measured in the same unit.

## 10. A hidden dependency becomes a continuation capability

Let X,Y,Z∈{−1,+1} have joint law P_t(x,y,z)=(1+txyz)/8, with −1≤t≤1. Their means vanish and their covariance is I₃ for every t. At t=0 the bits are independent; at t=1 they obey Z=XY.

An independent physical input U∈{−1,+1} controls a sign flip. A fixed parity decoder then acts reversibly:

```text
(X,Y,Z) → (X,Y,UZ) → (X,Y,UXYZ).
Receiver output W = UXYZ.
P(W=w | U=u,t) = (1+tuw)/2.
```

The full model retains U and all register outputs. The receiver reads only W. No direct input wire, reset, fresh blank receiver register, or swap of U into W is permitted. Both preparations face the same interface and operations; their preparation entropies differ, so this does not compare equal preparation costs.

| Dependency | Initial covariance score at β=1 | Separation of conditional receiver laws | Best recovery with fair U |
| --- | ---: | ---: | ---: |
| t=0 | 3 log 2 | 0 | 1/2 |
| t=1/2 | 3 log 2 | 1/2 | 3/4 |
| t=1 | 3 log 2 | 1 | 1 |

The exact separation is |t| and recovery is (1+|t|)/2. The independent preparation is uniform on eight states and unchanged by any reversible register permutation. Its quantum realization I₈/8 is also unchanged by any unitary on that register. Input-selected reversible register operations alone therefore cannot transfer U into this receiver at t=0. The parity preparation permits perfect transfer.

This result survives an exhaustive check of the distinct one-bit readouts of eight-state reversible decoders. Each is a balanced Boolean function f with four positive outputs and has a reversible extension. There are 70: 36 expose no dependency, 32 give separation |t|/2, and two give |t|. The direct readout W=UZ is a zero-transfer control. These counts do not supply a probability prior over operations.

If the fair input U is averaged out, the entire receiver register is uniform for every t. The full joint object still retains E[UW]=t. Even a complete unconditional receiver snapshot therefore fails to characterize input transfer. The conditional response object captures it.

There is a direct comparison independent of the diversity formula. With receiver-only stochastic postprocessing allowed, a channel of strength t can reproduce strength s whenever |s|≤|t|. For t≠0, multiply W by an independent sign R with E[R]=s/t. The converse fails for |s|>|t| because such processing cannot increase the separation of conditional output laws. This orders the specified transfer capability, not the global value of the preparations.

The two response laws also provide a test of richer summaries. Under the physical fair input and similarity 1−TV, D₂=1/(1−|t|/2). Weighted covering with centers in the response family needs two balls precisely when ε<|t| and δ<1/2. Both detect the demonstrated change. The underlying representation already retained it; the deficient object was the covariance compression. A scalar evaluation can still tie different processes without being wrong.

## What these examples establish together

Phase, joint correlation, access, horizon, redundancy, shared resources, and information for policy selection all change continuation. A proposed consequence representation must preserve their effects within its declared domain. A candidate lushness summary must state which aspects it compares and justify the distinctions it discards for that purpose. The continuation test supplies a concrete sufficiency requirement without prescribing a value ranking. Part 16 links its exact enumeration and the accompanying calibration and rare-event probes.
