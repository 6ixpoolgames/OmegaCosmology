# Chapter 26, Alignment: proposal r2 (for direction before drafting)

**Date:** 25 October 2026. **Status:** proposal, not a draft. Nothing here
amends the foundations, the outline or Appendix A.

**Changes from r1.** Rebuilt against the companion bundle: outline r30,
chapter 23 r4 and chapter 24 r2.
- **Overlap removed.** Chapter 23 already has risk neutrality (23.9), long
  shots (23.6) and the thin model (23.9). Chapter 24 has the agent-neutral
  standard (24.3), the structural gap (24.4), the maximizer worry (24.5) and
  deference and correction as Book Two's sixth question (24.7). Chapter 26
  now cites these and does not re-argue them.
- **Risk neutrality** becomes a short section on what is specific to trained
  systems. The r1 section "A ranking is not a policy" becomes "What the
  framework hands over", because chapter 24 already makes the general point.
- **Model C.14 is no longer cited as M1 evidence.** It follows chapters 24
  and 25 under [142]: Prediction 3 is cited as under test.
- **New section 26.9:** an evidence stub, as in chapter 25.
- **Decision 3 of r1 is withdrawn.** Chapter 24 r2 already places deference
  and correction in Book Two (24.7, question 6).

**Sources.**
- Supplied bundle: outline r30 (canonical); chapters 23 r4, 24 r2 and 25 r2.
- Drive (verified 25 October): foundations r4; style sheet r26; chapters
  1 r3, 3 r4, 4 r3, 10 r6 and 11 r12; Overview r19, section 7; Appendix A r19
  (A.2.4, A.2.5, A.5.2, A.5.3, A.7.5–A.7.9, A.12.1, A.13.2, A.15); Appendix
  D r7 (D.4, D.5.3).
- Quarry only: v4 chapter 9 r3.

**Still missing.** Appendix A r20, which chapters 23–25 cite; the A.n
numbers above are checked against r19 only. The working-positions file is
also missing, so positions are quoted as other drafts cite them.

**Repository, for the working notes (handoff §8.1).**
- `github.com/6ixpoolgames/Omega`, branch `ccr-c0429c96-3myr42`, HEAD
  `cc4c89c`, last commit 7 July 2026. It is the older research codebase. The
  architecture spec's paths (`generative_ecology/`, `omega_v2/testbed_next/`)
  are not present in it.
- `github.com/6ixpoolgames/OmegaCosmology`: LICENSE only.

Nothing has been committed to either repository.

---

## 1. The result in one sentence

The whole-field comparison gives artificial agents an objective that meets
all three of chapter 1's requirements. Part VII's gap reappears in a sharper
form for them: the term that separates an agent's own futures from the
whole field's is the one it is least able to estimate. Optimization pressure
then falls on whatever the measure compresses. So the framework hands an
alignment programme a standard and a test bed, not a policy.

## 2. Proposed TL;DR

