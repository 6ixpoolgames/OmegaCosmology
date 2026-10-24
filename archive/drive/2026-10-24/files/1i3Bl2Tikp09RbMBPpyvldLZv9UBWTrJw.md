# Lattice frame program, second pass — report r2

**Date:** 17 October 2026.
**Supersedes:** report r1. Its results are restated in the first table below;
its reading of them is corrected in "What changes from r1".
**Scripts:**
- `analysis/frames/lattice_frames.py` (first pass, unchanged);
- `analysis/frames/lattice_frames_probe.py` (this pass). Results are in
  `lattice_frames_probe_results.json`.

**Question:** does the structural definition of a physical frame agree with an
independent dynamical diagnostic?

## The two checks (unchanged from r1)

1. **The definition (structural).** Is the candidate a set of the field's
   degrees of freedom, possibly carried by a locator that the dynamics move
   locally? Summaries and relations between locators fail, and so do locators
   imposed by a schedule.
2. **The diagnostic (dynamical, blind to the specification).** At
   stationarity:
   - **autonomy**, I(D′; D) / I(D′; X): the share of the candidate's
     predictable next state that its own present supplies;
   - **screening deficit**, I(D′; X | D, B), given its interaction
     neighbourhood B.

## First pass, restated

Ring of 7 sites under noisy majority dynamics (error 0.12), and one particle
that swaps its bit with the site it lands on.

| Candidate | Definition | Autonomy |
|---|---|---|
| moving particle with turnover | pass | 0.901 |
| local cluster {0,1,2} | pass | 0.680 |
| composite {0,1} + {4,5} | pass | 0.630 |
| checkerboard {0,2,4,6} | pass | 0.576 |
| single site | pass | 0.497 |
| total number of 1s | fail | 0.811 |
| analyst-redrawn site | fail | 0.098 |
| random hash | fail | 0.093 |
| global parity | fail | 0.006 |

## This pass

### 1. A probe on the total (option 1 of r1)

**Model.** The same ring without the particle, plus a probe register that
reads the total number of 1s each step. In the plain variant the probe reads
with read error δ and overwrites its record every step. In the retaining
variant it keeps its record with probability m. On its own, the total has
autonomy 0.923 in this model.

| Probe | Read error | Retention | Record fidelity | Probe autonomy |
|---|---|---|---|---|
| overwrites | 0 | 0 | 1.000 | 0.384 |
| overwrites | 0.1 | 0 | 0.775 | 0.295 |
| overwrites | 0.3 | 0 | 0.478 | 0.171 |
| overwrites | 0.6 | 0 | 0.176 | 0.052 |
| overwrites | 0.9 | 0 | 0.014 | 0.003 |
| retains | 0 | 0.5 | 0.498 | 0.634 |
| retains | 0 | 0.8 | 0.234 | 0.837 |
| retains | 0 | 0.95 | 0.053 | 0.956 |

Record fidelity is I(probe′; total) / H(total).

- **The probe passes the definition at every setting.** It is a register: a
  set of degrees of freedom.
- **Recording does not hand the total's autonomy to the probe.** A perfect
  probe that overwrites its record holds the total exactly, yet scores 0.384
  against the total's 0.923. Its next state is supplied by the field it reads,
  not by its own present.
- **Retention raises autonomy, but only as the probe tracks the total less.**
  At retention 0.95 the probe scores 0.956 and holds 5 per cent of the total's
  information. Autonomy here measures the probe's own memory, not how well it
  instantiates the collective variable.

**Reading.** Recording puts the total's *value* into a frame. It does not make
the total a frame, and it does not make the probe a dynamical stand-in for it.
The recorded quantity and the recording frame come apart. Option 1 survives in
its plain form: a collective variable is something a frame can register, not a
frame itself. Its predicted repair, that the probe would carry the total's
autonomy, does not occur.

### 2. An open feedback controller (Sol's candidate)

**Model.** As above, but the probe also acts: a high reading drives site 3
towards 1, a low reading towards 0.

| Read error | Controller autonomy | Action on site 3 (bits) | Total's autonomy |
|---|---|---|---|
| 0 | 0.371 | 0.471 | 0.889 |
| 0.3 | 0.150 | 0.471 | 0.832 |
| 0.9 | 0.002 | 0.471 | 0.768 |

