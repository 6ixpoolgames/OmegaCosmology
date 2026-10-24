# Omega Cosmology v4.1: style sheet — r5

**Date:** 16 October 2026.
**Changes from r4:** terms for the foundation adopted on 16 October (one
premise, the ethical comparison, contraction and harm); canonical outline is
r5; "valuer" is a definition, no longer a pending one; the example of a result
resting on a premise no longer uses the retired valuing premise.

**Changes from r3:** "central thesis" replaces "central conjecture" (ruling
24); status C covers theses and conjectures; analogy rule restated; chapter 20
retitled; canonical outline is r4.

**Changes from r2:**
- One status per numbered result, with the sources of machinery listed
  separately (section 2).
- The chapter map is written out in full, with the canonical outline file
  named (section 6).

**Changes from r1:**
- Status vocabulary for formal results (section 2).
- A rule for results that rest on premises (section 2).
- The chapter map (section 6).
**Use:** read this sheet before drafting or revising any section, and again
after every context compaction. It applies to every chapter and appendix.
Where it repeats a standing ruling, the ruling governs.

## 1. Voice

The manuscript has one voice, after Parfit.

- **Plain declarative sentences.** Each claim is stated precisely enough to be
  wrong. A paragraph makes one step.
- **Explicit arguments.**
  - Arguments that carry weight are numbered.
  - Their premises are named and listed.
  - The text says which premise does the work.
- **Objections at full strength.** An objection is stated in its best form
  before it is answered. If it is not answered, the text says so.
- **Worked examples, never analogies.** No comparisons across domains either:
  do not set the case under discussion beside another to show that it is "the
  same" (restated 16 October). An example is a specified physical
  model with numbers that can be recomputed (Appendix B). Thought experiments
  are allowed only when they can be written as such a model.
- **No ornament.**
  - No rhetorical questions used in place of arguments.
  - No "clearly", "obviously", "of course", "profoundly" or "deeply".
  - Short memorable lines appear only when they clarify. The only approved
    aphorism is: "If your internal state cannot influence the world, might as
    well dream."
- **Person.**
  - "We" for the reasoning ("we now show").
  - "The program" for the research enterprise.
  - "This manuscript" for the text. Never "I", and never "the book".
- **Terms.** A technical term is defined at its first use and keeps exactly
  one sense afterwards.

## 2. Status

Every substantive claim has one of six statuses. In prose, the status is
carried by the verb.

| Status | What it is | Verbs and forms allowed |
|---|---|---|
| D, definition | a stipulation | "we define", "is defined as" |
| T, theorem | proved in Appendix A, or cited with a source | "proves", "it follows", "Theorem A.4.2 shows" |
| M, model result | shown in a named model, within its scope | "in model C.n, …", "the model shows"; never "proves", "establishes" or "demonstrates" without the model's name |
| E, empirical correspondence | observed in published work | "corresponds to", "is observed in", with a citation |
| N, normative premise | assumed, and named | "we assume", "the [name] premise" |
| C, thesis or conjecture | a thesis is asserted and defended; a conjecture is proposed without yet being asserted; either can lose | "the central thesis", "we hold", "we conjecture"; always with what would count against it |

- **Status tables.** Every chapter ends with a status table listing its
  claims under these six labels.
- **Firewalls.**
  - A model result bears on a thesis or conjecture only through a sentence that says how
    far it bears.
  - The subject distinction never licenses an ethical conclusion by itself.
- **Formal results (Appendix A and chapters citing it).** Every formal result
  carries one of these statuses:

  | Status | Meaning |
  |---|---|
  | established elsewhere | proved in the literature; outlined or proved here, with the source |
  | proved here | proved in Appendix A under its stated assumptions |
  | conditional on physical premises | proved given named physical hypotheses, which are not proved |
  | conditional on a normative premise | proved given a named normative premise, which does the normative work |
  | analytical model with stipulated payoffs | algebra in a decision model whose gains and losses are stipulated, not computed by the measure |
  | definition | a stipulation |
  | adopted | a methodological choice |

