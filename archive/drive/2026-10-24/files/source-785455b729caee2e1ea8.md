# Lattice frame program, first pass — report r1

**Date:** 17 October 2026.
**Script:** `analysis/frames/lattice_frames.py`; results in
`lattice_frames_results.json`.
**Question:** does the structural definition of a physical frame agree with an
independent dynamical diagnostic, without being built from it?

## The model

- A ring of 7 binary sites under noisy local majority dynamics (error 0.12 per
  site per step).
- One particle hops left, right or stays, and swaps its internal bit with the
  bit of the site it lands on, so its constituents turn over.
- The joint state space has 1,792 states, and the stationary law is computed
  exactly.

## The two checks

1. **The definition (structural).** Is the candidate a set of the field's
   degrees of freedom? Sets may be contiguous or not, and may be carried by a
   locator that the dynamics move locally. Summaries that mix many sites into
   one value fail, and so do locators imposed by a schedule.
2. **The diagnostic (dynamical, blind to the specification).** At stationarity:
   - **autonomy**, I(D_{t+1}; D_t) / I(D_{t+1}; X_t): the share of the
     frame's predictable future that its own present supplies;
   - **screening deficit**, I(D_{t+1}; X_t | D_t, B_t), given its interaction
     neighbourhood B.

## Results

| Candidate | Definition | Autonomy | Screening deficit |
|---|---|---|---|
| moving particle with turnover | pass | 0.901 | 0 |
| local cluster {0,1,2} | pass | 0.680 | 0 |
| composite {0,1} + {4,5} | pass | 0.630 | 0 |
| checkerboard {0,2,4,6} | pass | 0.576 | 0 |
| single site | pass | 0.497 | 0 |
| **delocalized total (number of 1s)** | **fail** | **0.811** | — |
| analyst-redrawn site (jumps by 3) | fail | 0.098 | — |
| random hash of the whole state | fail | 0.093 | — |
| global parity | fail | 0.006 | — |

## What it shows

- **Eight of nine agree.** Every frame that passes the definition has autonomy
  between 0.50 and 0.90, and its interaction neighbourhood screens it exactly.
  Parity, the hash and the analyst-redrawn site all fall below 0.10. The two
  checks were not built from each other, so this agreement is evidence that the
  definition tracks something real.
- **The frame with turnover is the most autonomous.** The particle exchanges
  its constituent with the lattice at every step, and its own present still
  supplies 90 per cent of its predictable future. The dynamics carry the
  boundary; nobody redraws it.
- **The checkerboard passes both checks,** as a composite should. It is less
  autonomous than a contiguous cluster, because its sites' neighbours lie
  outside it.
- **One disagreement, the expected hard case: collective variables.** The total
  number of 1s is a summary, so it fails the definition. Under majority
  dynamics, though, it changes slowly and predicts itself well (0.81). Slow
  collective variables behave as dynamical individuals without being sets of
  degrees of freedom. Magnetization and order parameters are the physical
  instances.

## Reading the disagreement

There are two honest options. Neither is chosen here.

1. **Keep the definition.** A collective variable becomes a frame only when
   something physically records it: a probe, a field or another frame coupled to
   the total. That is the record criterion of Definition A.14.2 applied to
   classical frames. The next run would add a probe that couples to the total,
   and check that the probe's records instantiate it.
2. **Widen the definition.** Admit variables that the dynamics make autonomous,
   even if they are summaries. The cost: the definition would then partly rest
   on the diagnostic, and the independence that makes their agreement
   informative would be lost.

Option 1 keeps the two checks independent and matches A.7.1 ("a function that
summarizes the field without being instantiated in it"). The probe run would
test it.

## Limits

- One small model, one dynamics, and seven sites.
- Autonomy is a diagnostic in the spirit of the Carroll–Singh proposal, not
  their objective.
- Sol's candidates not yet run:
  - a temporary collision aggregate;
  - an open feedback controller with explicit sensing and action;
  - overlapping frames.
