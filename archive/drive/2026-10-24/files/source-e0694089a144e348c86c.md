# Formal audit, part 5: frames, correspondence, profile, quantum — r1

**Date:** 16 October 2026.
**Origin:** the discussion of 16 October that followed Sol's review of r7
(rulings 28–32), and Sol's list of compressions.
**Applied in:** Appendix A r9.
**Checks:** `analysis/formal_audit/verify_appendix_a_part4.py`, V25–V28, all
pass.

## What changed

| Before (r8) | After (r9) | Source |
|---|---|---|
| Valuer ⊆ subject, with [P4] open | Definition A.7.1: projection, valuer and whole field. A valuer is anything that physically instantiates a frame relative to which its possible continuations are defined. The whole field is the ultimate frame and counts. Summaries of the field are projections, not valuers. [P4] closed. The instantiation criterion is open. | rulings 10, 28 |
| "The ethical comparison" (Definition A.7.8) | "The unindexed comparison", with no ethical vocabulary. That ethical judgement tracks it, and prudence the indexed comparison, is part of the central thesis. | ruling 32 |
| Two foundational commitments: the premise, and the definition | The link (value requires valuers: no valuer, no value relation) and the central thesis (a correspondence, proved class by class). | ruling 32 |
| "Adopted": comparison by total lushness over expected persistence | Nothing adopted. Corollary A.3.9 makes the profile primary. Rate-then-offset is its limit, and the expected-persistence comparison is a reading of it (Lemma A.4.1, Proposition A.4.8). | Sol, compression 1 |
| A.14: an obstruction | A conditional construction. A.14.2: a frame's recorded histories have an ordinary law. A.14.3: records at spacelike separation do not depend on the slicing. Edge: assembly fails in extended Wigner's-friend scenarios. | ruling 29; Sol |
| Precaution, option value, deference as separate results | One decision structure, with the uncertainty placed in different spots (section A.9). A.13.3 gains computed payoffs b and b_c from A.4.9. | ruling 30; Sol |
| Recorded mixtures, a separate proposition (r8 A.13.2) | Part (b) of Corollary A.5.2. A.13.3–A.13.6 become A.13.2–A.13.5. | Sol, compression 8 |

**Counts.** r8 had 67 results. r9 merges 1 away and adds 3 (A.3.9, A.14.2,
A.14.3), for 69 in all: 15 established elsewhere, 40 proved here, 2
conditional on physical premises, 1 analytical model and 11 definitions. No
result is adopted, and none rests on a normative premise. V28 confirms one
status per result.

## Checks

| Result | Status | Check | Verdict |
|---|---|---|---|
| A.3.9 profile and verdict | proved here | V25: identity to 10⁻¹¹; sign follows the rate gap; equal final rates converge | sound. It is Theorem A.3.3 restated, but it removes the adopted row. |
| A.5.2(b) recorded mixtures | proved here (merged) | V16 | unchanged |
| A.14.2 frame-relative quantum lushness | established elsewhere | V26: total probability 1; the qubit of A.14.1 gives breadth 1 and 2 | sound, conditional on a fixed record structure |
| A.14.3 records at spacelike separation | established elsewhere | V27: order difference 3 × 10⁻¹⁷ | sound |

## Where the commitments moved

| Commitment | Where it lives now | Status |
|---|---|---|
| Value requires valuers | the link, outside the formal core; chapter 16 | link from the physical to the moral; not a moral premise |
| What makes a frame physically instantiated | A.15; one question for valuers, quantum records and admissible grains | open, with a candidate and the lattice program |
| That ethical judgement tracks the unindexed comparison | central thesis; chapters 16 and 22 | thesis, tested |
| Goods ↔ expansion, harms ↔ contraction | central thesis; chapter 20 | correspondence, proved class by class |
| Comparison horizon | Corollary A.3.9; the definition of Omega | no longer adopted |
| Quantum whole field in extended Wigner's-friend regimes | A.14.3 remarks; A.15 | open |

## Points for the manuscript

- **Prologue r11.** Value requires valuers is the link. The thesis is stated
  as a correspondence. Definition 3 and the ultimate frame are included. The
  Alpha chain runs from orientation to frame to continuation to lushness.
- **Chapter 5** teaches the profile.
- **Chapters 16 and 24** carry the instantiation criterion and the lattice
  program.
- **Chapter 4 or 30** carries the quantum frame construction.
- **Part VI** presents precaution, option value, deference and correction as
  applications of one structure.
- **Prose rule (ruling 31).** Goods, harms and the structures that enable them
  are dynamics of the continuation structure. No sentence should give
  organization, protection or cooperation a value of its own.
