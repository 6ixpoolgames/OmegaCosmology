# Formal audit, part 3: deriving the measure — r1

**Date:** 16 October 2026.
**Origin:** Sol's proposal of 16 October, "quotient first; count second".
**Applied in:** Appendix A r6.
- New Definition A.1.1 and Proposition A.1.2.
- Theorem A.2.3 restated.
- The "weight-only class: adopted" item removed.

## What changed

| Before (r5) | After (r6) |
|---|---|
| The measure's class, weight-only with grouping, was **adopted**. The prologue sample r7 justified the weight-only part by "impartiality applied to counting". | The measure is **derived**. Physics settles sameness at a declared resolution (Definition A.1.1). Four conditions on any effective count of resolved continuations then force perplexity (Theorem A.2.3). Impartiality plays no part in the derivation; its only job is to choose the whole field as the subject. |

## Check of the theorem

**The conditions.**

| Condition | Status | Relation to Faddeev's theorem |
|---|---|---|
| 1. Sufficiency (symmetry; null invariance) | Definitional (Proposition A.1.2) | gives symmetry |
| 2. Continuity of B(p, 1 − p) | Required by finite-precision measurement | the same condition |
| 3. Recursive composition | Required for consistent evaluation over time; used at every step of Theorem A.13.1 | implies grouping (a two-stage process that merges two outcomes and then splits them) |
| 4. Calibration B(uniform on k) = k | Definitional ("effective number") | k = 2 gives the normalization; the other values of k follow |

**The proof.** Faddeev (1956) proves that symmetry, continuity, grouping and
normalization force log₂ B = H. The converse holds: 2^H satisfies 1–4, and
condition 3 is the chain rule.
- **Null invariance** is also implied by Faddeev's conditions, since they
  force H(1, 0) = 0. Stating it separately does no harm.
- **Verdict:** sound.

**Status.** The theorem is established elsewhere (Faddeev 1956). What is new is
that each condition is now justified as definitional or as a requirement, not
adopted.

## Similarity weighting

- The argument rests on a dichotomy.
  - Either a similarity has physical consequences, and they appear in the
    continuation structure at an admissible resolution and horizon.
  - Or it has none, and weighting by it changes the question.
- It contains no theorem and needs none. It is a remark on why a similarity
  matrix lies outside the continuation structure.
- **Its scope is correctly limited** in the appendix. The first branch holds
  only if the resolution is fine enough and the horizon long enough for the
  consequences to appear.

## Where the commitment moved

| Commitment | Where it now lives | Status |
|---|---|---|
| The measure's class | Theorem A.2.3 | derived |
| Every consequential distinction appears at the declared resolution and horizon | Definition A.6.5; section A.4; Theorem A.2.3 remarks | a requirement on each comparison, checked by sign stability |
| What the measure compresses away does not matter | Section A.15 | part of the central thesis |
| Resolved histories in quantum theory | Section A.14 | open (choice of family) |

## Points for the manuscript

- **Remove "impartiality applied to counting"** wherever it appears. Prologue
  sample r7 is superseded by r8.
- **Chapter 4** carries the argument in full: the problem, the four
  conditions with their justifications, the theorem, and the similarity
  dichotomy.
- **Chapter 16** is the only place where impartiality is used: it is the move
  from a part of the field to the whole field.
- **Appendix A now has 57 numbered results.** One status each; the status
  table was checked by script.
