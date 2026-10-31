# K — retained-figure audit

31 October 2026. Completed locally on the user's “Proceed”. No simulation,
new history calculation, manuscript amendment, commit, upload or push.

The ten private working drafts supplied with request r7 were inspected against
the retained R1, R1-M, R2, E1, S3, S4 and S4b evidence. They are not imported as
canonical manuscripts. This report paraphrases findings and gives file/line
locators; it does not reproduce private prose. Input hashes, not private text,
are in [SOURCE_INPUTS.json](SOURCE_INPUTS.json).

## Result

**The checked headline numbers survive. Several statements about their scope
need correction.** [NUMERICAL_CHECKS.json](NUMERICAL_CHECKS.json) records 124
retained-value, rounding and independently recounted signed-row assertions;
all 124 agree. Seventeen numerical source files were checked against their
pre-existing evidence manifests. This is an audit of transcription and scope,
not independent experimental replication or a rigorous rounding certificate.

The most important error is a claim of no negative interval at cadence .5:
the full retained activity comparison has three crossings at that cadence,
just as it does at .125 and .25. Checking four endpoint horizons missed this.

## Corrections for the drafting instance

Locations refer to the unmodified, hash-identified private drafts in the packet.
The proposed corrections below are not applied to those drafts.

| ID | Location | Finding and necessary correction |
|---|---|---|
| K01 | Chapter 10 r3, lines 692–703; Appendix C r1, lines 714–722; Appendix D r1, lines 266–270 | Distinguish the four printed endpoints from the intervening profile. At cadence .5 all four endpoints are positive, but the retained prefix has three crossings. A claim of never trailing is false. See the brackets below. The analogous Appendix C/D wording needs an explicit endpoint qualifier. |
| K02 | Appendix C r1, lines 725–730; chapter 10 r3, lines 697–699 | With the source off, the comparison reuses the source-on fitted conductance and is **not activity matched**. At .25, its positive T1024 difference is +30.671642 bits, but its rate difference is −.014045941 bits/time. The finite lead is not an offset-only comparison: it contains rate, bias and transient contributions. This diagnostic does not isolate a source-dependent effect at fixed activity. |
| K03 | Chapter 10 r3, lines 692–703; Appendix C r1, lines 722–724; Appendix D r1, line 264 | Matching is numerical, not exact arithmetic. The stationary event-rate residual is −8.3267e−17 events/time. The **sign** of the source-on rate contrast agrees across the three tested cadences; its magnitude changes (+.013063, +.014344, +.016027 bits/time). Specify sign stability rather than cadence independence of the rate itself. |
| K04 | Chapter 10 r3, lines 684–688; chapter 12 r10, lines 445–450; Appendix C r1, lines 691–698 | The load has no direct bank-charging, construction or useful-unlocking step. That does not show it changes no access or function indirectly. Its native reverse, occupancy changes and existing basal/capture routes remain. Describe the direct relaxation mechanism instead of assigning it no consequential effect. The work match is stationary **net external work**, not equal finite dissipation, gross input or source histories. |
| K05 | Chapter 18 r11, lines 175–182; Appendix D r1, lines 812–820 | S3 repair contains **four unique laws and eight law/cadence cases**, not eight unique laws. The approximate 17–26 bit range needs cadence .25 stated; its actual T4096 range is 16.992979–26.488814 bits. Across all tested cadences the range is 16.992979–30.432491. T1024 is a physical duration: at cadence .25 it is 4096 sampled steps. Do not call it the thousandth sampled step or an exact settling time. |
| K06 | Appendix C r1, lines 681–687 and 1868–1869 | Publication metadata is stale. P0/T, paired qualification r2 and R1-M are published in 90baf70. Use their retained repository locations. No new upload or replay is required. |
| K07 | Appendix C r1, lines 441–450 | E1 has **45 laws in total**, comprising 40 supplied laws plus five source-off laws; 65 law/cadence cases result from the extra cadence checks. Clarify that source-off is included in 45, rather than additional to it. The quoted 650 profiles and 1935 contrasts are correct. |
| K08 | Appendix C r1, lines 333–334 and 719–721; Appendix D r1, lines 247–249 | For R1's selected mechanism contrast and the source-on net-work comparison, no crossing is observed on the evaluated prefix. The retained float64 Poisson/bias calculation is not a verified-rounding all-horizon certificate. Qualify unbounded no-crossing wording accordingly. Nothing here disputes the positive computed limiting rates. |