- **The controller passes the definition and acts on the field.** The action
  term, 0.471 bits, equals 1 − h₂(0.12) at every read error. It is set by the
  actuation noise and by the symmetry of the readings, not by the quality of
  the reads.
- **Its autonomy is close to the passive probe's.** Acting does not make the
  controller more of an individual on this diagnostic.
- **Acting on poor reads lowers the total's autonomy,** from 0.923 without
  feedback to 0.768 at read error 0.9. A controller that acts on noise injects
  noise into the field.

### 3. A temporary aggregate (Sol's candidate)

**Model.** Two particles hop on a ring of 8 sites. When they land on the same
site they bind with probability 0.8, and a bound pair unbinds with probability
0.05 per step (mean life 20 steps). The pair is bound 63.2 per cent of the
time.

| Candidate | Definition | Autonomy |
|---|---|---|
| bound pair: whether it exists, and where | pass | 0.937 |
| co-location, same model | fail | 0.907 |
| co-location, no binding (control) | fail | 0.248 |

- **The bound pair passes both checks** while it exists. A frame need not
  persist (Definition A.7.1), and a frame that forms and dissolves is handled
  without any special rule.
- **Binding is what makes it autonomous.** The same variable scores 0.248
  when the particles do not bind.
- **Co-location scores high in the binding model only because it nearly
  coincides with the bound pair.** 97.2 per cent of co-location is bound.

### 4. Overlapping frames (Sol's candidate)

**Model.** The first-pass model; clusters {0,1,2} and {2,3,4} share site 2.

| Candidate | Definition | Autonomy | Screening deficit |
|---|---|---|---|
| cluster {0,1,2} | pass | 0.680 | 0 |
| cluster {2,3,4} | pass | 0.680 | 0 |
| union {0,…,4} | pass | 0.741 | 0 |

- Both overlapping clusters pass both checks, and their next states share
  0.425 bits. Overlap raises no difficulty for either check. Nothing needs to
  be assigned to one frame or the other, in keeping with the remark to
  Corollary A.7.9 that overlapping subjects need no rule.
- Cluster {0,1,2} reproduces the first pass's 0.680 exactly.

## What changes from r1

1. **Autonomy is not evidence that the definition is right.** r1 read the
   eight-of-nine agreement as evidence that the definition tracks something
   real. This pass shows that the diagnostic measures self-prediction, which
   any projection can have:
   - summaries can score high: the total (0.923), and co-location (0.907);
   - genuine frames can score low: a noisy register (0.003);
   - the ratio is unstable when its denominator is small: the noisy register's
     I(D′; X) is 0.04 bits.

   The r1 agreement owed much to the choice of candidates. The claim should be
   withdrawn.
2. **High-autonomy summaries are slow modes of a containing frame.** The total
   is a slowly changing feature of the whole ring's continuation, and
   co-location is a near-copy of the bound pair. Each is real dynamics. In
   both cases a frame already contains it: the whole ring, or the pair. Making
   the summary a frame of its own adds nothing to either.
3. **Option 2 of r1 (widen the definition to admit autonomous summaries) is
   now weaker.** It would admit co-location and the total. It would also have
   to say why a noisy register, a set of degrees of freedom with autonomy near
   zero, is not a frame.

## Limits

- **The screening check is empty for the probe and the bound pair.** There,
  the neighbourhood together with the candidate's own state is the whole state,
  so the deficit is zero by construction. Only the cluster results test it.
- **Scope.** Small models, one dynamics each, and stationary statistics only.
- **Not tested:**
  - transients;
  - frames whose boundary is set by an interaction strength rather than by a
    bond;
  - the probe with an integrating update, in which its own state and its
    reading combine.

## Open for discussion

- Whether to keep the definition as stated in Definition A.7.1 (structural,
  sets of degrees of freedom), with autonomy reported as a description and not
  as a test. That is the reading this pass supports.
- Whether chapter 16 (now chapter 9) should present collective variables as
  what frames register, with the total and co-location as the worked cases.
- No change to Appendix A is proposed until this is discussed.
