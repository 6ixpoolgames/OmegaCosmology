# Foreclosure and probability suppression at a declared resolution

25 October 2026. Proposal for Sol/Opus review, prompted by the S3 discussion.
This does not amend imported Appendix A or redefine lushness. The checked
reference is [Appendix A r19](../../sources/v4.1/A_FORMAL_CORE_r19.md), A.9.3;
later manuscript revisions have not been checked here.

## 1. Required comparison data

Fix the sufficient present/conditioning, continuation window, and an explicit
history observation map for each arm into one common measurable history space.
For the finite backend, use sampled words Y1,...,Yn, excluding the already
conditioned initial symbol. Include the initial symbol only in a separately
declared query. Native event histories and sampled-state histories are different
observations; their supports need not have the same relation.

Let a be the assessed continuation law and b the reference. Preparations,
mechanism contrasts and implemented options remain distinct. Common labels
require a physical mapping, not merely renaming unrelated states to align arrays.
The history space must include physical termination/debris symbols if present.
An empty word is an outcome for a zero-length window, not an empty probability
law for an ended subject.

## 2. Exact finite foreclosure: preserve A.9.3

For the declared resolution r and window n:

`Theta_{r,n}(a:b) = {w : P_b(w)>0 and P_a(w)=0}`

`F_{r,n}(a:b) = P_b(Theta_{r,n}(a:b))`.

The first quantity is a set of histories, the second its reference weight.
Report the direction: F(a:b) generally differs from F(b:a). Neither is an
entropy difference, a stock loss, a closure probability or a new objective.

Support comes from structural transitions and admissible roots, with exact
zero semantics. Exponential underflow, Monte Carlo non-observation, a cutoff
and a probability rounded to zero do not prove impossibility.

At a positive sampling cadence, a finite CTMC's structural transition support
is the reflexive transitive closure of its directed jump graph. If both arms
have full support over the same state alphabet, every finite sampled word is
possible in both, so F=0. This includes different roots in one irreducible class
when X0 is conditioned out. Their entropy and first-passage profiles can still
differ substantially. Event-mark observations can differ even in this case;
they require their own physical resolution and cannot be silently substituted.

For a common deterministic coarsening c of both history observations, exact
foreclosure weight cannot increase: a coarse event absent under a pulls back
to an absent fine event. Thus coarsening does not turn a rare nonzero event
into an impossible event. Declaring a grain alone does not solve the manuscript's
open problem about practically lost but not strictly impossible futures.

## 3. A separate operational probability-suppression profile

Propose the diagnostic curve

`S_{r,n}(epsilon; a:b) = sup E_b[t(w)] subject to 0<=t<=1 and E_a[t(w)]<=epsilon`,

for 0<=epsilon<=1. It asks how much reference continuation mass can lie in a
testable history class that is rare under a. Fractional t describes a statistical
test/weight; it is an analysis object, not a new physical random register.

In a finite model this is a linear programme. Sort histories by decreasing
P_b(w)/P_a(w), treating P_a=0<P_b first, and fill the P_a budget, with at most
one fractional boundary. To verify optimality, move budget from a lower-ratio
history to a higher-ratio one; reference mass cannot decrease. Repeat until
the sorted allocation is reached. No independence between history stages is
assumed.

Properties, conditional on these common finite word laws:

- S(0;a:b)=F(a:b), recovering the exact reference-weight foreclosure.
- S is monotone and concave in epsilon; S(1;a:b)=1.
- Identical laws give S(epsilon)=epsilon. Its positive diagonal is the test
  budget, not evidence of harm or lost access.
- Common deterministic coarsening cannot increase S: every coarse test pulls
  back to an admissible fine test with the same two expectations.
- Swapping a and b produces a different curve. Report both when interpretation
  depends on the direction of suppression.

For finite words, the first property follows directly: a test with zero a mass
can be positive only on zero-a histories. Concavity follows by mixing feasible
tests at two budgets. The other statements follow from normalization and
pullback. These are elementary finite-law results for the proposed diagnostic,
not a theorem that a particular physical grain is faithful.

Call this **probability suppression**, not exact foreclosure. The entire curve
or a declared budget range should be reported. Epsilon is not fitted to make
an arm look harmful, and is not a physical resolution cutoff by itself. A claim
that some suppression is practically irreversible needs an external physical
argument about windows, observations, intervention costs and recovery. Nothing
here authorizes deleting its rare histories from lushness.

This gives a precise candidate handle on the open issue, rather than pretending
to settle a universal physical definition. It does not select an ethical threshold.
It also does not extend to incompatible quantum history families without a
common probability law.

## 4. Closure and recovery: report independent queries

Choose a functional target set G separately from the history observation.
Finite-model structural closure means reaching a state from which G is
unreachable in the native directed graph. Closure is not inferred from a
deadline with no recovery. Report:

1. Probability of structural closure by the deadline, where defined.
2. Unconditional probability and first-passage distribution of recovery by T.
3. Functional occupancy at T and integrated uptime; ever recovery is different.
4. Exact history foreclosure F, or an explicit unsupported status.
5. Probability-suppression S, when computationally supported.
6. The full entropy difference, retaining every represented random contribution.

A reversible trap can have enormous practical recovery time and zero closure
risk under this graph definition. An irreversible sink may change the answer,
but it is a declared physical boundary/idealization, not a numerical threshold.

## 5. Implementation sequence and evidence guarantees

The code already contains exact-word `foreclosure` and full-state structural
support dynamic programming in history.py, plus conformance examples of
contraction without foreclosure and foreclosure without contraction. The gap is
study integration and general projected histories, not absence of all machinery.

First expose a typed result with comparison direction, observation, conditioning,
window, support provenance, weight interval and applicability status. Full-state
DP requires a common state alphabet. For hidden projections, recognize possible
observation words using candidate reachable-state subsets; reference weights
must still propagate the reference hidden law. Do not replace a projected
process by a Markov chain. Cap subset/word growth and return unsupported when
necessary.

Start S on short exactly enumerated word laws; report unsupported at larger
windows. A sorted finite-word LP is not an efficient long-history algorithm.
Future likelihood/automaton algorithms need independent exact references and
error bounds. Structural absence may be exact while its reference weight is
evaluated numerically: the result must say which guarantee applies to each.

Reference cases: equal support/unequal entropy; support loss/entropy gain;
same endpoints/different admissible words; CTMC underflow without structural
loss; projected memory; refinement pullback; tiny positive reverse probability;
identical-law diagonal; empty window; different physical state alphabets.

No code implementation or scientific run is performed by this proposal.
