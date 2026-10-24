# Formal audit, part 2: Appendix A sections A.6–A.14 — r1

**Date:** 16 October 2026.
**Requested by:** Sol, in the review of Appendix A r2.

**What was checked, for every result:**
- assumptions;
- exact statement;
- derivation or source;
- scope;
- domain and units;
- status.

**Results covered:**
- A.6–A.14;
- A.2.5, which was added in r2;
- the A.5.1 error that Sol found.

**Outcome.**
- Applied in Appendix A r3 (A_FORMAL_CORE_r3):
  - one mathematical error corrected, which Sol found;
  - eight fixes to scope, domain or wording: four from Sol and four found by
    this audit;
  - two results relabelled, both from Sol.
- The audit also sharpened one of Sol's corrections (finding 2).
- No result was withdrawn.

**Verification:** `analysis/formal_audit/verify_appendix_a_part2.py`, results in
`verify_appendix_a_part2_results.json`. Checks V10–V17, plus two new checks,
V10b and V11b. All pass.

## Findings and changes in r3

| # | Result | Finding | Found by | Change in r3 |
|---|---|---|---|---|
| 1 | A.5.1 (gambles) | The proof's equality cases were reversed. Upper-bound equality holds when the history determines the outcome; lower-bound equality holds under independence. The statement and the In words line were right. | Sol | Proof corrected |
| 2 | A.7.1 (subject) | "Larger" is wrong. Sol proposed "no smaller". The audit found that "no smaller" holds only on average over the full presents compatible with the subject's present. For a particular full present the quantity can be larger or smaller (V11b: 3.50 bits, against 2.58, 3.62 and 3.34). | Sol; refined by the audit | Restated with the average, and the counterexample cited |
| 3 | A.10.2 (division) | With r_i > 0, the convex maximum lies at an extreme point outside the domain. | Sol | Domain changed to r_i ≥ 0 with f ≥ 1. A supremum clause added for returns undefined at zero |
| 4 | A.12.2 (removal) | q/(q + ε) needs exact hazard semantics. | Sol | Defined as mutually exclusive per-step events, or as competing exponential clocks. The case of independent per-step chances is explicitly excluded |
| 5 | A.6.3 (temporal expansion) | F contains log Q, which depends on the unit of time. | Sol | One declared unit for τ, T and Q. The units paragraph shows ℓ_T(τ) is invariant (V10b) |
| 6 | A.6.4 (crossover resolution) | Follows from 5: is τ× unit-dependent? | Audit | No. It names the same physical cadence in every unit. Stated |
| 7 | A.6.3 | The step count T/τ must be a whole number. | Audit | Stated |
| 8 | A.8.2 and A.8.4 (registers) | "Cannot act" must include costs. A register whose upkeep draws on resources the world uses acts on the world through its cost, and the proposition then fails. This matters for the test bed, whose registers are paid. | Audit | Scope added to both; A.8.4 now also requires the same world kernel and present |
| 9 | A.7.4 (resolved rankings) | Depth k is undefined at early steps (t < k). | Audit | Take k = t there, where the bounds are exact |
| 10 | A.9.2 (strict protection) | The valuing premise does the normative work, so "proved here" overstates it. | Sol | Retitled "given the valuing premise". The premise is named in the statement. A new status row is added, and A.15 lists the premise |
| 11 | A.13.4 (deference) | The payoffs are stipulated, so it is not a theorem of the measure. | Sol | Retitled as a decision model. A new status row is added, and prose must report it as a property of the model |

## Result-by-result record

Status codes:
- **E**: established elsewhere, proved or outlined here;
- **P**: proved here;
- **CP**: conditional on physical premises;
- **CN**: conditional on a normative premise;
- **SM**: analytical model with stipulated payoffs;
- **D**: definition.

