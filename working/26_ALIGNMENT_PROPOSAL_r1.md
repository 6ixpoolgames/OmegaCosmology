# Chapter 26, Alignment: proposal r1 (for direction before drafting)

**Date:** 25 October 2026. **Status:** proposal, not a draft. Nothing here
amends the foundations, the outline or Appendix A.

**Built from (verified on Drive, 25 October):** foundations r4; style sheet
r26; outline r28 (chapter 26 entry), with the r30 chapter-26 entry as
summarized in the handoff of 25 October (§3); chapters 1 r3, 3 r4, 4 r3,
10 r6; chapter 25 r2 (supplied); Overview r19 section 7; Appendix A r19
(A.2.4, A.2.5, A.5.2, A.5.3, A.7.5–A.7.9, A.9.5, A.12.1, A.13.1–A.13.3,
A.15); Appendix D r7 (D.3.6, D.4, D.5.3, D.6); v4 chapter 9 r3 (*Decision,
corrigibility and alignment*), as a quarry only.

**Not available to this instance:** outline r30 itself, chapters 23 r4 and
24 r2, the working-positions file, Appendix A r20 and the companion ZIP.
Where the chapter touches chapters 23–24 (correction, deference, option
value), the proposal points to them without stating their content. That
needs checking against chapter 24 r2 before drafting.

---

## 1. The result in one sentence

The whole-field comparison gives artificial agents an objective that meets
chapter 1's three requirements. The same structure shows three ways an
agent pursuing it can still go wrong: the scope collapses towards the
agent, the measure carries no caution, and the count compresses. The
measure repairs none of them, so a ranking is a standard to act against,
not a policy to act on.

## 2. Proposed TL;DR

