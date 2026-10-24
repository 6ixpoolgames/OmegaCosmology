# P001 — Does weighted distance geometry retain feedback composition?

**Specification date:** 2026-09-16, before implementation.  
**Status:** completed; results are in `report.md`; model content preserved during repository migration.  
**Question:** Can equal weighted distance matrices of normalized residual
processes hide different lawful two-step actuator responses?

## Complete finite model

This is an exact classical special case of the finite quantum realization.
The Hilbert embedding is six qubits in order `(S,M,A,R0,R1,R2)`; only diagonal
states are initialized and reachable. The full classical state space has 64
basis states. No coherent path is assigned a classical probability. The
mixed initial state is explicitly part of this finite model, with no returning
omitted environment:

`rho0 = (1/2)|000000><000000| + (1/2)|100000><100000|`.

All subsequent elementary state changes are permutations. Each implements a
unitary channel in the quantum embedding. They are defined on all 64 states,
even though only a subset is reachable. Registers are never reset or erased.
Records are physically copied into initially zero registers by CNOT. Reading
them is a computational-basis instrument; reachable states are already
diagonal. The full state and all record histories remain in the output.

The common schedule is:

1. Copy `S` into `R0`, revealing `r` to the controller.
2. Comparison action `a=0`: identity on M; `a=1`: X on M. Both occupy the
   same single mode-control slot. The action is not conditioned on r.
3. Control `b1` applies `X_S^b1`. Apply the inherited fixed Toffoli law
   `A <- A XOR (S AND M)`. Copy A into R1 and reveal `a1`.
4. Control `b2` applies `X_S^b2`. Apply the same Toffoli again. Copy A into R2.
5. Read the final output. No further controls are available in this horizon.

The mode is part of the physical state, not a changed transition law. The
controller cannot directly write M after step 2 or A at any time. Only the
stated gates are available. There are two source-control slots and three
initially zero record registers in both cases. Energetic costs are not modeled;
we claim equal slot/register budgets, not equal thermodynamic cost.

The deterministic causal policies are `b1=f(r)` and `b2=g(r,a1)`. There are
`2^2 * 2^4 = 64` syntactic policies. These are alternatives, not a distribution.
No probability prior over them is introduced. The full finite object consists
of the transition tables, scope/observation maps, and all policy-indexed
weighted occurrence trees. Probabilities belong to the initial physical
mixture and its record outcomes. Zero-weight observations are not normalized.

## Residuals and testers

At the boundary just after the comparison action, retain two normalized
residual processes `P_(m,r)`, each with occurrence weight 1/2. The common type
contains the same two remaining input slots, record outputs, and terminal
readout. A residual includes the full remaining response, not just an endpoint.

The full readout returns the entire six-bit terminal state. The controller's
earlier access is only `(r,a1)`, as specified; descriptive completeness does
not grant it additional interventions. The complete allowed testers are the
64 deterministic causal policies followed by that readout or any classical
postprocessing. Postprocessing cannot increase total variation. No additional
quantum controls, memory, randomizers, or alternate schedules are permitted.

`d(P,Q) = max_pi TV(law(P,pi),law(Q,pi))`.

Since a full output is available, this is an exact maximum for this model, not
a sampled lower bound. For each mode, holding both controls at zero returns
the original S=r at termination. Thus the two residuals have disjoint outputs
under one common tester. This supplies a lower bound 1 matching the universal
upper bound 1. The distance matrix should be `[[0,1],[1,0]]` in both modes.

Consequently the packing profile with strict separation `d > epsilon` should
be 2 for `0 <= epsilon < 1`, and 1 for `epsilon >= 1`. The associated probability
weights are identical. Equality is an isometry of these summaries; it does
not assert an equivalence of their full tester-indexed process semantics.

A second, explicitly bounded descriptor forgets everything except actuator
records `(R1,R2)` and uses the SAME policy family. This diagnoses scope loss;
it is not substituted for the full finite object.

## Structural witness and ordinary calculation

Conditioned on r and a fixed control word `(b1,b2)`:

`S1 = r XOR b1`, `A1 = m AND (r XOR b1)`,
`S2 = r XOR b1 XOR b2`, `A2 = m AND b2`.

Thus for each r, mode 0 permits only actuator record `00`; mode 1 permits
`00,01,10,11` across the four lawful control words. These are reachability
sets across alternatives, not four equally probable branches of one policy.

For any desired pair `(u,v)` in mode 1, the legal policy `b1=r XOR u`, `b2=v`
makes the pair certain. Under the exact same policy mode 0 still yields 00.
In particular `(u,v)=(1,1)` has probabilities 1 versus 0. Both actions leave
the immediate actuator at zero and the initial record weights at 1/2.

This is a composition/capability distinction within one declared model. It
does not make mode 1 better. There is no replication, valuer criterion,
self-maintenance, open-ended novelty, or lushness ordering in the fixture.

## Tests, transport and budget

Use exact integers/Fractions, standard library only. Enumerate 64 causal
policies, two actions and two initial records: 256 complete occurrences,
plus shared prefixes retained by their distinct histories. Store all 64-state
transition permutations. Check against the archived Toffoli matrix on the
eight SMA basis states, without rerunning or altering the baseline.

Check normalization for every policy, causal prefix independence from future
controls, explicit inverse/bijective gate behavior, and the analytic witness.
Transport components, initial states, gates, records and observations together
under a bijective rename and reordered coordinates; compare every transported
response and transition, not just a final scalar. Retain histories that merge
on SMA but have different record registers. Duplicating textual policy labels
may not change a maximum over testers.

No scaling is needed. Stop once the matched-geometry claim and a differing
response are established, or record an implementation/specification failure.

## Relation to earlier work and rejection target

The Toffoli dependence is reused from note 10, section 11; record-preserving
transport follows that note's section 8 and the legacy transport report's
discipline. The new comparison isolates the information lost in the entire
weighted within-family distance matrix. This is a small explicit diagnostic,
not a claim of mathematical novelty. It deliberately exploits distance
saturation. It rejects standalone weighted geometry as a complete account of
these response possibilities, while leaving weighted composition as a lead.