| Result | Status | Derivation or source | Domain and units | Verdict |
|---|---|---|---|---|
| A.2.5 control invariance | P | ℓ is a functional of the history law | none | sound; nearly empty, used negatively |
| A.6.1 declared resolution | D | — | cadence and generator in one unit (finding 5) | sound |
| A.6.2 coarser grain | P | the entropy of a function is at most the entropy of its argument | equality iff the map is invertible on the support | sound; the ranking-reversal example checked by hand |
| A.6.3 temporal expansion | E | Gaspard and Wang (1993, section 3.3); outline checked step by step, including the O(τ² log 1/τ) terms from two-jump paths | findings 5 and 7 | sound after r3 |
| A.6.4 crossover resolution | P | subtraction of the expansions | finding 6 | sound |
| A.6.5 admissible resolutions | D | follows the program's resolution corridor | the band can be empty; nothing in the definition prevents that | sound |
| A.7.1 subject | D | — | finding 2 | corrected |
| A.7.2 whole and parts | P | chain rule; entropy of a function | — | sound |
| A.7.3 subject bounds | E | Cover and Thomas (2006, section 4.5); the lower-bound step uses the Markov property given X_{t−k}, re-derived | exact at k = t, given the fixed present | sound (V11) |
| A.7.4 resolved rankings | D | — | finding 9 | amended |
| A.7.5 subjects disagree | P | explicit example | — | sound; the example is trivial by design |
| A.8.1 register decomposition | P | chain rule in the order Y, then S | — | sound |
| A.8.2 register that cannot act | P | Y's law is fixed by K_Y; maximum entropy at m values | finding 8 | sound with the cost scope (V12) |
| A.8.3 factorial identity | P | definitions | — | sound; empty by design |
| A.8.4 information through action | P | A.8.2 applied to both arms without actuation | finding 8; same K_Y and present | sound with the added conditions |
| A.9.1 recovery | D | the largest closed subset exists because a union of closed sets is closed | can be empty | sound |
| A.9.2 strict protection | CN | dominance under the valuing premise | — | relabelled (finding 10) |
| A.9.3 precautionary protection | P | Theorem A.4.2 under dependence; first order in m | reverses if preservation lowers the rate | sound |
| A.9.4 option value | E | the value of information is non-negative (Jensen, pointwise); the irreversibility effect | the cost w is outside the inequality and stated separately | sound (V13) |
| A.10.1 coupling | E | mutual information is never negative | — | sound |
| A.10.2 division | E | Schur-concavity and convexity | finding 3 | corrected |
| A.10.3 concentration conditional | P | A.2.5 | — | sound |
| A.11.1 matched reference | P | A.3.3 averaged; h constant when K is irreducible | the limit needs aperiodicity | sound (V17) |
| A.11.2 matched transients | P | chain rule and Markov property | the total-variation remark uses ℓ_n ≥ 0 | sound |
| A.12.1 unresolved remainder | P | (i) total-variation bound, 2‖g‖ per side, so 4C in total, re-derived; (ii) A.3.3 | (i) needs a common g after τ | sound |
| A.12.2 removal | P | long-run rates by A.3.4 | finding 4 | sound after r3 (V14) |
| A.13.1 decision recursion | E | induction; Bellman (1957) | deterministic policies; randomized ones by A.13.2 | sound |
| A.13.2 recorded mixtures | P | A.5.2; concavity in q | the choice must be recorded | sound (V16) |
| A.13.3 requisite variety | E | Ashby (1956); thin-model step re-derived | injectivity is necessary | sound |
| A.13.4 deference | SM | algebra in a stipulated model | — | relabelled (finding 11; V15) |
| A.13.5 plan revision | P | transitivity and irreflexivity | fixed evaluation | sound |
| A.13.6 when rate can choose | P | immediate | the example's best options were found by exact search over a finite list | sound |
| A.14.1 quantum families | P | single-time families are trivially decoherent | — | sound |

## Notes for drafting the chapters

- **Chapter 11.** The test bed's registers are paid, so A.8.2 and A.8.4 do not
  apply to them directly. The chapter must use the model results for paid
  registers, and cite A.8.4 only for the idealized case.
- **Chapter 15.** A.6.4 makes the activity objection formally explicit. The
  chapter should say so, and should not treat the cadence corridor as a
  defence of the measure. The corridor is a discipline on claims.
- **Chapters 7 and 22.** Use A.7.1's averaged statement whenever the
  subject's own view is discussed.
- **Chapters 17 and 27.** State strict protection as "given the valuing
  premise". Report deference as a property of the decision model.

## Erratum to part 1

FORMAL_AUDIT_NEW_RESULTS_r1 passed A.5.1 without catching the reversed equality
cases in its proof. The fix is finding 1 above.