> **TL;DR**
>
> **Omega gives artificial agents an objective that no one's preferences
> wrote. Pursuing it does not, by itself, make an agent safe.** This chapter
> says what the framework offers an artificial agent, and where an agent
> that took it up could still go wrong.
>
> - **The whole-field comparison meets the three requirements an artificial
>   agent's standard must meet.** Physics sets it, not the preferences of
>   those who trained the agent. It names no group. A better model of the
>   world is a better model of the same object, so the standard does not
>   change as the agent learns, though its verdicts can be corrected.
> - **Applied to the agent alone, the same measure can reward seizing
>   control of what others depend on.** Keeping one's own options open is a
>   familiar objective for artificial agents. It differs from the
>   whole-field comparison by one term: what an act does to the rest of the
>   field, given what it does to the agent.
> - **Naming the whole field in an objective does not put the whole field
>   in the agent's model.** An agent estimates that term from records it
>   holds, and it is least sure of exactly that term. A controller that
>   cannot model a source of variation can still meet its targets by
>   suppressing it.
> - **The measure is neutral to risk, so caution has to come from
>   elsewhere.** It values a gamble at the probability-weighted rate of its
>   outcomes. Under stated physical premises, long shots with capped gains
>   lose. Beyond that, prudence must come from what the agent does not know.
> - **Lushness compresses, and an optimizer pushes hardest on what it
>   compresses away.** Options with equal lushness can differ in other ways.
>   If any of those differences matter to value, a strong optimizer is
>   likely to find them. The compression test of
>   [chapter 31](#chapter-31) is therefore a test of alignment as well.
> - **A ranking is a standard to act against, not a policy to act on.** The
>   framework says what an agent's acts are judged by. When to act, defer or
>   accept correction is the work of Gradient Ethics, the separate book that
>   follows this one.

**Bold-only test.** Read alone, the bold lines run: the offer and its
limit; the requirements met; the local misuse; why even the whole-field
objective, once estimated, drifts towards the local one; no caution; the
compression risk; the boundary with Book Two. Every bold line states a
result, and none of them announces an agenda. No toy figures appear.

## 3. Section ladder

Each header is a claim or the reader's question. Read in order, the headers
trace the argument.

| § | Header | What it does | Sources |
|---|---|---|---|
| 26.1 | **What an artificial agent's standard must do** | Restates chapter 1's three requirements (no dependence on whose preferences trained it; favours no group; keeps working as understanding grows). Preference learning inherits whose preferences were learned (Gabriel 2020; Russell 2019, credited fairly). Reader's question first: *what would an objective look like that no one's preferences wrote?* | ch 1 §1.5–1.6; Overview §7 |
| 26.2 | **A standard no one's preferences wrote** | The whole-field comparison meets the requirements: physics sets it; the comparison with no index names no part ([A.7.8](#a-7-8), [A.7.9](#a-7-9)); a better model of the world is a better model of Omega. **Concede:** the identification and the composition rule are commitments (ch 10 §10.3), so the standard is not choice-free; it is one stated, testable choice, not a list of who counts. **Concede:** "keeps working" is not "never changes its verdicts". Verdicts at a coarser level can be corrected once a finer level is shown faithful, and which level governs is open ([A.6.5](#a-6-5); A.15). Testable: exact models score any proposed policy. Ends on the turn: *the standard is fixed; what an agent knows of it is not.* | ch 1, 4, 8, 10; A.6.5, A.7.8–A.7.9, A.15 |
| 26.3 | **The agent is inside the field** | Short. An artificial agent is a valuer (ch 3) and a controller (ch 25). Capability gains it no standing, and being artificial costs it none. Its own futures are counted in the whole field, once. Whether it experiences anything is left to chs 18 and 22. Special protection under uncertainty, for any party, is Book Two's. This section does not depend on consequence flux (see §6, question 6). | ch 3 §3.6; ch 25 §25.1; ch 10 §10.6 |
| 26.4 | **The same count, aimed at oneself** | One measure, two scopes. The self–whole gap ([A.7.6](#a-7-6)): Δℓ_whole = Δℓ_agent + Δℓ_rest∣agent. Agent-centred objectives (empowerment, causal entropic forces, maximum occupancy) are local comparisons in this manuscript's sense (ch 4 §4.6; ch 25 §25.6). Relation to the power-seeking results (Turner et al. 2021) is set out as a correspondence, not a derivation. **Model instance, body only:** in model C.14 the blocker gains while the whole field narrows (M1, D.3.6). The local comparison also rewards uncontrolled variation, so it does not always lead to power seeking (ch 4 §4.4). Misappropriation, defined: presenting a local comparison as the whole-field verdict. The defence is chapter 4's scope, not an extra rule. *Primer: power seeking and side effects.* | A.7.5–A.7.7; C.14; ch 4 §4.4; ch 25 §25.6 |
| 26.5 | **Naming the whole is not modelling it** | The new argument of the chapter. A bounded agent ranks by an *estimate* of whole-field lushness. The term that separates the agent's scope from the whole field's is the one that depends most on parts of the field the agent does not see (ch 10 §10.6: far away, far ahead). Requisite variety with a thin model ([A.13.2](#a-13-2)): unmodelled variety passes into outcomes unless it is accommodated or suppressed. Suppression is always available to a capable controller (ch 25 §25.4). Side-effect penalties (Krakovna et al. 2019; Turner, Hadfield-Menell and Tadepalli 2020) are local relatives. The whole-field scope makes side effects part of the objective rather than a penalty added to it, but estimation still leaves the gap. An agent's uncertainty is not branching in the field, and its errors are consequences (ch 10). **Proposed conjecture 26.1** (see §4). Evidence stub: the bounded-agent test is not built (D.4). | A.13.2; A.12.1; ch 10 §10.6; ch 25 §25.4; D.4 |
| 26.6 | **A measure without caution** | Risk neutrality in rate, and risk seeking by at most H(p) bits in total ([A.5.2](#a-5-2)). Ruin counts by its size, which grows with the horizon, not by an inflated probability. Body figure: the measure accepts a 70% chance of ruin for a 30% chance of a law worth 4 more bits (D.5.3). Pascal's mugging (Bostrom 2009): finite stakes defeat long shots *given* premises F1–F3 ([A.5.3](#a-5-3), conditional); no universal bound on branching is claimed. A recorded randomization cannot rescue a much worse policy (A.5.2(b)). Prudence beyond expectation must come from model error and option value. That is chs 23–24 and Book Two, not the measure. Ends: *the measure will not supply caution, so anyone who builds on it must.* | A.5.2–A.5.3; A.9.5; D.5.3 |
| 26.7 | **What the count compresses** | The compression boundary (A.15). The measure is not injective. By control invariance ([A.2.5](#a-2-5)), consent and coercion, distributed and concentrated control, differ only through the law they induce. Goodhart, applied to this measure: three questions kept apart (does the estimate misrepresent breadth; does the comparison omit futures; does accurately measured breadth misjudge value). Only the third tests the thesis. Noise: the repertoire ceiling ([A.2.4](#a-2-4)) and ch 15. Optimization pressure goes to wherever the count is blind, so an aligned use of the measure raises the stakes of the compression pairs (ch 31; D.4). | A.15; A.2.4–A.2.5; ch 15; ch 31 |
| 26.8 | **A ranking is not a policy** | Ch 10: a ranking does not by itself give authority to act. What the framework hands an alignment programme: a standard to judge acts against, and a test bed. What it does not hand over: a decision rule, a deference or corrigibility protocol, margin calibration, a training method, estimators. The off-switch game (Hadfield-Menell et al. 2017) is noted as the canonical framing of the problem Book Two inherits; the framework has not solved it. **Optional table** (§6, question 4): Concrete Problems (Amodei et al. 2016), mapped onto what this chapter addresses and what Book Two inherits. | ch 10 §10.6; ch 24; A.13.3 cited only as a decision model |
| 26.9 | What would count against these claims | See §4. | |
| 26.10 | What the chapter gives the rest of the manuscript; what it does not claim | Pointers to chs 31, 32 and Book Two; a list of exclusions (§5). | |

Then the status table and the references.

**In Omega box (26.2):** *An artificial agent is a controller inside Omega.
The whole-field comparison reads the part of Omega that follows from the
present under each of its options. What the agent can compute is a model of
that part.*

## 4. Claim-status ledger

| Status | Claims |
|---|---|
| **D** | misappropriation: a local comparison presented as the whole-field verdict (26.4). Possibly none other; the chapter defines little. |
| **Argued** | the whole-field comparison meets chapter 1's three requirements, with the concessions in 26.2; an artificial agent is a valuer and a controller, with no standing gained or lost (26.3); naming the whole field does not put it in the model, and the gap term is the hardest to estimate (26.5); caution must come from outside the measure (26.6); optimization raises the stakes of the compression boundary (26.7); a ranking is not a policy (26.8) |
| **T** | the self–whole gap ([A.7.6](#a-7-6)); subjects that lose nothing ([A.7.7](#a-7-7)); the subject of the comparison with no index ([A.7.9](#a-7-9)); risk neutrality and recorded mixtures ([A.5.2](#a-5-2)); finite stakes, *conditional on F1–F3* ([A.5.3](#a-5-3)); requisite variety and the thin model ([A.13.2](#a-13-2)); repertoire ceiling ([A.2.4](#a-2-4)); control invariance ([A.2.5](#a-2-5)) |
| **M** | blocking widens the blocker and narrows the whole (model C.14, M1), as an instance of the scopes diverging (26.4). Model C.17 is **not** cited (record not in the archive). |
| **E** | maximum-occupancy agents (Ramírez-Ruiz et al. 2024), as a related correspondence, consistent with chapter 25 |
| **C** | **Conjecture 26.1 (proposed, author to decide):** in coupled worlds, a bounded agent that ranks by its estimate of whole-field lushness, with a model that misses part of the rest of the field, chooses suppression over accommodation of the unmodelled part more often than the same agent with the full model. *Would count against it:* matched bounded-agent models in which a thin model suppresses no more often than a full one. Test not built (D.4, "Bounded agents and local knowledge"). |
| **Open** | estimators with error bounds; installing an objective in a trained system; the governing faithful resolution; the compression boundary; a universal bound on branching; conjecture 26.1 |

## 5. Explicit exclusions

- No claim that a maximizer of the scalar, local or whole-field, is safe.
- No decision rule, deference policy, corrigibility protocol or margin
  calibration. These are Book Two's (outline r28; style sheet r26).
- No account of how to train or install the objective (the inner-alignment
  problem). The chapter concerns the target, not how a system is made to
  pursue it.
- No moral-status verdict on artificial agents beyond universal admission:
  no special standing, and protection under uncertainty left to Book Two.
- No claim about whether artificial agents are conscious (chs 18, 22).
- No dependence on consequence flux or on test-bed results (same rule as
  ch 25 [142]).
- No Alpha.
- No toy numbers in the TL;DR. Model figures stay in the body.

## 6. Decisions needed from the author

1. **The headline.** Is "an objective no one's preferences wrote; pursuing
   it does not make an agent safe" the right framing? It is stronger on the
   limits than Overview r19 §7 ("an evaluator, a decision structure, a reason
   to stay correctable, and a test bed"). Under r28 the second and third of
   those move to Book Two, so the Overview needs to follow at compilation.
2. **Conjecture 26.1 (26.5).** It is a new claim and the chapter's main
   contribution. Should it be adopted as a conjecture with an M4 evidence
   stub, or kept as an argued remark with no C status?
3. **How much of correction stays here.** v4 chapter 9 derived a persistent
   reason to seek correction ("no system holds the whole"). Proposal: one
   paragraph of diagnosis in 26.8, with deference and the value of a
   channel left to chapter 24 and Book Two. Please confirm against chapter
   24 r2, which I could not read.
4. **The Concrete Problems table (26.8).** Include it (useful to AI readers,
   and the handoff lists the paper), or leave it to Book Two?
5. **Maximum occupancy wording.** Overview r19 says maximizing lushness
   "coincides with" the maximum-occupancy principle. That principle weights
   action entropy and state entropy separately, with its own discounting, so
   I would write "is closely related to" until the two are checked against
   each other. The Overview would then follow.
6. **Consequence flux (handoff §5, chapter 25).** The five critiques are
   substantive. A binary switch has Φ ≤ 1 bit whatever its downstream
   effect. Conditioning on R₀ does not establish record-conditioning. The
   intervention distribution is unspecified. Chapter 26 is designed not to
   depend on the answer. Do you want to (a) keep 25.2 as a provisional
   definition and add a short note naming these limits, or (b) revise 25.2
   now, for example by separating "distinguishability of downstream
   histories" from leverage?

## 7. Live objections to meet at full strength

- **"Physics-set" disguises a choice.** The designers chose lushness and the
  resolution. *Reply:* conceded in part (26.2). The identification is a
  commitment, but it is one stated and testable claim, not a list of who
  counts.
- **Specifying the objective is the easy part of alignment.** *Reply:*
  conceded. The chapter claims only to concern the target (26.8).
- **A whole-field maximizer would turn the world into noise.** *Reply:* the
  repertoire ceiling and chapter 15. Concede short horizons and fixed
  repertoires (26.7).
- **A whole-field objective licenses overriding people for the greater
  good.** *Reply:* a ranking gives no authority to act. Overriding discards
  records the imposer lacks (ch 10). Book Two.
- **An agent that gives humans no special weight is dangerous.** *Reply:*
  stated honestly. There is no special standing, only special protection
  under uncertainty (ch 10 §10.6, ch 17), and Book Two calibrates it. This
  objection has to be stated in the chapter, not deferred.
- **Risk neutrality is disqualifying.** *Reply:* conceded as a stated risk
  (26.6). The measure is not the whole of a decision procedure.

## 8. References to verify before the chapter is marked final

Amodei et al. (2016); Ashby (1956); Bostrom (2009); Gabriel (2020);
Goodhart (1975); Hadfield-Menell, Dragan, Abbeel and Russell (2017);
Klyubin, Polani and Nehaniv (2005, 2008); Krakovna et al. (2019); Manheim
and Garrabrant (2018); Ramírez-Ruiz et al. (2024); Russell (2019); Turner et
al. (2021); Turner, Hadfield-Menell and Tadepalli (2020); Wissner-Gross and
Freer (2013).
