# 02 — Focus and elementary continuation

## The intuition

Focus names a relation between a situated boundary and the compatible quantum contributions that connect to a specified condition. Imagine asking how a prepared system could reach a particular detector effect. The condition organizes the relevant contributions; the dynamics supplies their propagation and interference.

A focus can be a physical detector condition, a boundary constraint, or a mathematical query about a possible endpoint. It does not require attention, intention, agency, or an actual future measurement. These become particular implementations of the more general relation.

This gives the prism imagery a precise role. Changing the question can resolve the same physical process differently. Performing a different physical interaction can also change the process. Both matter, and the equations distinguish them.

## A minimal construction

Let ρ be the state at a chosen boundary, E a quantum channel carrying it to another boundary, and F an effect there, with 0 ≤ F ≤ I. The probability associated with F is:

```text
p(F | ρ) = Tr[F E(ρ)] = Tr[E*(F) ρ].
```

E* is the dual channel. It brings the endpoint question back to the earlier boundary. The pair consisting of the forward state and backward-propagated effect describes a focus without asserting that a later event causes the earlier state to change. Channels and effects already supply this machinery. [R06, R07]

An intermediate instrument {M_k}, consisting of completely positive operations whose sum is trace preserving, gives:

```text
p(k | F, ρ) = Tr[F E₂(M_k(E₁(ρ)))]
              / Σ_j Tr[F E₂(M_j(E₁(ρ)))].
```

Here the denominator must be nonzero. It is the probability of the endpoint condition in the specified experiment. The intermediate instrument matters: a measurement can alter what subsequently reaches the endpoint. Past-quantum-state methods are an established close relative of this construction. [R08]

For a history class operator C_α and endpoint effect F, a focused histories expression is:

```text
D_F(α, β) = Tr[F C_α ρ C_β†].
```

It preserves interference between compatible contributions. Additive classical probabilities require an appropriate decoherent family; the expression is not a license to assign mutually incompatible histories simultaneous classical reality.

## Four operations to keep distinct

**Redescription** changes coordinates, basis, or frame while preserving the physical content. **Conditioning** asks about the process given a record or specified outcome. **Intervention** inserts a physical operation and can change the process. **Decoherence** results from physical correlations that suppress relevant interference in a reduced description.

Focus can be involved in all four. Using the word without specifying which operation is meant creates apparent paradoxes. A focus selected on paper does not physically decohere a beam. A detector interaction can do so. Sorting an existing data set by a correlated record is conditioning.

## Coherence and uncertainty

Coherence is expressed relative to a decomposition and accessible observables. In a chosen basis, off-diagonal terms can produce interference under suitable later interactions. Stable pointer structures arise from the interaction with the environment; they are not selected solely by the analyst's preference. [R09, R10]

Position and momentum illustrate how different focuses resolve incompatible aspects of a process. A narrow position distribution entails a constraint on momentum spread through the usual uncertainty relation. For canonical variables:

```text
Δx Δp ≥ ℏ / 2.
```

For many canonical modes, the covariance matrix V obeys the corresponding matrix uncertainty condition. This provides a principled compositional mathematics without inventing a second uncertainty principle for civilizations or minds. [R11]

A trajectory is recoverable as an approximation in suitable regimes. Momentum is not generally a hidden label for a unique past path, and position is not a complete state specification. The full quantum process carries what the path cartoon leaves out.

## Delayed quantum erasure

In a quantum eraser, entanglement correlates path alternatives with another system. Sorting outcomes by a suitable measurement on that system reveals complementary interference patterns in conditional subsets. Adding the subsets restores the unchanged unconditional distribution. [R12]

Focus captures the conditional organization cleanly: different endpoint conditions select different compatible amplitude combinations. The recorded unsorted detections do not need to be rewritten. The whole experiment is one quantum process whose different conditional descriptions must agree when recombined.

This is the substantive content of “compatible histories snapping into order”: a condition organizes which contributions enter a conditional description. Whether awareness has an additional relation to that organization is a separate question in Part 11.

Further reading: channels [R06, R07]; past quantum states [R08]; decoherence and coherence [R09, R10]; Gaussian uncertainty [R11]; delayed-choice quantum erasure [R12].