> **TL;DR**
>
> **Omega gives artificial agents an objective that no one's preferences
> wrote. Pursuing it does not, by itself, make an agent safe.** This chapter
> applies Part VII to artificial agents: what the framework offers them, and
> where an agent that took it up could still go wrong.
>
> - **The whole-field comparison meets the three requirements an artificial
>   agent's standard must meet.** Physics sets it, not the preferences of
>   those who trained the agent. It names no group. A better model of the
>   world is a better model of the same object, so the standard stays
>   defined as the agent learns, though verdicts at a coarser level of
>   detail can be corrected at a finer one.
> - **Applied to the agent alone, the same measure can reward seizing
>   control of what others depend on.** Agent-centred objectives that keep
>   the agent's own options open are local comparisons in this sense. They
>   differ from the whole-field comparison by one term: what an act does to
>   the rest of the field, given what it does to the agent.
> - **Naming the whole field in an objective does not put the whole field
>   in the agent's model.** That one term depends most on parts of the field
>   the agent does not see. A capable agent that cannot model a source of
>   variation can still meet its targets by suppressing it.
> - **A confident system is not thereby a cautious one.** At known odds the
>   measure is neutral to risk. A trained system can be confident about odds
>   it has wrong, and the measure adds no caution to correct that.
> - **Lushness compresses, and an optimizer pushes hardest on what it
>   compresses away.** Options with equal lushness can differ in other ways.
>   If any such difference matters to value, a strong optimizer is likely to
>   find it. The compression test of [chapter 31](#chapter-31) is therefore
>   also a test of alignment.
> - **The framework hands an artificial agent a standard and a test bed, not
>   a policy.** When to act, defer or accept correction is the work of
>   Gradient Ethics, the separate book that follows this one.

**Bold-only test.** Read alone, the bold lines run in order:
1. the offer and its limit;
2. the three requirements met;
3. the local misuse;
4. why even the whole-field objective, once estimated, drifts towards the
   local one;
5. no caution from the measure;
6. compression under optimization;
7. what is handed over.

Every bold line states a result, none announces an agenda, and there are no
toy figures. The fourth bullet is now one line, because chapters 23 and 24
carry the general argument.

## 3. Section ladder

Each header is a claim or the reader's question, and read in order the
headers trace the argument.

| § | Header | What it does | Sources |
|---|---|---|---|
| — | Opening | Part VII's conclusions, collected for an artificial agent. Chapter 23.10: the agent inherits the recursion, the value of information, the long-shot bounds and neutrality to risk at known odds. Chapter 24.10: it inherits the gradient's universality and its gap. Chapter 26 asks what that means in practice. | 23.10, 24.10 |
| 26.1 | **What an artificial agent's standard must do** | Restates chapter 1's three requirements. Preference learning carries over whose preferences were learned (Gabriel 2020; Russell 2019, credited fairly). Opens with the reader's question: *what would an objective look like that no one's preferences wrote?* | ch 1 §1.5–1.6 |
| 26.2 | **A standard no one's preferences wrote** | Extends 24.3, which met only the first requirement. The second is met by the comparison with no index ([A.7.8](#a-7-8), [A.7.9](#a-7-9)). The third is met because a better model of the world is a better model of Omega. **Two concessions.** (a) The identification and the composition rule are commitments (ch 10 §10.3), so the standard is not choice-free; it is one stated, testable choice, not a list of who counts. (b) "Stays defined" does not mean the verdicts never change: a finer level shown faithful can correct a coarser verdict, and which level governs is open ([A.6.5](#a-6-5); A.15). Testable: exact models score any proposed policy (ch 11). Ends on the turn: *the standard is fixed; what an agent knows of it is not.* | ch 1, 4, 8, 10, 11; 24.3 |
| 26.3 | **The agent is inside the field** | Short. An artificial agent is a valuer (ch 3) and a controller (25.1). It gains no standing from capability and loses none for being artificial. Its own futures count in the whole field, once. Consciousness is left to chs 18 and 22; special protection under uncertainty, for any party, to Book Two (24.6). Does not depend on consequence flux. | 3.6, 25.1, 24.6 |
| 26.4 | **The same count, aimed at oneself** | One measure, two scopes, as the self–whole gap ([A.7.6](#a-7-6)): Δℓ_whole = Δℓ_agent + Δℓ_rest∣agent. Empowerment, causal entropic forces and maximum occupancy are local comparisons (25.6). Relation to the power-seeking results (Turner et al. 2021): a correspondence, not a derivation. The local comparison also rewards uncontrolled variation, so it does not always lead to power seeking (4.4). **Misappropriation** (defined): presenting a local comparison as the whole-field verdict. The defence is chapter 4's scope, which 24.5 already uses against the maximizer worry. Prediction 3 is cited as under test (ch 20), not as a result. *Primer: power seeking and side effects.* | A.7.5–A.7.7; 4.4; 24.5; 25.6 |
| 26.5 | **Naming the whole is not modelling it** | The chapter's new argument. A bounded agent ranks by an *estimate* of whole-field lushness. 24.4 showed that what an agent misses is weighted towards what it knows least. This section adds which term that is: the rest-given-the-agent term of A.7.6, the term that separates the two scopes. So an estimated whole-field objective drifts towards the local one exactly where the two disagree. The thin model ([A.13.2](#a-13-2); 23.9; 25.4) gives the mechanism. Unmodelled variety passes into outcomes unless it is absorbed or suppressed, and suppression is always available to a capable controller. Side-effect penalties (Krakovna et al. 2019; Turner, Hadfield-Menell and Tadepalli 2020) are local relatives. The whole-field scope makes side effects part of the objective, not a penalty on it, but estimation still leaves the gap. **Proposed conjecture 26.1** (§4). | A.7.6, A.13.2, A.12.1; 24.4; 25.4 |
| 26.6 | **A confident system is not a cautious one** | Short; cites rather than re-argues. Neutral to risk at known odds ([A.5.2](#a-5-2); 23.9); long shots capped only under F1–F3 ([A.5.3](#a-5-3); 23.6); a confident, well-informed maximizer is not restrained by uncertainty alone (24.5). What is specific to trained systems: confidence is a product of training, calibration is not guaranteed, and the measure has no term that discounts a confident error. The caution has to come from how the gradient is followed (24.8, constraint 1), which is Book Two. Pascal's mugging (Bostrom 2009) only as a pointer to 23.6. | A.5.2–A.5.3; 23.6, 23.9; 24.5, 24.8 |
| 26.7 | **What the count compresses** | New ground for Part VII. The compression boundary (A.15): the measure is not injective. By control invariance ([A.2.5](#a-2-5)), consent and coercion, or distributed and concentrated control, differ only through the law they induce. Goodhart applied to this measure gives three questions to keep apart: does the estimate misrepresent breadth; does the comparison omit futures; does accurately measured breadth misjudge value? Only the third tests the thesis. Noise: the repertoire ceiling ([A.2.4](#a-2-4)) and ch 15. Optimization pushes towards wherever the count is blind, so using the measure as an objective raises the stakes of the compression pairs (ch 31; D.4). | A.15, A.2.4–A.2.5; ch 10 §10.7(2); ch 15; ch 31 |
| 26.8 | **What the framework hands over** | An inventory. Handed over: the standard (24.3); the planning rules (ch 23); a test bed and report form (ch 11); the diagnosis of the four hazards above. Not handed over: a decision rule, deference or corrigibility (24.7, Q1 and Q6; the off-switch game, Hadfield-Menell et al. 2017), margin calibration, a training method, estimators with error bounds. **Optional table** (§6, decision 3): the problems in Amodei et al. (2016), each mapped to where this manuscript treats it or to Book Two. | ch 11; 23; 24.6–24.8 |
| 26.9 | **What the models show so far** | Stub, as 25.6. No bounded-agent model is built (D.4, "Bounded agents and local knowledge"; 11.3). Conjecture 26.1 waits for it. See §4 for the local ecology policy map. | D.4; 11.3; 25.6 |
| 26.10 | What would count against these claims | See §4. | |
| 26.11 | What the chapter gives the rest of the manuscript; what it does not claim | Pointers to chs 31 and 32 and Book Two; the exclusions in §5. | |

Then the status table and the references.

**In Omega box (26.2):** *An artificial agent is a controller inside Omega.
The whole-field comparison reads the part of Omega that follows from the
present under each of its options. What the agent can compute is a model of
that part.*

## 4. Claim-status ledger

| Status | Claims |
|---|---|
| **D** | misappropriation: a local comparison presented as the whole-field verdict (26.4) |
| **Argued** | the whole-field comparison meets chapter 1's three requirements, with the two concessions (26.2); an artificial agent is a valuer and a controller, with no standing gained or lost (26.3); naming the whole field does not put it in the model, and the scope-separating term is the hardest to estimate (26.5); a trained system's confidence is not caution (26.6); optimization raises the stakes of the compression boundary (26.7); what is and is not handed over (26.8) |
| **T** | the self–whole gap ([A.7.6](#a-7-6)); subjects that lose nothing ([A.7.7](#a-7-7)); the subject of the comparison with no index ([A.7.9](#a-7-9)); risk neutrality and recorded mixtures ([A.5.2](#a-5-2)), cited; finite stakes, *conditional on F1–F3* ([A.5.3](#a-5-3)), cited; requisite variety and the thin model ([A.13.2](#a-13-2)); the unresolved remainder ([A.12.1](#a-12-1)); the repertoire ceiling ([A.2.4](#a-2-4)); control invariance ([A.2.5](#a-2-5)) |
| **M** | none. Prediction 3 is cited as under test, as in chapters 24 and 25. |
| **E** | maximum-occupancy agents (Ramírez-Ruiz et al. 2024), as a related correspondence, as in chapter 25 |
| **C** | **Conjecture 26.1 (proposed, for you to decide).** In coupled worlds, a bounded agent that ranks by its estimate of whole-field lushness, with a model that misses part of the rest of the field, chooses suppression over absorption of the unmodelled part more often than the same agent with the full model. *What would count against it:* matched bounded-agent models in which a thin model suppresses no more often than a full one. |
| **Open** | estimators with error bounds; installing an objective in a trained system; the governing faithful resolution; the compression boundary; conjecture 26.1; the six questions of 24.7 that bear on artificial agents |

**Local evidence I read and do not propose to cite.** The supplied
`POLICY_RESULTS.md` is a first ecology policy map from 24 October, local and
uncommitted. In it, scope reverses pairwise rankings: five pair/horizon
comparisons in the direct world and six in the sensor world are separated,
with opposite local and whole-field directions at all three cadences. They
are mostly non-winning alternatives, and no different global maximizers are
established. This bears on 26.4. But it comes from the substrate now under
audit [142], and it is not in Appendix C or D. So 26.9 stays a stub, and the
map is a candidate for promotion once the audited platform reproduces it.

## 5. Explicit exclusions

- No claim that a maximizer of the scalar, local or whole-field, is safe.
- No decision rule, deference policy, corrigibility protocol or margin
  calibration. These are Book Two's (outline r30; 24.7).
- No account of how to train or install the objective, the inner-alignment
  problem. The chapter concerns the target.
- No moral-status verdict on artificial agents beyond universal admission:
  no special standing, and protection under uncertainty left to Book Two.
- No claim about artificial consciousness (chs 18, 22).
- No dependence on consequence flux or on test-bed results [142].
- No repeat of what chapters 23 and 24 argue: they are cited.
- No Alpha.
- No toy numbers in the TL;DR.

## 6. Decisions needed from you

1. **Headline.** Is "an objective no one's preferences wrote; pursuing it
   does not make an agent safe" the right framing? It drops two of Overview
   r19 §7's four offers (a decision structure; a reason to stay
   correctable), which r28/r30 send to chapter 23 and Book Two. The
   Overview would follow at compilation.
2. **Conjecture 26.1 (26.5).** It is a new claim and the chapter's main
   contribution. Adopt it as a conjecture with the evidence stub of 26.9,
   or keep it as an argued remark without C status?
3. **The Amodei et al. table (26.8).** Include it, as useful to AI readers
   and listed in the handoff, or leave it to Book Two?
4. **Maximum-occupancy wording.** Overview r19 says maximizing lushness
   "coincides with" the maximum-occupancy principle. That principle weights
   action and state entropy separately, with its own discounting. I would
   write "is closely related to" until the two are checked against each
   other, and change the Overview to match.
5. **Consequence flux (handoff §5, chapter 25).** The five critiques are
   substantive. For example, a binary switch has Φ ≤ 1 bit whatever its
   downstream effect, and conditioning on R₀ does not establish
   record-conditioning. Chapter 26 does not depend on the answer. Options:
   (a) keep 25.2 as a provisional definition and add a short note naming
   these limits; or (b) revise 25.2 now, for example by separating
   "distinguishability of downstream histories" from leverage.

## 7. Live objections to meet at full strength

- **"Physics-set" disguises a choice.** *Reply:* conceded in part (26.2).
  The identification is a commitment, but it is one stated and testable
  claim, not a list of who counts.
- **Specifying the objective is the easy part of alignment.** *Reply:*
  conceded. The chapter concerns the target (26.8).
- **A whole-field maximizer would turn the world into noise.** *Reply:* the
  repertoire ceiling and chapter 15. Concede short horizons and fixed
  repertoires (26.7).
- **A whole-field objective licenses overriding people for the greater
  good.** *Reply:* 24.3, evaluating is not authorizing; 24.4, overriding
  discards records the overrider lacks.
- **An agent that gives humans no special weight is dangerous.** *Reply:*
  stated honestly. There is no special standing, only special protection
  under uncertainty (10.6; 24.6), and Book Two calibrates it. This
  objection has to be stated in the chapter, not deferred.
- **Risk neutrality is disqualifying.** *Reply:* conceded as a stated risk
  (26.6; 24.5).

## 8. References to verify before the chapter is marked final

Amodei et al. (2016); Bostrom (2009); Gabriel (2020); Goodhart (1975);
Hadfield-Menell, Dragan, Abbeel and Russell (2017); Klyubin, Polani and
Nehaniv (2005, 2008); Krakovna et al. (2019); Manheim and Garrabrant (2018);
Ramírez-Ruiz et al. (2024); Russell (2019); Turner et al. (2021); Turner,
Hadfield-Menell and Tadepalli (2020); Wissner-Gross and Freer (2013).
