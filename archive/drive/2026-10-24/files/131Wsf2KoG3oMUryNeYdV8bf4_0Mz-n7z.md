# Formal audit, part 4: the subject, persistence and harm — r2

**Date:** 16 October 2026.
**Origin:** Sol's proposals of 16 October:
- "whole-field uniqueness" (the subject without impartiality);
- persistence as a realization condition;
- harm as counterfactual contraction.

The originator's statements are ruling 25. The foundation was adopted in
ruling 26.
**Applied in:** Appendix A r7. Sol's review of r7 is applied in r8 (addendum
below).
**Checks:** `analysis/formal_audit/verify_appendix_a_part3.py`, V18–V24, all
pass.

## What changed

| Before (r6) | After (r7) |
|---|---|
| The whole field as the ethical subject was a named premise, [P3]. | It is derived: Definition A.7.8 (the ethical comparison takes no index) with Corollary A.7.9. The step that excludes a subject is the sufficiency step that derives the measure. |
| "Valuer" was a working definition, [P4]. | A valuer is any subject (Definition A.7.1), as ruling 10 says. |
| Strict protection rested on the valuing premise (r6 A.9.2). | Retired. Proposition A.9.4: within the measure the bottom of the ranking is total foreclosure. This is a fact about entropy, not a premise. |
| Harm had no formal definition. | Definition A.9.2: contraction and expansion, descriptive. Harm and benefit are the evaluative terms, and the central thesis links them. Definition A.9.3: foreclosure, kept separate. |
| Persistence had only the persistence-setting results. | Corollary A.4.7 covers the regime's accrual. Proposition A.4.8 gives its worth to the whole field. Proposition A.4.9 gives the cost of an early end, with regeneration. |
| Orientation was not mentioned. | A.1 states that every result presupposes the order of steps. Irreversibility enters as γ = 0 in A.4.9. |

**Counts.** r6 had 57 results. r7 retires 1 and adds 11, for 67 in all: 13
established elsewhere, 40 proved here, 2 conditional on physical premises, 1
analytical model and 11 definitions. No result is now conditional on a
normative premise. V24 checks that every numbered result has exactly one
status.

## Checks of Sol's proposals

**1. Whole-field uniqueness.** Sound, once condition 4 carries the weight.
- **The mathematics** is the entropy of a function: H(f(Y)) ≤ H(Y), with
  equality if and only if f is injective on the support (Proposition A.7.7).
- **Condition 3 is not needed.** Sol's condition 3 ("no privileged
  decomposition") follows once condition 4 ("no merging of resolved
  histories") holds.
- **Condition 4 is sufficiency** (Definition A.1.1; Theorem A.2.3,
  condition 1), applied a second time.
- **What remains is a definition** (A.7.8), not a normative premise. The
  question of why to ask it moves to chapter 16 (section A.15).
- **Sol's isolated-civilization worry** is answered by reach, not by
  dependence (Proposition A.7.10). A region the options can affect is in the
  field. A region they cannot affect, and that is independent of what they do
  affect, cancels.

**2. Persistence.** Sol's monotonicity result is correct, but narrower than its
reading.
- **The result.** Corollary A.4.7(a) is his result. It is also a one-line
  consequence of Lemma A.4.1, and it holds for any process, since ℓ_n never
  decreases in n.
- **The extension.** Part (b) adds hazards that depend on the state, shown by
  the monotonicity of non-negative matrix products.
- **The correction.** The result concerns the regime's own accrual. At the
  whole-field level the field continues after the regime ends. One more unit
  of expected persistence is worth h − h′ + O(1/m) (Proposition A.4.8): the
  regime's rate less that of its successor.
  - V19 shows the worth approaching the rate difference as m grows.
  - When the successor branches more, longer persistence lowers whole-field
    lushness. This is Sol's sterile-churn case.

**3. Harm as contraction.** Viable.
- **The bottom of the ranking** follows from the non-negativity of entropy
  (A.9.4). That is why r6 A.9.2 and its premise can be retired.
- **Dependency.** "Value requires valuers" alone does not exclude a negative
  total: a suffering valuer is still a valuer. What excludes one is the thin
  definition of valuing (ruling 10), under which disvalue is a registered
  contraction. This is noted in A.9.4 and assigned to chapter 16.
- **Foreclosure by support** is exact only for finite models. It is listed as
  open in A.15.
- **The two examples in A.9.3** show that foreclosure and contraction are
  independent.

**4. The sign of harm and Alpha.** Orientation is not needed for the sign: any
counterfactual comparison has one. Orientation supplies two things:
- **the downstream direction** that lushness counts (A.1);
- **irreversibility.** This is the regime-level case γ = 0, which makes the
  cost of an early end largest (A.4.9).

