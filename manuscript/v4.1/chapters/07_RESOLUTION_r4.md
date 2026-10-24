# 7. Resolution: what counts as different

> **Drafting note (r4, 23 October).**
> - Ruling 79: matched resolution first; a finer level governs only once
>   shown faithful (Appendix A r19, Definition A.6.5).
>   - **7.3:** new paragraph on matched resolution; the refinement governs
>     once shown faithful; why the finer of two faithful levels (the step
>     chapter 10 meets for subjects); the box example cites section 7.2 for
>     the chamber grain's faithfulness. Definition 7.2 amended.
>   - **7.4:** four verdicts, adding the resolution-dependent reversal.
>     Definition 7.3 amended.
>   - **7.6, 7.7, 7.8, 7.9** and the status table follow.
>   - TL;DR: headline and the second and third bullets.

> **Drafting note (r3, 23 October).**
> - Sol's review of r2 (ruling 77). Structure, examples and TL;DR kept.
>   - **The crossover is not guaranteed** (7.5, Definition 7.4; Corollary
>     A.6.4 in Appendix A r18). The leading terms always tie somewhere; that
>     estimates a scale, and whether the full counts cross has to be found
>     from them. Two random switches at different rates never cross, though
>     their leading terms tie.
>   - **Formation time is not timing resolution** (7.6). The criterion is
>     whether the record histories, or what follows them, physically differ
>     with the timing; how long a record takes to form does not settle it.
>   - **Possible records** are those in physically reachable histories, not
>     any instrument that can be described (7.6, In Omega).
>   - **7.7:** "Every frame records less than the whole" becomes "Frames
>     that form records typically register only part of the whole" (chapter
>     3 does not require frames to keep records).
>   - **Example 7.3** states the switch's rate (0.25 flips per time unit)
>     and the system's rotation (one radian per time unit).
>   - **7.3:** that the fullest faithful description governs is stated as
>     the program's rule, physically motivated, not a theorem of physics
>     (Sol's second message). The law in question is the native law; where
>     it comes from is mentioned only in passing, with a pointer to the
>     cosmology (ruling 77: Alpha stays out of the TL;DR and is mentioned at
>     most in passing outside Part VIII).

> **Drafting note (r2, 23 October).**
> - After the originator's Zeno point and Sol's two reviews (ruling 76):
>   - **Section 7.6** is rebuilt around three things kept apart: the physical
>     development, the physical records, and the analyst's sampling. What
>     physics limits is recordable timing information; a sharp floor is one
>     possible result, not an assumption. The Margolus–Levitin bound is
>     stated as a limit on evolution toward orthogonal states, not as a
>     floor. The short-time onset of quantum transitions is named.
>   - **Example 7.3** (new): a recorded two-level system against a passively
>     read random switch. It is presented as the entropy of the records of
>     different measurement protocols, not as a refinement and not as a
>     bound on the whole field.
>   - **Whether finer recording pays** is an option comparison, the
>     apparatus and its costs included, after the originator's note.
>   - **Section 7.3:** refinement relates passive descriptions of one
>     development; the joint grain is Corollary A.6.7, for compatible
>     histories, with the quantum limitation stated.
>   - **Section 7.5:** the expansion is stated for random waiting times.
>   - TL;DR: the last bullet replaced.
> - Appendix A r17 carries the matching changes (Theorem A.6.3, scope;
>   Definition A.6.5; Corollary A.6.7; verifications V48 and V49).

> **Drafting note (r1, 23 October).**
> - First draft, following outline r19 (chapter 7) and the concept ladder
>   (faithful resolution; the governing level; certified and corrected
>   rankings; unresolved), in the form of rulings 63–69 and 72: a headline
>   and takeaways with no toy results, claims stated as strongly as they can
>   be defended, qualifications argued in the body.
> - **Sources:** outline r19; Overview r19, section 3 ("What counts as
>   different", "Physics decides what counts as the same"); Appendix A r16,
>   section A.6 (Definition A.6.1 to Proposition A.6.6) and section A.15
>   ("The governing resolution"); chapter 4 r5, section 4.2, which leaves two
>   questions to this chapter: descriptions neither of which refines the
>   other, and the floor on cadence; chapter 12 r8, section 12.5.
> - **For approval (ruling 15).** Section 7.3 argues that two faithful grains
>   neither of which refines the other have a faithful common refinement,
>   which governs both. It follows from Definition A.6.5 in a few lines but is
>   not yet a numbered result. Proposed as Corollary A.6.7 in Appendix A r17.
>   The chapter cites Definition A.6.5 until then.
> - The Overview's section 3 still describes the retired rule ("accept only
>   robust verdicts ... at every admissible resolution"). It is on the held
>   r20 list; this chapter follows Definition A.6.5.
> - Script: `analysis/ch7/ch7_numbers.py` computes the box, relay and
>   molecule numbers by exact enumeration and matrix exponentials, and the
>   Margolus–Levitin times. The verification counts in 7.4 are Appendix A's
>   V47.
> - The drafting notes are working provenance. They are removed at
>   compilation and kept in the revision record (Appendix H).

> **TL;DR**
>
> Physics decides which differences count, and options are compared at one
> level of detail. A ranking that flips with the level of detail is not a
> stalemate: the flip shows where the difference comes from, and the finer
> level settles it once its extra detail is shown to be physical.
>
> - **A distinction counts only if physics can register it.** It counts if a
>   record of it can form, or if it changes what later records show.
>   Renaming, duplicating and idle checkpoints draw no distinction.
> - **Compare at one level; the finer faithful level governs.** More detail
>   alone settles nothing. The fullest faithful description, the judgement
>   of the ultimate frame, is the target.
> - **A coarse verdict can be certified, corrected or left open.** It stands
>   when it exceeds the most the omitted detail could add. A reversal counts
>   as a correction only at a level shown to be faithful.
> - **Read finely enough, the busiest process wins.** For random events, each
>   finer digit of timing adds bits in proportion to the number of events, so
>   which timing differences count has to come from physics.
> - **Timing counts only as finely as physics can record it.** A clock is a
>   physical system, and a finer one can change what it measures. Whether
>   finer recording is worth its cost is a choice like any other.

Chapter 4 counted futures at a declared resolution and left two questions
open: which of several faithful levels of detail governs a comparison, and
where the floor on cadence comes from. This chapter answers both, as far as
they can now be answered, and develops the part of
[Overview section 3](#overview-3) that concerns what counts as different.
Its results are definitions and theorems of [Appendix A](#appendix-a),
section A.6. What the most complete faithful description of a given model
is, and how much timing information its records can carry, are not yet
derived for any model; section 7.6 says what is known.

---

## 7.1 Rankings that move

**The same two options can trade places when the level of detail changes.
That is a fact about the measure, and it needs a rule.**

A resolution has two parts: a grain, which says which states count as
different, and a cadence, which says how often the development is read
(chapter 4). A coarser grain can only hide branching; it cannot create it
([Proposition A.6.2](#a-6-2)). But it can hide more of one option's
branching than of another's, and then the ranking reverses.

**Example 7.1: a box with a pocket.** A box is divided into four chambers,
and a small pocket opens off the fourth. A molecule sits in the fourth
chamber. Two options act on the doors.
- **Open the partitions, seal the pocket.** The molecule moves among the four
  chambers, landing in each with equal probability at every step.
- **Close the partitions, open the pocket.** The molecule moves between the
  fourth chamber and the pocket, landing in each with equal probability at
  every step.

| Over 10 steps | Partitions open | Pocket open |
|---|---|---|
| Read by chamber | 20 bits | 10 bits |
| Read only as box or pocket | 0 bits | 10 bits |

Read chamber by chamber, opening the partitions keeps more open. Read only
as "in the box" or "in the pocket", it keeps nothing open, and the pocket
option leads. Neither reading is mistaken arithmetic. Something has to say
which one decides.

> **Primer: coarse-graining and entropy**
>
> A coarse description is a function of a fine one: each fine state is
> assigned to one coarse state. A function of a random quantity has no more
> entropy than the quantity itself, and the difference is the entropy of the
> fine detail given the coarse (Cover and Thomas 2006, chapter 2). Applied to
> histories, a coarse history never carries more branching than the fine
> history it summarizes. Which of two options loses more under the summary
> depends on where each one's branching lies.

---

## 7.2 What counts as a difference

**A distinction counts only if physics can register it.**

The first rule removes distinctions that are not there. A distinction
between states, or between the times at which changes occur, is faithful if
a physical record of it can form, or if it changes the law of later records
([Definition A.6.5](#a-6-5)). Three operations draw no faithful distinction
at all: renaming histories, splitting one history into duplicates, and
inserting checkpoints that change no transition
([Proposition A.1.2](#a-1-2)). A count of futures that changed under any of
them would be counting the description, not the world.

> **Plain-English definition 7.1: Faithful distinction**
>
> A difference between states, or between the times at which changes occur,
> that physics can register: a record of it can form, or it changes what
> later records show.

A faithful grain draws only faithful distinctions, and it keeps the
relations the physics of the case depends on: what acts on what, what is
conserved, which alternatives are open, which recoveries are possible, and
the difference between the continuations the comparison is about. In the
box, the chamber the molecule occupies is faithful: the molecule's position
can leave a record, and it decides which chambers it can reach next. So both
readings of Example 7.1 are faithful. The first rule does not settle the
example. The second does.

> **In Omega**
>
> A faithful distinction is one that Omega itself contains: two branches
> that differ in a way physics records. A resolution decides how many of
> those differences a reading shows, never whether they are there.

---

## 7.3 The finer description governs

**Options are compared at one level of detail. Of two faithful
descriptions, one finer than the other, the finer governs, because it leaves
out less of what happens; its extra detail has to be shown physical, not
assumed.**

**Matched resolution first.** A comparison ranks both options at one
declared resolution: the same grain, the same cadence and the same horizon,
from the same present. A difference between one option read finely and
another read coarsely measures the readings as much as the options, and it
is not a ranking. Every table in this chapter compares options within a
row.

One resolution refines another when the coarser history can be computed from
the finer one: the coarser cadence is a whole multiple of the finer, and the
coarser grain merges states of the finer grain. Refinement relates two
passive descriptions of one development; a reading made by a physical
apparatus is part of the development, and section 7.6 returns to it. Of two
resolutions, one refining the other, the refinement governs the comparison
once it is shown to be faithful: each distinction it adds has to pass the
test of section 7.2 ([Definition A.6.5](#a-6-5)). Greater detail alone
decides nothing. Section 7.5 shows why the test is needed: a finer passive
clock adds bits without limit, and would hand every verdict to the busiest
process. The coarser level is not wrong. It omits
distinctions that physics registers, and the comparison is about what
physically happens. This is the program's rule, not a theorem of physics.
Physics says what a finer description contains that a coarser one omits;
that the fuller description should decide is the program's commitment, made
because the measure is meant to read what physically happens, and testable
by where it leads. Which distinctions physics registers is settled by the
native law of the world in question. Where that law comes from is a question
for the program's cosmology ([chapter 28](#chapter-28)); nothing in this
chapter depends on the answer.

Why the finer of two faithful levels, and not the coarser? Ranking at the
coarser level treats as the same two histories that physics tells apart.
That adds a criterion of sameness the physics does not contain. Chapter 10
meets the same step when it asks whose futures a comparison counts.

In Example 7.1, the chamber-by-chamber reading refines the box-or-pocket
reading, and both are faithful: section 7.2 showed that the chamber can
leave a record and decides which chambers the molecule can reach next. The
chamber reading governs: opening the
partitions keeps more open, by 10 bits over 10 steps. The coarse verdict is
corrected, and it is kept on record, because it says where the pocket
option's lead came from: every bit of it is a crossing between box and
pocket. The chamber reading counts those crossings too, together with the
moves among chambers that the coarse reading cannot see.

Taken to its end, the rule names a target. The most complete faithful
description of the whole field is the one that omits nothing physics
registers. It is the reading of the ultimate frame, the whole world taken
as a frame (chapter 3). Every level of detail we compute approximates it,
and a ranking is as reliable as its approximation.

> **Plain-English definition 7.2: The governing description**
>
> Of two faithful descriptions, one finer than the other, the finer, once
> its extra detail is shown to be registered by physics. The fullest
> faithful description, the reading of the ultimate frame, is the target
> that every computed level approximates.

**When neither description refines the other.** Two faithful grains can
each keep information the other drops: one records which chamber the
molecule is in, another records its speed. Neither can be computed from the
other. They still have a governing description. Distinguish two states
whenever either grain does. Every distinction this joint grain draws is
drawn by one of the two, so it is faithful; it keeps every relation either
keeps; and it refines both. So it governs both, and each of the two is a
coarser approximation of it ([Corollary A.6.7](#a-6-7)). Two faithful
cadences that are whole multiples of a third faithful cadence are both
refined by it. The result needs the two descriptions to belong to one
history. Quantum records made by incompatible instruments need not, and
then no joint description exists ([chapter 29](#chapter-29)).

> **In Omega**
>
> Omega does not change with the resolution. The governing description is
> the reading of Omega that loses least of it, and coarser readings are
> judged by how much of the difference between two options they keep.

---

## 7.4 Checking a coarse verdict

**A ranking found at a coarser level stands when the most the omitted detail
could add cannot reverse it.**

Computing the governing description is often out of reach. A coarser
ranking can still be relied on, because refining a description adds to each
option exactly the uncertainty of the new detail given the old
([Proposition A.6.6](#a-6-6)).

> \[
> \ell'=\ell+H(W\mid V,X_0=x),\qquad
> \Delta'\ \ge\ \Delta-H_b(W\mid V,X_0=x).
> \]
>
> *In words:* the finer level's lushness is the coarser level's plus the
> uncertainty of the extra detail, so a coarse lead of one option over
> another survives refinement whenever it is larger than the most the extra
> detail could add to the option behind.

Four verdicts follow, and every ranking in the manuscript carries one.
- **Certified.** A bound on what the finer level could add to the trailing
  option is smaller than the coarse lead. The ranking holds at the finer
  level without computing it.
- **Corrected.** A finer level, shown to be faithful, reverses the
  ranking. The finer level decides, and the coarse ranking is kept as a
  record of where the difference comes from.
- **Resolution-dependent.** A finer level reverses the ranking, but whether
  its extra detail is physical has not been established. Both rankings are
  reported, each with its level of detail and with the detail that carries
  the reversal. Neither decides.
- **Provisional.** The ranking holds at the finest level computed, and has
  been neither certified nor corrected beyond it. Both sides of a
  resolution-dependent reversal are provisional.

> **Plain-English definition 7.3: Certified, corrected,
> resolution-dependent, provisional**
>
> A coarser ranking is certified when what a finer level could add cannot
> reverse it; corrected when a finer level shown to be faithful reverses
> it; resolution-dependent when a finer level reverses it and that level's
> faithfulness is open; and provisional when none of these has settled it.

**Example 7.1, continued.** Add a third option: shut every door, so the
molecule stays in the fourth chamber. Against it, the pocket option leads by
10 bits over 10 steps at the box-or-pocket level. Does the lead survive the
chamber-by-chamber reading?
- The general bound counts how many finer states each coarse state merges.
  Here the box merges four chambers, so the bound allows up to 20 bits of
  extra detail. That exceeds the 10-bit lead, so the counting bound does not
  certify it.
- The law gives a tighter bound. With every door shut, the molecule is
  always in one chamber, so the extra detail adds nothing to the shut option.
  The lead is certified, without computing the finer level.

Set against the partitions option instead, the pocket option's 10-bit lead
faces an option whose chamber detail adds 20 bits, and the lead reverses.
That ranking is corrected, as section 7.3 found.

The counting bound is crude but not idle. In 2,000 random pairs of small
laws, it certified 60 coarse rankings, and none of them reversed at the
finer grain ([Appendix A](#appendix-a), verification V47). The same
structure certifies a finite horizon's ranking against what lies beyond it
([Proposition A.12.1](#a-12-1)): there the omitted part is later time, here
it is finer detail.

---

## 7.5 Time: a finer clock favours the busy

**Read finely enough, the option with more events always leads. The cadence
therefore cannot be left free.**

Cadence raises a problem that grain does not. Every finer reading of the
clock adds a digit to when each event happened, and that digit is a
branch. It adds no events: it distinguishes more finely when the events
occurred. For a process in continuous time whose events come after random
waiting times, read at cadence τ over a horizon T, the count splits into two
parts ([Theorem A.6.3](#a-6-3); Gaspard and
Wang 1993).

> \[
> \ell_T(\tau)=\bar N(T)\,\log_2\frac1\tau+F(T)+o(1).
> \]
>
> *In words:* read finely enough, a process's lushness is the expected
> number of events it produces, times a term that grows without bound as the
> clock gets finer, plus a finite term set by which events happen and how
> unevenly.

The first term does not depend on the unit of time; a change of unit moves
lushness between the two terms and leaves the total unchanged. The
consequence for comparisons is direct. Of two processes, the one with more
events leads at every fine enough cadence ([Corollary A.6.4](#a-6-4)). At
coarser cadences the other can lead, if its events are more varied, and
then the two counts cross. The leading terms always tie at some cadence,
which estimates where a crossing would lie. Whether the counts actually
cross has to be found from the counts themselves. Two random switches that
flip at different rates show why: their leading terms tie at about 0.21 time
units, yet the faster switch keeps at least as much open at every cadence,
and the two draw level only when both are read so rarely that each reading
looks random.

> **Plain-English definition 7.4: Crossover resolution**
>
> The cadence, where there is one, at which the counts of a busier process
> and a more varied one cross. Read more finely, the busier one leads; read
> more coarsely, the more varied one can.

**Example 7.2: a relay and a wandering molecule.** Two processes run for the
same time, measured in nanoseconds.
- **A relay** clicks between two positions, about ten times a nanosecond.
- **A molecule** hops among sixteen binding sites, about once a nanosecond,
  to any other site with equal probability.

| Cadence (ns) | Relay (bits/ns) | Molecule (bits/ns) | Leader |
|---|---|---|---|
| 1 | 1.00 | 3.36 | molecule |
| 0.5 | 2.00 | 4.95 | molecule |
| 0.2 | 5.00 | 6.92 | molecule |
| 0.1 | 9.87 | 8.23 | relay |
| 0.01 | 43.86 | 11.93 | relay |
| 0.001 | 80.13 | 15.31 | relay |

Read every half nanosecond, the molecule keeps more open: each reading finds
it at one of sixteen sites, and the relay at one of two. Read every
hundredth of a nanosecond, the relay leads nearly four to one, because almost
all of its count is now the timing of its clicks. The two tie at a cadence
of 0.128 ns. The leading terms of the expansion put the tie at 0.156 ns;
near the crossover the remainder still matters, so its exact place is found
at the actual cadence.

Without a physical criterion for timing, this settles every comparison the
same way: refine the clock far enough and the busier process wins, whatever
else either does.
That would make lushness a count of events. It is also the formal root of
the objection that the measure rewards activity, which
[chapter 16](#chapter-16) takes up at full strength.

---

## 7.6 Timing counts only as finely as physics records it

**A timing that no record can register is not a faithful distinction. What
physics limits is the timing information a system can record, and a clock
is itself a physical system.**

Three things have to be kept apart.
- **The physical development:** which events can happen, when, and with what
  probabilities.
- **The physical records:** which differences in that development can be
  registered, including differences in when events occurred.
- **The analyst's sampling:** how often someone chooses to compute or
  inspect a model.

Only the first two fix what Omega contains. The third creates no
possibility: reading a model more often adds nothing to the world unless
the reading is itself a physical process, and then it belongs to the
development. The relay of Example 7.2 does not click more often because it is
read more finely. A finer reading distinguishes more precisely when the
clicks occurred, and the question is whether physics registers those
distinctions.

The first rule applies to time as it does to states. A distinction between
two times at which an event might have happened counts only as far as the
system's own physics can register it or let it affect later records
([Definition A.6.5](#a-6-5)). The test is whether the record histories, or
what follows them, physically differ with the timing. How long a record
takes to form does not settle it: a record that takes a while to form can
still come out differently according to when the event occurred, and nearby
event times can change the chances of later records. Where the dynamics make
timing differences below some interval indistinguishable in every record
and every consequence, reading more finely adds nothing faithful. Whether a
given system has such a floor, or bounds its recordable timing information
without a sharp cutoff, or has a more complicated structure, is a fact about
that system, to be derived from its dynamics. It is not something to
assume.

There is also a ceiling on how coarse a cadence can usefully be. Above the
coarsest cadence that still resolves every kind of event the system
produces, whole families of events are missed. Such a cadence is faithful,
since everything it records is registered, but it omits so much that it
seldom decides anything.

**What physics says about timing.** Three things are known, and none of them
settles the question alone.
- **A speed limit.** A system cannot evolve to a state orthogonal to its
  present one faster than its mean energy above the ground state allows: at
  least h/(4E) (Margolus and Levitin 1998). For one electronvolt that is
  about one femtosecond; for an energy of kT at room temperature, about
  forty femtoseconds. The bound constrains evolution toward distinguishable
  states. It does not give an interval in which no interaction can occur,
  and it does not by itself bound the timing information records can carry.
- **How transitions begin.** The expansion of section 7.5 assumes that the
  chance of a transition in a short interval grows in proportion to the
  interval, as random waiting times give. Physical transitions often begin
  more slowly than that: in quantum evolution the chance of leaving a state
  grows with the square of the elapsed time, at times shorter than the
  correlation time of whatever drives the transition. There the expansion
  does not describe the development ([Theorem A.6.3](#a-6-3), scope).
- **Limits set by the law.** In Bohmian mechanics under quantum equilibrium,
  no subsystem can record its own configuration more finely than its
  conditional wavefunction allows (Dürr, Goldstein and Zanghì 1992). Limits
  on what can be recorded need not come from instruments; they can come from
  the physical law.

None of these fixes a universal smallest cell or time step. The limit
belongs to each case: to the couplings that form records in that system,
and to how its records are built. In Example 7.2, if the system's records
cannot register timing finer than 0.128 ns, the molecule leads at every
faithful cadence. If they can, the relay leads at the finest faithful
cadence, and that verdict is the measure's, not an artefact of the clock.

**Recording is a physical act.** A record is made by a physical system that
interacts with what it records, and the interaction changes what follows.

**Example 7.3: recording a system that oscillates.** A two-level system
rotates steadily between its two states at one radian per time unit,
completing a rotation in about six time units. A detector records which
state it is in, every τ time units, by an ideal measurement. Each
measurement leaves the system in the state found, so the records form a
chain that flips with a probability set by how far the system rotated since
the last record. For comparison, a switch that flips at random, 0.25 times
per time unit in each direction, with exponential waiting times, is read
passively at the same cadences. Both run for 10 time units.

| Cadence | Recorded two-level system (bits) | Random switch, read passively (bits) |
|---|---|---|
| 2 | 4.36 | 4.50 |
| 1 | 7.78 | 7.15 |
| 0.5 | 6.64 | 10.03 |
| 0.1 | 2.52 | 16.54 |
| 0.01 | 0.42 | 25.16 |
| 0.001 | 0.06 | 33.51 |

The passively read switch behaves as section 7.5 says: the finer the
reading, the more timing information, without limit. The recorded system
does the opposite past a point. Recording it more often leaves it less time
to rotate between records, so it is found where it was left, and its records
approach a single unbroken history. This is the quantum Zeno effect (Misra
and Sudarshan 1977).

What the example shows needs to be stated exactly.
- **It is not a refinement.** A finer passive description of one history
  never has less entropy than a coarser one ([Proposition A.6.2](#a-6-2)).
  Each cadence of the detector is a different measurement protocol, with its
  own law of outcomes, so the falling numbers contradict nothing. The
  protocols are different physically implemented processes under the same
  native law, as the workshop's two policies were (chapter 5).
- **It is not a bound on the whole field.** The numbers are the entropy of
  the recorded outcomes. The detector, the energy it draws, the access it
  takes, and what those resources would otherwise have done all belong to
  the whole-field comparison.

**Whether finer recording pays.** Because recording is physical, it is an
option like any other. Measuring more finely uses energy and access, and it
disturbs what is measured. Whether what it adds to the futures repays that,
or whether the same resources would open more elsewhere, is decided the way
every choice from one present is decided: by comparing the options, the
recording apparatus and its costs included ([chapter 5](#chapter-5)). It is
the question [chapter 14](#chapter-14) asks of information in general, which
pays only when it is used.

**What is open.** The recordable timing information of a system has not been
derived for any model in the program. The research question is how much
timing information a given physical system can preserve, or make
consequential, given its native dynamics and its finite resources, including
the clocks needed to register it ([chapter 33](#chapter-33)). Until it is
answered for a model, a ranking that a finer cadence reverses is a
resolution-dependent reversal, and the finest cadence computed gives a
provisional ranking, not a governing one.

> **In Omega**
>
> Omega contains every difference physics registers and no others. It
> includes the physically reachable histories in which each record could be
> formed, with its costs and its effects on what follows, but not an
> instrument that no development can build merely because it can be
> described. An instrument does not determine Omega; it is part of it, under
> the same law. The governing description is not whatever one instrument
> happens to measure: it is everything the development's own physics
> registers.

---

## 7.7 Limited frames and the ultimate frame

**A frame with coarse records ranks options at its own level of detail. Its
ranking approximates the governing one, and is reliable where it is
certified.**

Frames that form records typically register only part of the whole. A cell registers
some chemical differences and not others; an instrument resolves some
times and not finer ones. Each frame's ranking of options, made from its own
records, is a ranking at a coarser faithful level. Section 7.4 says how far
to trust it: where its lead exceeds what the omitted detail could add, it
agrees with the governing description; where it does not, a finer reading
shown to be faithful may correct it.

One distinction keeps this from being misread. A subject's own history,
the futures of one part of the world (chapter 8), is not a coarse
description of the whole field. It defines a different comparison, about a
different subject, and the whole-field comparison does not correct it. The
rule of this chapter applies within each comparison: to descriptions of the
whole field for the whole-field comparison, and to descriptions of a
subject's history for that subject's comparison.

---

## 7.8 What the chapter gives the rest of the manuscript

- **The test bed.** Every comparison declares its resolution, and every
  ranking is reported as certified, corrected, resolution-dependent or
  provisional ([chapter 12](#chapter-12)).
- **Parts and wholes.** The same rule applies to descriptions of a subject's
  history ([chapter 8](#chapter-8)).
- **Activity.** The crossover resolution is the formal form of the busyness
  objection, tested in [chapter 16](#chapter-16).
- **Information.** Whether finer recording repays its cost is a case of
  information paying only through what it changes
  ([chapter 14](#chapter-14)).
- **Quantum frames.** Records made by quantum frames are compared at the
  resolution their couplings fix ([chapter 29](#chapter-29)).
- **The program ahead.** How much timing information a system can preserve
  or make consequential, and each model's most complete faithful
  description, are open problems ([chapter 33](#chapter-33)).

---

## 7.9 What this chapter does not claim

- **That any level of detail is as good as another.** Of two faithful
  levels, the finer governs.
- **That more detail settles a comparison by itself.** A finer level
  decides only once its extra detail is shown to be physical.
- **That a ranking must hold at every level.** A coarse ranking that a finer
  level shown faithful reverses is corrected, not left undecided; one that a
  finer level of open faithfulness reverses is reported with both readings.
- **That every system has a smallest faithful cadence.** It may instead
  bound its recordable timing information without a sharp cutoff. Which
  holds is to be derived for each system, and has not been for any of the
  program's models.
- **That physics fixes a universal smallest cell or time step.** The limit
  comes from each case's couplings and records.
- **That a finer clock always adds futures.** A finer passive reading adds
  timing information; finer recording by a physical apparatus is a
  different process, and can suppress what it records.
- **That the recorded entropy of one instrument bounds the whole field.**
  The apparatus and its costs belong to the whole-field comparison.
- **That the most complete faithful description has been characterized.**
  It is the target; computed levels approximate it.

---

## Status of chapter 7

| Status | Claims |
|---|---|
| **D** (definitions) | declared resolution ([Definition A.6.1](#a-6-1)) (7.1); faithful distinction, faithful grain and cadence, refinement of passive descriptions, matched resolution, the governing description, and certified, corrected, resolution-dependent and provisional rankings ([Definition A.6.5](#a-6-5)) (7.2–7.4, 7.6); crossover resolution (7.5); the development, its records and the analyst's sampling, kept apart (7.6) |
| **T** (results, under their stated assumptions) | a coarser grain shows less lushness ([Proposition A.6.2](#a-6-2), proved here); the temporal expansion ([Theorem A.6.3](#a-6-3), established elsewhere); the crossover resolution ([Corollary A.6.4](#a-6-4), proved here); certifying a coarser ranking ([Proposition A.6.6](#a-6-6), proved here); the speed limit on evolution between distinguishable states (Margolus and Levitin 1998), absolute uncertainty in Bohmian mechanics (Dürr, Goldstein and Zanghì 1992) and the quantum Zeno effect (Misra and Sudarshan 1977), cited (7.6); the joint grain of two faithful grains ([Corollary A.6.7](#a-6-7), proved here) (7.3) |
| **M** | none; Examples 7.1–7.3 are exact computations in specified finite models; the count of certified rankings in random laws is Appendix A's verification V47 (7.4), and Example 7.3 is V48 |
| **E** | none |
| **N** | none |
| **C** | none |
| **Open** | the most complete faithful description of a given model; how much timing information a system's records can carry, and whether it has a smallest faithful cadence; a rule for cadences that share no common refinement (7.3, 7.6) |

## References cited in chapter 7

*Collected with full details in Appendix G.* Entries marked "to verify" are
not yet checked against their sources.

- Cover, T. M., and Thomas, J. A. (2006). *Elements of Information Theory.*
  2nd edition. Hoboken: Wiley. To verify.
- Dürr, D., Goldstein, S., and Zanghì, N. (1992). Quantum equilibrium and the
  origin of absolute uncertainty. *Journal of Statistical Physics* 67(5–6),
  843–907. To verify.
- Gaspard, P., and Wang, X.-J. (1993). Noise, chaos, and (ε, τ)-entropy per
  unit time. *Physics Reports* 235(6), 291–343. To verify.
- Margolus, N., and Levitin, L. B. (1998). The maximum speed of dynamical
  evolution. *Physica D* 120(1–2), 188–195. To verify.
- Misra, B., and Sudarshan, E. C. G. (1977). The Zeno's paradox in quantum
  theory. *Journal of Mathematical Physics* 18(4), 756–763. To verify.
