# Formal source check for the next-generation platform

> Repository adaptation, 24 October 2026: selected for the v4.1-based `omega-cosmology` preparation. Package paths and imported-reference links are adapted; the unchanged source is in `archive/legacy-testbed/`. Design readiness does not claim engine implementation.


24 October 2026. Read-only source inspection; no Drive edits or scientific runs.

## Sources actually retrieved

- [A_FORMAL_CORE_r19.md](https://drive.google.com/file/d/1lIoQFGDdz20u8lDhEqxcZl7Xyf4h2C3F/view?usp=drivesdk),
  drafting note dated 23 October, about203k characters of readable source.
- [FOUNDATIONS_r4.md](https://drive.google.com/file/d/1niTNRFvxLNUVji0kpOS7shriYKFp-4wa/view?usp=drivesdk),
  dated 23 October, current frame/present wording.

Exact search for A_FORMAL_CORE_r20 found no result. A broader FORMAL_CORE search
and a metadata name search also returned r19 as the newest identified file.
This establishes only what was discoverable through the connected Drive; r20
may exist elsewhere or not yet have been uploaded. Opus's r20 review remains
useful supplied context, not independently verified r20 text.

The r19 frame/valuer prose predates the foundations-r4 correction. Use the
verified foundations wording for the platform's frame contract; do not restore
older wording merely because it appears in r19.

## Verified definitions and implementation consequences

### Resolution: A.6.5 and A.6.6

Certification means a ranking survives a specified refinement because the bound
on additional conditional entropy cannot reverse it. Faithfulness is not
required for this mathematical bound. Its scope is the named refinement only.

A faithful reversing refinement corrects the coarse ranking. An unverified
refinement that reverses it yields a resolution-dependent reversal. Governing
status can remain provisional even after certification against one refinement.

Implement separate certification, faithfulness, reversal and governing-status
fields. A single mutually exclusive four-label enum would lose information.
Store the actual inequality and uncertainty bounds used in each certificate.

### Exterior: A.7.10 and A.7.11

The exterior must have the same history law under implemented options. Finite
affected entropy and nested finite-entropy exterior descriptions exhausting the
same exterior information complete the latter proposition's premises.

The comparison retains the difference in mutual information with the exterior.
Matched reservoir settings alone neither prove an unchanged exterior nor remove
its changing correlations. This is a finite-horizon statement; a joint spatial
and temporal limit is not supplied by it.

### Foreclosure: A.9.3 and A.9.4

Foreclosure is a difference in resolved HISTORY supports, with its weight under
the reference law. It is not endpoint reachability, a probability decrease,
stock loss or a finite recovery failure. Contraction is a difference in history
entropy and is independent of foreclosure.

The source gives valid examples:

- probabilities (.5,.5) changed to (.9,.1): contraction without foreclosure;
- support {1,2} with uniform probabilities changed to {2,3,4} uniformly:
  foreclosure of history1 with reference weight .5, but greater entropy;
- a point history chosen from a two-history reference: maximal contraction,
  but not total foreclosure because one reference history survives.

For sampled irreducible finite CTMCs on a common state alphabet, positive
sampled transition probabilities can make all finite history supports coincide.
Then exact foreclosure is zero even if rates differ enormously. A useful
finite-deadline access-risk query can coexist with that result, but must not
replace the formal support-based quantity.

### Comparison: foundations r4 section 7

Verified six requirements: one present; laws rather than selected histories;
matched resolution/conditioning; implemented options rather than postselection;
disclosed finite horizon; representation/section invariance required but open.

The reviewer names the gathered definition A.7.12. That ID does not occur as a
definition in r19. Implement from the verified foundations checklist and retain
the pending r20 ID mapping.

### Rates: A.3.9

The source calls the profile the object and describes its full-continuation
asymptotic reading as rate first, then offset under its finite-chain assumptions.
Finite-horizon signs are partial assessments. For periodic discrete chains the
offset limit may be Cesaro rather than ordinary; preserve that qualifier.
The new CTMC sampled kernels have self-return probabilities, but generic
reference cases must not silently assume every supplied discrete kernel is
aperiodic. A finite assessment is never replaced by this asymptotic result.

### Local conditioning: A.7.1

Part-history conditioned on the full present and part-history conditioned on
its own present are distinct. The latter requires the conditional distribution
over compatible full presents. Average inequalities do not determine the
ordering at every particular full present. The spec's separate quantity IDs
and explicit hidden-root law implement this distinction.

## Formal-reference mapping correction

The reviewer supplied A.11.1/A.11.2 for matched boundaries. In r19 these are:

- A.11.1: same-law irreducible preparation contrast, with rates cancelling;
- A.11.2: preparations whose state distributions coincide cease accumulating
  further history-entropy difference under the same law.

These belong in the preparation/transient suite. General boundary matching
belongs to the comparison contract; exterior cancellation to A.7.10/A.7.11.
Keep both tests and use the accurate source mapping rather than claiming one
theorem proves all forms of boundary matching.

Other supplied IDs were located at their expected headings in r19. This is a
targeted definition/conformance check, not a mathematical audit of all proofs.

## Readiness

Architecture r2 has been amended with the verified contracts. No unresolved r20
version question prevents building the local rule engine or exact backend.
Formal conformance must be labeled against the source version actually checked;
the r20 delta should be verified when available, before claiming r20 compliance.