- **One status per result.** Each numbered result carries exactly one
  status. The literature a proof draws on (its machinery) is cited separately
  and does not change the result's status.
- **Results that rest on premises.** State the premise in the sentence that
  uses the result. Write "given the physical premises F1–F3, a credence below
  the threshold cannot outweigh the largest available gain", never "the
  measure proves the threshold". In Appendix A r7 no result rests on a normative premise. The one
  normative claim is the central thesis (status C).
  Report a stipulated-payoff model as a property of that model, never as a
  theorem of the measure.
- **Pending decisions.** Text that depends on an open decision carries a
  bracketed marker in the draft (for example [P4]). Markers are removed once
  the originator decides.

## 3. Terms

| Use | Do not use |
|---|---|
| program, manuscript | project; book (in the text) |
| central thesis | central conjecture; wager |
| lushness L = 2^ℓ; log lushness ℓ, in bits | breadth as a defined term |
| rate h, offset b, crossover horizon T× | gain, bias (except when citing dynamic programming) |
| expected persistence E[N]; hazard λ; generative window | lifetime, survival as defined terms |
| model C.n (Appendix C) | adapter numbers, experiment code names |
| the premise (value requires valuers); the ethical comparison (Definition A.7.8) | axioms, for the foundation; impartiality as a premise |
| contraction, expansion (descriptive; Definition A.9.2) | negative value or disvalue as a quantity |
| harm, benefit (evaluative: whole-field contraction and expansion, by the central thesis) | harm as a defined physical quantity |
| foreclosure (Definition A.9.3), reported beside contraction | foreclosure as a synonym for contraction |

- **Lushness in prose.** "Lushness" may be used for ordinal comparisons, since
  L and ℓ rank developments the same way. Every number quoted is log lushness
  in bits.
- **Valuer** (definition): any subject in the sense of Definition A.7.1, a
  physically specified subsystem. The term implies neither experience nor
  agency. No kind of process is excluded.
- **Persistence.** "Metavalue" means that the persistence of valuing is a
  condition of every value not yet realized. In the measure, persistence is
  worth the rate it sustains beyond what would replace it (Proposition A.4.8).
  Never present persistence as valuable in itself.
- **Kept out of manuscript text:** ledger codes (A17, C5), ruling numbers, and
  the word "originator". They belong in the working files and in Appendix G.

## 4. Mathematics

- **Units.** Logarithms are base 2, so entropies are in bits.
- **Notation.** The notation is fixed in section A.1 and used everywhere. The
  core symbols:

  | Symbol | Meaning |
  |---|---|
  | K | kernel |
  | g | step entropy |
  | ℓ_n | log lushness |
  | Π | Cesàro limit |
  | Z = (I − K + Π)⁻¹ | fundamental matrix |
  | h = Πg | rate |
  | b = Z(g − h) | offset |
  | T× = −Δb/Δh | crossover horizon |
  | N, λ | random horizon, hazard |
  | H, h₂ | entropy, binary entropy |

- **Boxed results.**
  - A result's statement is set as a blockquote containing the display.
  - It is followed by a line beginning *In words:*, written without symbols.
  - Every boxed equation has an In words line.
- **Display math.** \[ … \]. Inline math in plain Unicode where it is
  legible (ℓ_n, Δh, T×).
- **Appendix A numbering.** Results are numbered within their section, with
  one counter for all kinds: Definition A.3.1, Lemma A.3.2, Theorem A.3.3,
  and so on.
- **Parts of a result.** Each result gives:
  - its assumptions, where they go beyond the standing ones;
  - the statement;
  - the In words line;
  - a proof, or the source with an outline of the proof;
  - its scope.

  A **conditional proposition** rests on physical premises. The premises are
  named and are not proved.