K01 changes a factual statement about the retained finite profile. K02–K05 and
K08 correct inference, matching, units or scope rather than reverse a printed
headline number. K06 is editorial provenance. K07 resolves a count ambiguity.
These are not new failures of a theory or of a physical qualification gate.

## Full-profile information that must accompany the four endpoints

Productive minus the source-on activity-matched control:

| Cadence | Observed crossing brackets, physical time | Four endpoints T16/64/256/1024 |
|---|---|---|
| .125 | [3.125,3.25], [51.25,51.375], [406.875,407] | +, −, −, + |
| .25 | [2.25,2.5], [63.25,63.5], [294,294.25] | +, −, −, + |
| .5 | [1,1.5], [102.5,103], [161.5,162] | +, +, +, + |

For a direct retained witness, at T124 and cadence .5 the difference is
−.102226044831 bits, despite the four headline endpoints being positive.

These are sampled-step sign brackets already retained in run A, not newly
root-found continuous-cadence or continuous-horizon crossings. In particular,
the .5 profile has a negative interval between the second and third brackets.
There is also an initial negative interval before its first crossing. All
three cadences have positive computed excess rates while the source is on.

## Verified numerical groups

| Group | Retained result checked |
|---|---|
| R1 | 144 profiles/240 contrasts; 72/72 positive mechanism rows; one cadence-flip group; preparation +5.78/+33.26 bits at T16/T1024, .25; selected replay and rate |
| R1-M | 96 rows/72 contrasts/72 paired passes; both four-horizon tables and all six source-on rate differences; source-off T1024 and rate; all three crossing sets |
| R2 | 216 profiles/396 contrasts; capacity and assistance each 72/72; no cadence flips, nine horizon-flip groups; selected replay +.03/+2.01/+27.94 bits at T16/T64/T1024, .25, and rate |
| E1 | 650 profiles/1935 contrasts; T4096/.25: local whole 18/18, local parts 36/36, cross whole 90/90, part intervals 108 positive/72 unresolved, reciprocity 6 positive/12 negative, preparations 30 positive/15 negative; 1 cadence/44 horizon flips; selected replay and rate |
| S3 | 168 profiles/254 contrasts; 80/80 fault-versus-intact positives; 360 zero foreclosure weights; four repair-fault contrasts; early +.926 whole and A[−.656,−.060], B[+.794,+1.357]; selected replay and rate |
| S4/S4b | Each 192 profiles/192 contrasts; each response contrast 48/48 positive; blocked +9.49/+18.45 bits at T1024/.25; 0/11 cadence-flip groups and 24/23 horizon-flip groups; S4b four endpoint interactions; both selected replays and rates |
| P0/qualification | 252 replayed rows, 61 headline rows, zero observed reproduction differences, 14 scoped paired checks; applicability remains separate from literal old inputs |

The detailed JSON selectors identify the arms, preparations, cadence, horizon,
quantity and denominator. A count of comparison rows is not a count of
independent regimes. Replayed headline contrasts are not replays of every row
elsewhere in their parent studies. The source-off diagnostic and adverse
intermediate signs remain part of the evidence.

## Coverage and unresolved questions

All ten supplied drafts were inspected for the named current-platform material.
Appendix C's seven current entries, Appendix D's current rows in D.3.1–D.3.6
and D.5, and the corresponding chapter passages were reviewed. The private
locator inventory was kept under ignored `.local/`; [REVIEW_COVERAGE.json](REVIEW_COVERAGE.json)
contains source locations and categories without manuscript text.

No numerical current-platform figure was left with no retained source among
the passages reviewed. This does **not** audit historical C.1–C.17 numerical
claims, external physiological literature, Appendix A proofs, bibliographic
metadata, or the whole manuscript's cross-reference numbering. Chapters 14 and
16 do not supply new current-platform numerical tables; their conceptual
claims are not made empirical by this audit. Existing tentative tiers do not
establish a finest faithful physical grain. The separate evidence axes and
the qualification limits must remain alongside any tier label.

No manuscript changes are applied, and no mechanism result is promoted to
physical faithfulness, ancestry, robust compounding, phenomenal valence or
ethical correspondence. The private latest Appendices A and B are not in
this packet; this is not a new conformance review of them.

## Reproduction

From the repository root, using its Python environment, execute the retained
[audit script](analysis/audit_retained.py) with `--packet` pointing to the
author-supplied r7 ZIP and `--out` pointing to a fresh ignored directory.
It reads JSON and computes counts/differences only; it imports no simulator,
compiler, kernel solver or history scorer. It verifies numerical sources
against their existing evidence manifests and writes no private text. The
manual reading/interpretation component is identified separately in this report.
