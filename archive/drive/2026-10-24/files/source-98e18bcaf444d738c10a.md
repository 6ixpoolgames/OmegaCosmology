# Appendix D. Evidence map

> **Drafting note (r2, 18 October).**
> - Sol's audit of r1, folded in:
>   - **Count corrected:** 19 tests not yet built, not 18.
>   - **M1 split by documentation:** 10 claims record the levels of detail
>     tested; 9 (†) do not and are provisional assignments.
>   - **M2 and M3 made disjoint:** M2 has at least one resolved ranking and
>     no reversal; M3 has none resolved, or resolved rankings of opposite sign.
>     Zero claims at M3 is no longer allowed to hide the sign changes seen in
>     operating ranges (D.1, D.6).
>   - **Finer cadences:** the capacity loop's win at finer cadences now cites
>     Theorem A.6.3 as a limit, with the unchecked range stated.
>   - **Information and organization narrowed:** information without leverage
>     does not outperform free variation under matched registers; the locked
>     source is an access claim, and a rate contrast does not by itself show
>     access.
>   - **Rate capability kept separate from the activity-matched test** (D.4).
>   - **D.9 rewritten:** each claim states its quantifier and domain, and what
>     would count against it is matched to that strength, with three grades of
>     contrary evidence.
>   - **Scope of the map:** the formal results, test-class claims and
>     correspondences the evidence program tracks, not "every claim".

> **Drafting note (r1, 18 October).**
> - First draft. Built from ledger r9 (Tier A rows, Tier C table, "C4 in
>   detail", "C23 in detail") and the program review r1 (section 3, with the
>   C5 corrections of fix note r2 folded in). Every figure is to be rechecked
>   against Appendix C once it is written.
> - Chapter 31 is the readable account of this map (ruling 43).
> - **Four tiers for model results** (ruling 43), applying chapter 12's rule
>   that a ranking holds only when it is resolved, with the same sign, at every
>   admissible level of detail:
>   - **M1** holds at every level of detail tested;
>   - **M2** holds at one level of detail, or a few, and is not yet shown at
>     the others (they are unresolved, or untested);
>   - **M3** unresolved, or the sign changes between admissible levels;
>   - **M4** not yet built.
> - **A limit on M1.** For most models the sources record which cadences and
>   grains were tested, but not a declared admissible range. Until Appendix C
>   declares one for each model, M1 means "every level tested", not "every
>   admissible level". Rows whose sources do not record the levels tested at
>   all are marked †.
> - Several rows drop a tier under the rule. The headline domination result
>   is M2: grain-stable over a fivefold refinement at one cadence (0.25);
>   other cadences are not reported in the sources.
> - The five checks of review r1 section 8 ("must land") have not landed. Each
>   affected row says so.

