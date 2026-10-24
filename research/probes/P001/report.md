# P001 result — Equal distance geometry can hide different feedback responses

**Status:** exact finite counterexample, with an ordinary analytic explanation.  
**Date:** 16 September 2026.  
**Specification:** [Model specification](spec.md).  
**Machine-readable evidence:** [Expected exact results](evidence/EXPECTED.json).

Two actions in one fixed finite model leave equally weighted residual families
with identical full distance matrices. Their permitted two-step actuator
responses differ. The missing information remains in the tester-indexed
response maps and in the subsequent state/record transitions.

## Exact comparison

The fixture extends the source–memory–actuator Toffoli law in formal note 10.
It uses its classical diagonal subcase with explicit record registers, two
source-control slots, and the same initial state for both comparison actions.
One action leaves M at zero; the other flips M to one. The transition law and
remaining control menu are unchanged.

At the boundary immediately after that action, the actual initial record r
has two alternatives, each with weight 1/2. Each normalized residual process
contains the response to the entire remaining two-slot schedule. We computed
all 64 deterministic causal policies, conditional on both initial records,
for both actions. No distribution over policies was supplied.

| Quantity | M=0 | M=1 |
| --- | --- | --- |
| Immediate actuator | 0 | 0 |
| Boundary occurrence weights | 1/2, 1/2 | 1/2, 1/2 |
| Full distance matrix of the two boundary residuals | `[[0,1],[1,0]]` | `[[0,1],[1,0]]` |
| Packing number for 0 <= epsilon < 1 | 2 | 2 |
| Packing number for epsilon >= 1 | 1 | 1 |
| Possible actuator-record pairs for either r, over legal control words | `00` | `00,01,10,11` |
| Under one common policy b1=1-r, b2=1 | `00`, probability 1 | `11`, probability 1 |
| Distinct full states after first source-control slot | 4 | 4 |
| Distinct full states after second source-control slot | 4 | 8 |

The four possible records in the M=1 row are alternatives obtainable with
different controls. They are not four outcomes each assigned probability 1/4.

For a fixed r and controls `(b1,b2)`, the law gives

`A1 = M * (r XOR b1)` and `A2 = M * b2`.

For a desired actuator pair `(u,v)`, the policy `b1=r XOR u, b2=v` realizes it
with certainty at M=1. M=0 always gives `00`. This is a witness about lawful
control responses, without a preference assigned to any pair.

## Why the geometry loses the difference

Holding both controls at zero leaves final S=r. The two normalized boundary
residuals therefore have disjoint outputs under a common lawful tester,
in either mode. Their distance is at least one, and total variation is at most
one. The exact optimum is one; no optimization over an untested continuum is
being claimed.

More generally, suppose residual processes have deterministic outputs under
every tester in a common family. Two different response functions differ on
some tester. Their point-mass output laws then have total variation one.
Otherwise every tester agrees and the distance is zero. Thus the maximum-TV
metric on the distinct response functions is discrete: its pairwise distances
do not retain which interventions produced which outputs. This is an ordinary
proof under the stated determinism assumption, not a quantum-general claim.

The fixture was intentionally chosen to expose this saturation. It is a
transparent diagnostic, not independent evidence for or against the existence
of lushness. The general issue was already anticipated in the handoff; this
session supplies a concrete, reproducible instance.

## Scope of the rejection

The rejected proposal is that the weighted distance matrix of this boundary
family is a complete description of its feedback response possibilities.
The result applies even though each point denotes a complete remaining
process, rather than an endpoint state. Taking pairwise maximum distances is
still a lossy operation on those processes.

**The comparison does not match the geometry of every later reachable family.**
The table explicitly shows different terminal full-state support sizes, 4
and 8. A descriptor retaining such stage-indexed families could distinguish
this pair. The result therefore does not establish that all possible forms
of continuation geometry fail, or that composition cannot be represented
geometrically. It also does not compare complete semantics as if they were
identical: the common-policy witness proves they are different.

In the bounded actuator-record scope the distance between the r residuals is
zero for M=0 and one for M=1. The full descriptor saturates in both cases.
This illustrates dependence on the observation map. The bounded descriptor
has not thereby become the global substrate or an ethical score.

## Verification and provenance

- The unchanged inherited baseline passed all 233 checks and exactly matched
  its archived JSON. All 66 inventoried source-package files matched their
  recorded digests.
- Eight focused test methods passed. They check the feedback permutation
  against the archived exact quantum matrix; reversibility of all gates on
  all 64 states; normalization and the independent formula for every policy;
  causal prefix independence; the witness and strict packing thresholds;
  scope/duplicate-label behavior; full presentation transport; and retention
  of different occurrences that share the same working SMA state.
- Presentation transport renames and reverses all six coordinates, carrying
  initial states, gates, records and observations along with them. Every gate
  transition and all 256 complete conditional responses commute with it.
- The calculations use only exact integers and rational probabilities under
  Python 3.12.14. No source file was edited; no legacy Lean suite was rerun.
- [Provenance](evidence/PROVENANCE.json) records the original result hashes and
  repository migration. [Full objects](evidence/FULL_OBJECTS.json) preserve the
  exact transition tables and occurrence trees. Current source hashes are
  written into each new run's summary.

From this repository, with Python 3.10 or newer:

```text
python scripts/check_workspace.py --out-dir runs/P001_reproduction
```

Choose a fresh output directory. This verifies imported sources, runs the
focused tests and baseline, and compares reproduced P001 semantics and full
objects with the retained evidence. The core physical model is unchanged.

## Interpretation and next question

**Structural result:** weighted pairwise distinguishability of the selected
boundary family omits a real difference in controlled continuation.

**Interpretation:** the handoff's insistence on keeping composition alongside
geometry is warranted in this example. An unlabelled maximum-distance summary
discards the relation between control and consequence.

**Unresolved bridge:** neither the response maps nor the extra reachable
actuator records have been connected to valuerhood, phenomenality, persistence,
or greater value substrate. This model has no open-ended generativity and
does not justify calling one setting ethically superior.

The next structural test could match the support sizes and distance profiles
at every stage while varying their allowed sequential connections. That would
remove the simple terminal-count difference left here. It would still be a
test of representation; connecting the retained organization to valuation is
a separate unresolved research question. P001 stops at its stated diagnostic.
