# Formal audit, part 6: quantum frames — r1

**Date:** 17 October 2026.
**Origin:** rulings 29 and 33; Sol's proposals of 16–17 October; the record
criterion settled on 17 October.
**Applied in:** Appendix A r10, section A.14.
**Checks:** `analysis/formal_audit/verify_appendix_a_part5.py`, V29–V38, all
pass.

## What changed

| Before (r9) | After (r10) |
|---|---|
| A.14.1 as an obstruction; A.14.2 frame-relative law; A.14.3 spacelike records | A conditional construction in ten numbered items. A state alone does not fix a continuation structure (A.14.1). A resolved frame's couplings fix its records (A.14.2), quantum theory gives their law (A.14.3), and lushness counts it. |
| — | The classical limit (A.14.4), coarse-graining (A.14.5), comparison before the branch (A.14.6), when two frames have no common history (A.14.7), continuation-equivalent presents (A.14.9), and resolved quantum comparisons with a remainder bound (A.14.10). |
| Haag (1996) for spacelike commutation | Fewster and Verch (2020) as the primary source (A.14.8). |

**Counts.** 76 numbered results: 15 established elsewhere, 43 proved here, 2
conditional on physical premises, 1 analytical model and 15 definitions. V38
confirms one status per result.

## Settled in this round

- **The record criterion.** A record is an instrument outcome retained at the
  declared resolution over the horizon. It need not change later
  probabilities. A correlation undone within the horizon is not a record.
- **Continuation equivalence** merges presents, never recorded histories (Sol's
  correction). V33: a recorded branch with identical futures keeps a constant
  offset of 2 bits: one for the record, one for the coherence the record
  destroyed.
- **Certification needs a bound.** Sign persistence certifies nothing. V37 and
  the small environment of V29 both show records forming and being undone.

## Checks

| Check | Result |
|---|---|
| V29 pointer selection | Z coherence falls to 0 by t = 0.8; no X coherence appears; 1 bit of record information in one environment qubit |
| V30 basis rotation | coherence in the coupling basis is 0 at every angle |
| V31 normalization | total probability 1 |
| V32 classical limit | agreement to 10⁻¹⁰ bits at horizons 1, 3, 5 |
| V33 recorded branch | constant offset at horizons 1, 3, 6; future laws equal |
| V34 latent phase | identical early records; later records (1, 0), (½, ½), (0, 1) |
| V35 inaccessible sector | change in lushness exactly 0 |
| V36 Wigner protocol | friend (½, ½), reversal option (1, 0): no common law; options compare as 2 bits and 0 bits |
| V37 recurrence | record forms and is undone every π/2 |

## Open, as stated in A.15

- Which frames are physically instantiated (the lattice frame program).
- Covariance across quantum reference frames.