This appendix lists the formal results, the claims of each test class and the
empirical correspondences that the evidence program tracks, with their status,
the chapter that argues each, and the evidence for it. [Chapter 31](#chapter-31)
walks through it one class of cases at a time. Nothing in the main text may
claim more than its row here allows.

---

## D.1 How to read the map

**Every row has a status, and every model result has a tier.**

The six statuses are those of the whole manuscript.

| Status | What it is |
|---|---|
| **D** | a definition |
| **T** | a theorem, proved in [Appendix A](#appendix-a) or cited with its source |
| **M** | a model result, shown in a named model of [Appendix C](#appendix-c), within its scope |
| **E** | an empirical correspondence: published work showing a mechanism operating in the real world |
| **N** | a normative premise, assumed and named. The manuscript has none. |
| **C** | a thesis or conjecture, asserted or proposed, with what would count against it |

A model result also carries one of four tiers, which say how far its ranking
holds ([chapter 12, section 12.5](#chapter-12)).

| Tier | Meaning |
|---|---|
| **M1** | resolved, with the same sign, at every level of detail tested |
| **M2** | resolved at one level of detail or more, and nowhere reversed; at the other levels the ranking is unresolved or untested |
| **M3** | no resolved ranking at any level tested, or resolved rankings of opposite sign at admissible levels |
| **M4** | not yet built |

Of the nineteen claims at M1, ten record the levels of detail tested. The
other nine (†) are provisional assignments, not verified ones.

No claim of the thesis sits at M3. That does not mean no sign has changed
anywhere. Signs changed with cadence in results that make no claim of the
thesis, and those are listed with the operating ranges (D.6).

Three further classes sit outside the tiers, because they make no claim on the
principle.
- **Operating range:** a model maps how a mechanism behaves across its
  parameters, without a verdict for or against the principle.
- **Pressure:** a result the manuscript has to answer.
- **Diagnostic or withdrawn:** a result from a model that fails one of the
  five conditions of [chapter 12](#chapter-12), or that was withdrawn on audit.
  These are kept in [Appendix H](#appendix-h) and never cited as evidence.

A figure marked † comes from a source that does not record the levels of
detail tested. Its tier is provisional until [Appendix C](#appendix-c)
records them.

---

## D.2 What is derived (status T and D)

**[Appendix A](#appendix-a) contains seventy-six numbered results: definitions,
results established elsewhere, results proved there, results conditional on
named physical premises, and one analytical model.**

| Status in Appendix A | Number | Examples |
|---|---|---|
| Established elsewhere | 15 | the chain rule (A.2.1); the unique effective count (A.2.3); the temporal expansion (A.6.3); option value (A.9.6); the decision recursion (A.13.1) |
| Proved here | 43 | the offset theorem (A.3.5); the profile and the verdict (A.3.9); the robustness floor (A.4.6); what persistence is worth (A.4.8); the cost of an early end (A.4.9); the self–whole gap (A.7.6); the subject of the unindexed comparison (A.7.9); the factorial identity (A.8.3); information pays through action (A.8.4); the largest contraction (A.9.4) |
| Conditional on named physical premises | 2 | finite stakes (A.5.3); the persistence cap (A.5.4) |
| Analytical model with stipulated payoffs | 1 | deference and correction (A.13.3) |
| Definitions | 15 | declared resolution (A.6.1); sign stability (A.6.5); valuer and whole field (A.7.1); resolved subject rankings (A.7.4); contraction (A.9.2); foreclosure (A.9.3) |

Where each result is used:

| Chapter | Results it rests on |
|---|---|
| [4](#chapter-4) Counting futures | A.1.1–A.1.2, A.2.1–A.2.5 |
| [5](#chapter-5) Futures through time | A.3.1–A.3.9 |
| [6](#chapter-6) How long things last | A.4.1–A.4.9, A.5.1–A.5.4 |
| [7](#chapter-7) Resolution | A.6.1–A.6.5 |
| [8](#chapter-8) Parts and wholes | A.7.1–A.7.7, A.7.10 |
| [10](#chapter-10) The comparison with no index | A.7.8–A.7.9 |
| [11](#chapter-11) The central thesis | A.9.2–A.9.4 |
| [12](#chapter-12) How the thesis is tested | A.2.1, A.3.5, A.3.6, A.3.9, A.6.1, A.6.5, A.7.4, A.8.3, A.9.2, A.9.3, A.11.1–A.11.2, A.12.1 |
| [14](#chapter-14) Information pays through action | A.8.1–A.8.4 |
| [17](#chapter-17) Harm as narrowing | A.4.9, A.9.1–A.9.4 |
| [20](#chapter-20) Cooperation and joint access | A.2.5, A.10.1–A.10.3 |
| [24](#chapter-24) Choosing inside the structure | A.12.1–A.12.2, A.13.1, A.13.4–A.13.5 |
| [25](#chapter-25) One uncertainty, many places | A.9.5–A.9.6, A.13.3 |
| [29](#chapter-29) Quantum frames | A.14.1–A.14.10 |

What the formal core does not contain is listed in section A.15. The largest
item is the central thesis itself.

---

## D.3 Model results, by test class (status M)

**Each row gives the claim, the model, the key figures, the tier, and what is
still pending.**

### D.3.1 Organization reaches a source that disorder cannot ([chapter 13](#chapter-13))

| Claim | Model | Evidence | Tier | Scope and pending |
|---|---|---|---|---|
| A law under which organization can release a locked source beats the same law with that path removed | [locked source](#c-locked-source) | +0.260, +0.229 and +0.197 bits per unit time at three cadences; sign stable. Within the capable law, starting points tie in rate, as [Theorem A.3.5](#a-3-5) requires. | M1 | 16-state fixture. This is an access claim: the ablated law cannot release the source. A positive rate contrast elsewhere does not by itself show access to futures otherwise unreachable. The capable law accepts more external work, so this is an advantage in access and throughput. A cleaner ablation, keeping the locked resource present with its own dynamics, is pending. |

### D.3.2 Information without leverage does not outperform free variation; informed action can ([chapter 14](#chapter-14))

| Claim | Model | Evidence | Tier | Scope and pending |
|---|---|---|---|---|
| A register that tracks the world but cannot act on it scores below one that varies at random | [paid sensing](#c-paid-sensing) | Informative writing without action lost to random writing in 16 of 16 cases; uninformed movement lost in 15 of 16. | M1† | Matches [Proposition A.8.2](#a-8-2), which holds under matched register conditions. |
| Where information can be used to act and the structure using it can be rebuilt, informed action has the higher rate | [paid renewal](#c-paid-renewal) | Higher limiting rate in 57 of 57 comparisons (19 laws, 3 cadences). Finite wins: none at T64, 5 of 19 laws at T256, 13 of 19 at T1024. | M1 | The repayment horizons, 220–879 time units, were longer than the 64 steps guessed beforehand. |
| The advantage lies in information and action together | [paid renewal](#c-paid-renewal) | Informed beats random action in 57 of 57; information alone and action alone each beat the idle version in 0 of 57. | M1 | The two-factor split of [Proposition A.8.3](#a-8-3). |
| In short-lived valuers, information does not repay its cost | [paid sensing](#c-paid-sensing), mortal fixtures | The information term was positive in every pooled setting, yet the uncoupled register won 14 of 16, because lives of about 7 time units were far shorter than any repayment horizon. | M1† | Consistent with the robustness floor ([Corollary A.4.6](#a-4-6)). |

### D.3.3 Persistence and compounding ([chapter 15](#chapter-15))

| Claim | Model | Evidence | Tier | Scope and pending |
|---|---|---|---|---|
| An enabling loop retains apparatus near capacity and raises the rate with capacity | [capacity](#c-capacity) | Retention 3.94/4, 7.95/8, 15.89/16, 30.79/32; single-assistance ablations retain a quarter or less, in all 24 laws. Rate gain over basal +2.37, +3.44, +4.73 and +6.65 bits per unit time at cadence 0.25. Capture funds 96.6% at the central point. | M1 | No cadence-dependent signs in the grid. The loop leads in both event count and event-path entropy, so by [Theorem A.6.3](#a-6-3) it wins in the limit of fine cadence; cadences between the grid and that limit are not checked. Bounded compounding under declared kinetics; catalytic magnitudes conservative. |
| An enabling relation adds breadth that a non-enabling process at matched accepted work cannot | [matched work](#c-matched-work) | 12 of 12 positive at every cadence; captured energy funds 90–94.7% of the loop. | M1 | Accepted work matched, activity not (D.5.1). |
| Three successive paid enabling links compound, with retained expansion | [compounding](#c-compounding) | Three-link completion in all 12 shape settings, square-root feedback included. Cutting any link lowers retained expansion, measured without link labels. | M1 | Count chemistry, no positions. The chain tracker misses true chains, so completions are lower bounds. |
| The full mechanism beats the unbound preparation, all assistance switched off, and the cut loop | [compounding](#c-compounding) | At T256, at every cadence, in all 40 settings, stressed settings included; +165 bits over unbound and +366 over all-off at source 2.4. | M1 | The lushness lead shrinks under stress and never reverses. |
| Compounding persists at baseline wear | [compounding](#c-compounding) | Functional uptime 50–55% over 64–256 at medium and high source, with no closure. | M1† | Under heavy damage, see D.6. |

### D.3.4 Harm and protection ([chapters 17](#chapter-17) and [18](#chapter-18))

| Claim | Model | Evidence | Tier | Scope and pending |
|---|---|---|---|---|
| The policy that keeps the most open protects channels, not stock | [channels](#c-channels) | The winner sits between lock-in and burnout on every protection readout and keeps 4.8–9.2% less working apparatus than constant servicing, across capture factors 1–12. | M1† | Earlier reports scored this as failure; reread under the account (chapter 12, section 12.7). |
| Productive configurations beat their non-conducting arm | [channels](#c-channels), paid capacity | 78 of 78. | M1† | Capability, not margin. |
| Physical dependence can make maintenance the policy that keeps the most open | [dependence](#c-dependence) | Servicing rises from 75% to 100% when the gate relaxes; the winner beats passive idle, 6.195 against 5.903 bits per unit time; the one-step planner carries 1.248 points more closure risk. | M1† | Within scope: dependence is not sufficient in general. |
| The structure of a harm sets policy, not its raw hazard | [harm sweep](#c-harm-sweep) | Irreversible loss of hardware that has substitutes did not induce its preservation (87–91% chance of losing it; the channel stayed open). Raw hazard moved policy weakly: 4 of 15 comparisons increased servicing, one reversed. | M2 | Shown at T64 and T256 at one hazard; a check across cadences is pending. |
| Longer horizons favour maintenance | reserve and [harm sweep](#c-harm-sweep) | 17 of 20 and 22 of 24 adjacent horizon steps increased servicing; none decreased. | M2 | Pending: the trend at cadences 0.125 and 0.5 across the whole candidate family. |
| A harm that lowers the rate eventually outweighs any finite gain | several | 40 of 40 long-run loss comparisons favour the intact structure. | M1† | Late crossovers are pressure (D.5.2). |

### D.3.5 Suffering ([chapter 19](#chapter-19))

| Claim | Model | Evidence | Tier | Scope and pending |
|---|---|---|---|---|
| A valuer with an aversive drive to escape an obstacle it cannot pass has narrower futures than the same valuer without the drive | [register controls](#c-register-controls) | Independent variation > injury-linked register without escape drive > obstructed suffering, at all 18 primary points at the finest level tested; the drive-free valuer beats the suffering one in all 216 comparisons; removing the futile drive adds 0.42–0.54 bits at the reference upkeep. | M2 | At the coarser, merged-signal level, 44 and 43 sweep cases are unresolved and none reverses. Two base worlds by nine upkeep levels; the W1 parameter sweep has not landed. |
| Paid neutral variation outscores an inactive register | [register controls](#c-register-controls) | Up to upkeep of 1–2 times basal power, with the crossing bracket the same at every cadence and horizon; replicated 16 of 16 in a richer resource model. | M1 | Per register, against basal power. |

### D.3.6 Constraint and domination ([chapter 21](#chapter-21))

| Claim | Model | Evidence | Tier | Scope and pending |
|---|---|---|---|---|
| Constraint is judged by its consequences | [domination](#c-domination), first map | From T64 onward at every cadence, in four environments: steering away from a trap +9.5 to +13.2 bits; blocking access −6.3 to −8.4; blocking construction −4.5 to −6.0; steering into the trap −7.6 to −9.9. The constrained party's lushness moved with the whole field's in all 20 cases. | M1 | Corrected steering with the pocket: 144 of 144 whole-positive. The dominator's own lushness was unresolved throughout this map. |
| Blocking another's access narrows the whole while widening the blocker's own futures | [domination](#c-domination), corrected | Whole field −13.64 bits; blocker +4.85 to +14.06; blocked party −25.78 to −14.18 (T256, cadence 0.25). The same pattern at bank grids 0.5, 0.25 and 0.1; survives movement-only steering. | M2 | Grain-stable over a fivefold refinement, at one cadence. Other cadences are not reported in the sources. |
| The conflict also runs the other way | [domination](#c-domination), conservative field | The constraining party loses while the constrained party and the whole gain, at T1024, at all cadences. | M1 | — |
| Domination is not the dominator's best option when production is available | [domination](#c-domination) | Productive hardware's lower bound on the dominator's gain exceeds blocking's upper bound. | M2 | One certified point; horizons and cadences have not landed. |
| Directional flow narrows more than zero-net exchange at matched volume | [flow](#c-flow) | Directional flow loses to zero-net exchange in 18 of 18 comparisons; volume at zero net adds 23.95 bits. | M1† | The direction was set by an external affinity; a version funded by the dominator is pending. |

### D.3.7 Choosing inside the structure ([chapters 24](#chapter-24) and [26](#chapter-26))

| Claim | Model | Evidence | Tier | Scope and pending |
|---|---|---|---|---|
| Crossover horizons fall where the theory says | rate-first analysis, several models | Exact crossings within one step of the predicted crossover wherever transients are short; the persistence-weighted total agrees with ranking by rate exactly when expected persistence exceeds the crossover horizon (14 cases). | M1† | Checks of [Proposition A.3.7](#a-3-7) and [Corollary A.4.7](#a-4-7). |
| The whole field's best policy depends on state and horizon | [policy search](#c-policy-search), contact world | +4.9 bits over the best constant policy at T256. | Operating range | D.6. |

---

## D.4 What is not yet built (tier M4)

**Each open test is named with what it would decide.**

Two of them are often run together and should not be. That organization can
raise the rate at which futures open is shown in models without the
activity-matched comparator (D.3.1, D.3.3). The comparator tests something
further: whether a rate gain reflects enabling structure rather than activity
alone.

| Test | Decides | Chapter |
|---|---|---|
| Activity-matched comparator | whether a rate gain reflects enabling structure rather than activity alone: organization against busy noise doing as much | [16](#chapter-16), [32](#chapter-32) |
| Compression pairs | whether options of equal lushness can differ in ways that matter, and whether the difference reappears at longer horizons or finer levels of detail | [16](#chapter-16), [32](#chapter-32) |
| Plural ecology against confinement | whether a plural ecology outproduces a dense confined population on the same land (the factory-farming objection) | [19](#chapter-19), [23](#chapter-23), [32](#chapter-32) |
| Monsters and monocultures | whether one vast valuer, or one kind of valuer, can outscore a plural world | [23](#chapter-23), [32](#chapter-32) |
| Spatial model with several carriers | organization against disorder where disorder has room to spread, with a loop that keeps itself going | [13](#chapter-13), [15](#chapter-15) |
| Steering by incentive against steering by punishment | whether incentive is at least as lush as punishment towards the same target | [19](#chapter-19), [21](#chapter-21) |
| Hijacked signals | whether suffering that fires independently of any hazard competes | [19](#chapter-19) |
| Signal design | whether the signal that keeps the most open is intermediate and tracking, in a world where escape can pay | [19](#chapter-19) |
| Precaution under uncertainty | graded protection by a controller uncertain about the harm regime | [25](#chapter-25) |
| Tracking an obstruction that may lift | whether tracking keeps value in proportion to the chance of escape | [25](#chapter-25) |
| Bounded agents and local knowledge | controllers with mismatched models, with and without correction | [24](#chapter-24), [27](#chapter-27) |
| Opportunity windows | what follows when a source shuts down, and whether it can change the sign earned before | [15](#chapter-15) |
| Cross-scale composition | whether nested organization extracts more from a coupled gradient | [23](#chapter-23) |
| Embodied closure risk | whether protection lowers the risk of closure, against the rate after closure | [18](#chapter-18) |
| A justified matching rule | comparing alternatives that differ in earlier architecture | [33](#chapter-33) |
| Tests of generativity's rate in real systems | whether organization raises the rate at which futures open outside the models | [33](#chapter-33) |
| The criterion for physical frames | what makes a composite system a frame of its own | [33](#chapter-33) |
| Estimators with error bounds | lushness for realistic systems | [33](#chapter-33) |
| Comparisons between frames that disagree about records | quantum covariance and merging frames | [29](#chapter-29), [33](#chapter-33) |

---

## D.5 Pressure: results the manuscript has to answer

### D.5.1 Activity counts, and often wins

| Result | Model | Figures | Where answered |
|---|---|---|---|
| Activity contributes to finite comparisons, and the measure subtracts nothing for it | several | Paid variation, exchange volume, funded transfer and cycling selectors all add breadth. | [16](#chapter-16) |
| At fixed numbers of events, the enabling loop loses early and wins later | [capacity](#c-capacity) | Loses at 8 events (−1.76 bits); wins at 32 and 128. Each event is also less predictable: 1.05 against 0.38 bits per event. | [16](#chapter-16) |

### D.5.2 Material loss without narrowing

| Result | Model | Figures | Where answered |
|---|---|---|---|
| Permanent loss can raise lushness for a while | [compounding](#c-compounding) | Replacing repairable damage with 5% permanent loss raised T256 breadth in 4 of 8 contrasts, at all cadences. At one setting: +1.17 bits at T256, still positive at T1024, −2.46 at T4096. | [17](#chapter-17), [32](#chapter-32) |
| Funded appropriation widens every party | [flow](#c-flow) | The dominator pays from its own store, net 0.056 units flow to it, its energy rises and the other's falls; yet the whole field and both parties gain breadth, through turnover. | [17](#chapter-17), [21](#chapter-21) |
| A party's breadth can rise while its stock falls | [flow](#c-flow), funded pump | The constrained party's breadth rose while its stock fell. | [16](#chapter-16), [32](#chapter-32) |

### D.5.3 Other pressure

| Result | Figures | Where answered |
|---|---|---|
| Constraint wins every finite comparison through T1024, though most constrained laws have a lower rate | All 72 finite comparisons; four of six constrained laws have a lower rate; reversals estimated at about 7,200–36,000 time units. Exact bracketing has not landed. | [21](#chapter-21) |
| The measure is neutral to risk at known odds | It accepts a 70% chance of ruin for a 30% chance of a law worth 4 bits more. Prudence comes from model error and option value ([Corollary A.5.2](#a-5-2)). | [24](#chapter-24), [25](#chapter-25) |
| Private rankings are often unresolved | Policy differences of a few bits sit inside bound widths of tens of bits; what a dominator would choose among many policies is unresolved. | [21](#chapter-21), [26](#chapter-26) |
| In an exact worked example of a coupled commons, domination leads narrowly at fixed capacity until a channel-opening mechanism reverses it | Example E10 of the previous version. | [21](#chapter-21) |

---

## D.6 Operating ranges: mapped, with no verdict on the principle

| Result | Model | Figures |
|---|---|---|
| On a spatial lattice, an organized seed beats the thermal mixture and loses to an unbound start | [lattice](#c-lattice) | The seed beats the thermal mixture in 12 of 14 laws at every cadence. Against the unbound start at T4096, the unbound start wins at all cadences in 12 of 14, and 2 change sign. The implemented feedback does not sustain assembly: one carrier with a charge bottleneck. One mobility coefficient drives the regime; its sweep has not landed. |
| Compounding under heavy damage | [compounding](#c-compounding) | At source 0.6, raising damage from 0.005 to 0.02 and 0.08 drops retained three-link expansion from 10% to 0.9% and about 0.001%, and uptime from 50% to 11% and 0.1%. The shape resembles an error threshold (Eigen 1971). |
| Structure pays when it persists long enough to repay its cost | [compounding](#c-compounding) | Uptime and the breadth advantage rank together at every horizon (Spearman 0.82–1.0). A hypothesis with descriptive support; opportunity windows not run. |
| The blocker's private gain comes from paid enforcement, not appropriation | [domination](#c-domination) | Capture gain 0.081 against a bill of 0.330. |
| Best policies in an integrated world cycle reversibly among modes | [policy search](#c-policy-search) | Active idle wins uniquely, +92 bits over holding at T256: the first test-bed instance of the correspondence with maximum-occupancy agents (Ramírez-Ruiz et al. 2024). Sensitive to selector kinetics; that sweep has not landed. |
| Signs that change with cadence | [lattice](#c-lattice); reserve | On the lattice, against the unbound start, 2 of 14 laws change sign across cadences, and so does the target case (−14.7, −3.8 and +7.7 bits at cadences 0.125, 0.25 and 0.5). A reserve policy against constant servicing changed sign with cadence. None is a claim of the thesis, so none is tiered. |
| Baselines invert between models | [lattice](#c-lattice), [compounding](#c-compounding) | On the lattice the seed beat the thermal mixture and lost to the unbound start; in the count model it beat the unbound start and lost to the thermal mixture. Neither transfers to the other model. |

---

## D.7 Diagnostics and withdrawn results

**Kept on record in [Appendix H](#appendix-h). None is cited as evidence for
or against the thesis.**

| Result | Why it is a diagnostic or withdrawn |
|---|---|
| The "uncatalysed" control beat the catalysed process, 36.60 bits to 36.36 | The control was a more permissive law: feedback without apparatus at the catalysed rate. The answer was built in. |
| Calm obstruction beat the suffering valuer at two points, by +0.258 and +0.153 bits | The calm valuer had lost its inner variation as well as its drive, so the comparison was with a simpler valuer. |
| Confinement, forced labour and forced harvesting (first stage of the domination design) | Withdrawn on audit: a steering rule redirected 100% of the chemistry. The blocking rows stand. |
| The thermal mixture in the count model | The wrong reference: it starts with more machinery, and a model without positions lacks what makes disorder the default. |
| Hijacked-signal first batch | Neither arm was the intended object: the independent firing narrowed through its own costs, and the comparator did not track the hazard. |
| Early paid-renewal targets ("refund ratio above 1", "coverage crosses 1") | Ill-posed: stationary funding fractions sum to 1. |
| Surviving-hardware deep grid | Its ranking was decided by the tail after closure. |
| Thin-world and three-quarter-law calculations | Diagnostics for plural ecology and cross-scale composition, not tests of them. |

---

## D.8 Empirical correspondences (status E)

**Published work showing a mechanism operating in the real world. These
correspondences motivate hypotheses about rate and mechanism. They never show
that lushness is the right ranking.**

| Mechanism | Source | Verified | Chapter |
|---|---|---|---|
| Organized processes raising the rate of free-energy capture | Kleidon (2012) | yes | [Overview section 4](#overview-4), [15](#chapter-15) |
| Sustained adaptation with no plateau | Wiser, Ribeck and Lenski (2013) | yes | [Overview section 4](#overview-4), [15](#chapter-15) |
| Error thresholds for replicating information | Eigen (1971) | yes | [Overview section 4](#overview-4), [15](#chapter-15) |
| Option value under irreversibility | Arrow and Fisher (1974); Henry (1974) | yes | [Overview section 5](#overview-5), [25](#chapter-25) |
| Maximum-occupancy agents | Ramírez-Ruiz et al. (2024) | yes, by DOI | [Overview section 7](#overview-7), [26](#chapter-26) |
| Leverage and sensing | Kussell and Leibler (2005) | to verify | [14](#chapter-14) |
| Bet hedging | Cohen (1966) | to verify | [14](#chapter-14) |
| Horizon and the commons | Ostrom (1990) | to verify | [18](#chapter-18), [20](#chapter-20) |
| Channels and plurality | Yachi and Loreau (1999) | to verify | [18](#chapter-18), [23](#chapter-23) |
| Compounding in cultural evolution | Kline and Boyd (2010); Kremer (1993) | to verify | [15](#chapter-15) |
| Domination narrowing an ecosystem | Paine (1966) | to verify | [21](#chapter-21) |
| Aversive signals and their costs | Zanette et al. (2011) | to verify | [19](#chapter-19) |
| Free-energy processing and organization | Krissansen-Totton, Bergsman and Catling (2016); Hopfield (1974); Toyabe et al. (2010) | to verify | [15](#chapter-15) |
| Bounds on the rate of physical processes | Margolus and Levitin (1998) | to verify | [6](#chapter-6) |

Every entry is verified against its source before its chapter is marked
final.

---

## D.9 Theses and conjectures (status C)

**Each claim states its quantifier and its domain, and what would count against
it is matched to that strength.**

Contrary evidence comes in three grades.
- **Certified contrary:** a fair comparison resolved against the claim, with
  the same sign, at every admissible level of detail tested. It counts against
  the claim, and the theory is revised to fit it.
- **Contrary at one level:** resolved against the claim at one level of detail
  or a few, unresolved or untested at the others. It is pressure, and it calls
  for the other levels.
- **Unresolved:** no verdict either way.

A claim that something can happen is not refuted by one case where it does not.
A claim that something always happens within a domain is refuted by one
certified case inside that domain.

| Claim | Quantifier and domain | What would count against it | Chapter |
|---|---|---|---|
| **The central thesis:** what we recognize as good corresponds to widening the whole field's futures, and what we recognize as harm to narrowing them | universal, over classes of cases in which our judgements are clear | a certified contrary result in a fair model: what we recognize as harm widening the whole field's futures, or what we recognize as good narrowing them | [11](#chapter-11), [32](#chapter-32) |
| Organized systems can reach, within the time available, futures that disorder does not | capability, in settings where an organized law opens a pathway that the same law without it cannot | certified results that, across the settings named, the organized law never raises the rate once the pathway's own dynamics are kept in the ablated arm | [13](#chapter-13) |
| A register without leverage does not outperform free variation | universal, under matched register conditions | none inside those conditions, where it is a theorem ([Proposition A.8.2](#a-8-2)); outside them, a fair model in which information without leverage widens the whole field at matched cost | [14](#chapter-14) |
| Constraint that blocks others' access to resources narrows the whole, even when it widens the futures of whoever imposes it | universal, over blocking of access with the blocked party coupled and no offsetting opportunity in the model | a certified result in which such blocking widens the whole field | [21](#chapter-21) |
| Obstructed suffering narrows what the same world, with the same valuer and obstruction, would keep open without it | universal, over obstruction that cannot be passed, with the valuer matched | a certified result in which the suffering arm is at least as lush as the drive-free arm; a contrary result at one level is pressure | [19](#chapter-19) |
| Organized enabling can raise the rate at which futures open in real systems | capability, in the real-system settings named in chapter 33 | certified real-system results in those settings in which no organized process raises it; a single failure is pressure | [15](#chapter-15), [33](#chapter-33) |
| A structure's contribution is its uptime times its excess branching | approximation, over the compounding family | the heavy-damage case, if the lead comes from partial structure that never forms a working loop; the form would then be indexed to partial structure | [15](#chapter-15) |
| Ethical judgement tracks the comparison with no index, and prudence the indexed one | part of the thesis, over cases where the two comparisons conflict | considered ethical judgement systematically tracking one frame's futures against the whole field's where they conflict | [10](#chapter-10) |

---

## D.10 What this map does not contain

- **Ledger codes and ruling numbers.** They belong in the working files and
  in [Appendix H](#appendix-h).
- **Results that have not been reported.** Batches run but not yet received
  are not listed.
- **A verdict on the thesis.** The map says what has been shown, how far it
  holds, and what is still open. [Chapter 31](#chapter-31) says what that
  adds up to, and [chapter 32](#chapter-32) says what could still overturn it.

## References cited in Appendix D

*Collected with full details in Appendix G.* Entries marked "to verify" in
section D.8 are not yet verified against their sources.

- Arrow, K. J., and Fisher, A. C. (1974).
- Cohen, D. (1966).
- Eigen, M. (1971).
- Henry, C. (1974).
- Hopfield, J. J. (1974).
- Kleidon, A. (2012).
- Kline, M. A., and Boyd, R. (2010).
- Kremer, M. (1993).
- Krissansen-Totton, J., Bergsman, D. S., and Catling, D. C. (2016).
- Kussell, E., and Leibler, S. (2005).
- Margolus, N., and Levitin, L. B. (1998).
- Ostrom, E. (1990).
- Paine, R. T. (1966).
- Ramírez-Ruiz, J., Grytskyy, D., Mastrogiuseppe, C., Habib, Y., and
  Moreno-Bote, R. (2024).
- Toyabe, S., Sagawa, T., Ueda, M., Muneyuki, E., and Sano, M. (2010).
- Wiser, M. J., Ribeck, N., and Lenski, R. E. (2013).
- Yachi, S., and Loreau, M. (1999).
- Zanette, L. Y., White, A. F., Allen, M. C., and Clinchy, M. (2011).