The relation of γ to Alpha's directional asymmetry is argued in chapter 30
and listed in A.15 as not proved.

## New results: verdicts

| Result | Status | Check | Verdict |
|---|---|---|---|
| A.4.7 persistence and accrual | proved here | V18: identity to 10⁻¹³; no counterexample in 400 cases | sound |
| A.4.8 worth of persistence | proved here | V19: limit to 1.1 × 10⁻⁹ bits; derivative to 10⁻¹⁰ | sound; holds in Cesàro mean for periodic common laws |
| A.4.9 cost of an early end | proved here | V20: six cases, including γ = 0 and λ + γ = 2 | sound, under homogeneous blocks; the block-average version is not bounded |
| A.7.6 self–whole gap | proved here | V21: residual 0 | sound; C5 arithmetic gives a rest-given-dominator term in [−27.696, −18.486] bits |
| A.7.7 subjects that lose nothing | established elsewhere | V21: equal when injective on the support, lower when lossy | sound |
| A.7.8 the ethical comparison | definition | — | — |
| A.7.9 subject of the ethical comparison | proved here | — | sound, given A.7.8 and A.2.3 |
| A.7.10 reach | proved here | V22 | sound; independence is required and stated |
| A.9.2 contraction and expansion | definition | — | — |
| A.9.3 foreclosure | definition | V23: both examples | — |
| A.9.4 largest contraction | proved here | V23: no violation in 2,000 cases; equality at a point mass | sound |

## Where the commitments moved

| Commitment | Where it lives now | Status |
|---|---|---|
| Ethics asks the question with no index | Definition A.7.8; argued in chapter 16 | definition |
| The whole field as the subject | Corollary A.7.9 | follows from Definition A.7.8; no impartiality premise |
| Persistence of valuing is prior to every value | chapter 16, from value requires valuers | argued, not a theorem (A.15) |
| What persistence is worth | Proposition A.4.8 | derived |
| No absolute negative value | thin definition of valuing; A.9.4 remark; chapter 16 | follows from the definition |
| Whole-field contraction is harm | central thesis (chapter 20) | thesis |
| Every ethically salient material injury appears as contraction | central thesis (chapters 18 and 22) | thesis; exposed by the funded-extraction arm |
| Foreclosure in physical laws | A.15 | open |
| γ and directional asymmetry | chapter 30; A.15 | conjecture |

## Points for the manuscript

- **The prologue** states one premise, one definition and one thesis. The
  self–whole gap is its headline for the ethical standpoint.
- **Chapter 7** carries A.7.6 and A.7.7. **Chapter 16** carries A.7.8, A.7.9,
  the priority of valuing, the thin definition and the why-be-ethical
  argument. **Chapter 18** carries A.9.2–A.9.4 and A.4.9. **Chapter 30**
  carries orientation and γ.
- **The outline** needs these moves in chapters 16, 17, 18 and 30. They are
  not yet made, pending the originator.
- **Every adversarial report** states foreclosure and contraction separately
  (A.9.3).

## Addendum (r2): Sol's review of r7, applied in r8

Sol rated r7 the strongest Appendix A so far and asked for five targeted
corrections plus one to the status paragraph. No result changes.

| Point | Verdict | Applied in r8 |
|---|---|---|
| 1. The subject is derived from the definition, but the definition is not derived | Agreed. r7 already said so in A.15, but the drafting note and prologue said "derived". | A.7.9 remark "what is and is not derived"; status paragraph; prologue r10 presents the definition as the second commitment, argued in chapter 16. |
| 2. "A valuer is any subject" is too broad | Agreed that valuers ⊆ subjects. One qualification on Sol's proposed criterion: "continuation law depends nontrivially on distinctions" does not exclude a parity bit either, since any non-constant projection of a branching dynamics has a continuation that depends on differences. The work is done by "physically instantiated process", and that is the open criterion. | A.7.1 marks [P4]: valuers are physically instantiated processes; every physical process qualifies, gas included; arbitrary projections need not. No numbered result depends on where the line falls. Pending the originator, since ruling 10 bears on it. |
| 3. A.9.4 conflates maximal contraction with total foreclosure | Agreed. | Statement in words and remarks corrected, with Sol's counterexample. |
| 4. A.4.9 needs the sign of s_R − s_S | Agreed. | Statement in words and remark on γ = 0 qualified by sign. |
| 5. A.7.10's slogan exceeds its hypothesis | Agreed. | Renamed "unaffected parts cancel"; statement narrowed; causal reach in the scope. |
| 6. Status paragraph | Agreed. | It now names the two commitments outside the formal core, and the central thesis. |
| The measure derivation's bound | Agreed; already kept. | Prologue r10: "nothing else enters the count". |

V24 rerun on r8: 67 results, one status each.