- **Chapters do not prove.** They state results in words, cite them ("Theorem
  A.4.2") and show a worked example.

## 5. Citations

- **Author–year,** for example (Cover and Thomas 2006). Up to three authors are
  named; four or more are "first author et al.".
- **Pinpoints** (theorem, page or section numbers) are given only when they
  have been checked against the source. Otherwise, cite the chapter or the
  whole work.
- **Reference lists.** Every chapter ends with "References cited in this
  chapter", and Appendix F collects them all. Each reference is verified before
  its chapter is marked final.

## 6. Chapter structure

1. **An opening paragraph** stating what the chapter claims, with what status,
   and what it does not claim.
2. **Numbered sections,** n.1, n.2, ….
3. **A status table,** then the references.

Cross-references take the forms "chapter 5", "section 5.3", "Theorem A.4.2"
and "Appendix C".

**Chapter map.**
- **Canonical file:** /home/claude/v41/V41_OUTLINE_r5.md.
- **Status:** the map is frozen once the originator confirms it. From then
  on:
  - the old 00–14 rewrite map in the program review is superseded;
  - renumbering requires a recorded decision.

| Part | Chapters |
|---|---|
| Front matter | preface; the argument in brief |
| I. The object | 1 What follows from a present; 2 Frames, access and information; 3 Composition and intertwined futures |
| II. The measure | 4 Lushness; 5 Horizon, rate and offset; 6 Resolution and grain; 7 Subjects of the measure; 8 What the measure compresses |
| III. Mechanisms | 9 Reading the test bed; 10 Access that disorder cannot reach; 11 Information through action; 12 Persistence: structure pays when it lasts; 13 Compounding; 14 Organization against disorder; 15 Activity and productivity |
| IV. Value | 16 From measure to value; 17 Protection; 18 Harm, recovery and irreversibility; 19 Suffering; 20 The central thesis |
| V. Many | 21 Coupled futures and joint access; 22 Constraint and domination; 23 Justice, forgiveness and virtue; 24 Persons, populations and minds |
| VI. Action | 25 Choosing inside the structure; 26 Windows, rates and the price of robustness; 27 Uncertainty, correction and precaution; 28 Controllers as field-altering nodes; 29 Alignment |
| VII. The whole | 30 Alpha, Logos and Omega; 31 Completion, choice and what the account means |
| VIII. Evidence and program | 32 The evidence, surveyed; 33 What would decide it |
| Appendices | A Formal core; B Worked examples; C Test-bed methods and model catalogue; D Evidence map; E Glossary; F References; G Provenance |

## 7. Files and workflow

- **Local drafts:** /home/claude/v41/ms/.
  - Chapters: `NN_SHORT_TITLE_r#.md` (01–33).
  - Front matter: `00_FRONT_MATTER_r#.md`.
  - Appendices: `A_FORMAL_CORE_r#.md`, `B_WORKED_EXAMPLES_r#.md` and so on.
- **Scripts.** Every number in the manuscript is produced by a script under
  /home/claude/analysis/. Appendix B lists the script for each example.
- **Order of work for each chapter** (Sol, 16 October):
  1. draft;
  2. audit the status table;
  3. check every theorem citation against Appendix A;
  4. check every model claim against Appendix C and the evidence map;
  5. adversarial review;
  6. send to the originator;
  7. upload once approved.

  Watch especially for three translation errors:
  - a theorem becoming a universal physical claim;
  - a model result treated as evidence beyond its scope;
  - a normative premise missing from the sentence that uses it.
- **Drive.**
  - The v4.1 folder: 1XmZONm5t-ebBBdUhRBZ6padXlOycjkli.
  - Its deprecated folder: 18rCjxLRkoMMFSgD_YRbRqeD2alWNo9T7.
  - Upload with r# in the filename and check the Drive file size against the
    local byte count.
  - Superseded files go to deprecated, on Drive and in /home/claude/deprecated.
- **Repository.** Nothing is committed or pushed to the repository without the
  originator's explicit instruction.
