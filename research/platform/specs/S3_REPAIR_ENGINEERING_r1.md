# S3 repair and support-query engineering

25 October 2026. Authorized by the author's "Push unpushed and go next" following
the [S3 addendum](S3_INTERACTION_AND_HARM_ADDENDUM_r1.md). First push the pending
design notes, then implement and profile a capped smoke before selecting a map.

## Physical motif

Two distinct material slots R and Y each have precursor/damaged state0 and
constructed state1. R assists recipient-bank-paid restoration of Y. Y assists
restoration of R and catalyses capture from the same finite carrier. There is
one bank, not two independent grants. Occupied contacts R->Y and Y->R share
the constituent ports; Y cannot capture catalytically while bound in either
role. Native release, basal rebuilding/breakdown and unassisted paid rebuilding
remain. This is a reversible repair/access loop, not permanent destruction.

Formation energies .5 each, bank quantum.5, capacity2 ticks, construction bill2
ticks, bond energy-.25. Carrier energies0/3/2 and source work3 remain unchanged.
All directed events retain work/heat accounting and paired thermodynamics.
The local source-off reference must pass Gibbs detailed balance.

The feedback-ablation control removes only the Y-assisted paid reconstruction
conversion pair for R. Its contact still binds/releases, all energies and
material states stay, and unassisted reconstruction remains. This is a mechanism
contrast, not free backup hardware or a physically chosen option.

## Present sections and matching

In coordinate order R,Y,bank,carrier,contact-RY,contact-YR:

- intact = (1,1,2,1,0,0), energy5;
- repair-fault = (0,1,2,1,0,0), energy4.5;
- access-fault = (1,0,2,1,0,0), energy4.5.

The two faults have the same immediate constituent loss and energy deficit.
Their downstream comparison is matched in endowment under one law. Each fault
versus intact is also reported, explicitly as a different-energy preparation
diagnostic. No fault event or loss procedure has been enacted in the model.
The missing .5 is not silently deposited in the bank or rewarded as entropy.
An explicit common-present fault pulse is subsequent work.

The assay therefore supports per-preparation energy declarations, preserving
the existing protocol-wide default and checking every root against its declared
value. No arbitrary energy mismatch is accepted without this declaration.

## Queries

Whole modeled sampled history includes contacts and carrier; bath/source
histories stay unresolved. Component projections R and Y exclude the shared
bank/carrier and retain observed-history memory. They are component-history
diagnostics, not two interacting valuers. The shared bank is separately measured.

Function predicates: R available, Y functional, and both available. Report
deadline occupancy, integrated uptime, ever reaching the target, loss/return,
paid repair counts and accepted work. For a fault initially outside the target,
ever-target probability is unconditional restoration by the deadline; do not
reuse the initially-functional loss-and-return cohort for that query.

Add graph closure: a state is closed relative to a target iff no native directed
path reaches it. The closed set is forward invariant, so endpoint mass in it
equals closure-by-deadline probability. A reverse rate as small as1e-100 still
prevents structural closure if it provides a path. These reversible motifs
should have zero structural closure, without implying rapid or likely recovery.

Integrate exact support-loss reference weights for the same-law preparations
at the whole and R/Y observations. Projected support uses candidate hidden-state
subsets and reference hidden-state mass, not a projected Markov kernel. Full
candidate word support yields a structurally exact zero. General nonzero
reference weights are float64, not rigorous numerical intervals. Caps reject
subset growth explicitly. Probability suppression is implemented/tested only
on finite enumerated word laws; no long-history curve is claimed here.

## Smoke and acceptance

Two54-state cases (feedback intact/ablated), three known roots, T4/16, cadence.25.
Caps300s/2GiB/32MiB per case,600s/64MiB batch, one worker. Memory2 projected
bounds and native depth3 ancestry are affordable reference queries here. Native
support/LP checks use independent tiny examples. No lushness sign is required.

The smoke must validate matched fault loss, distinct route consequences, native
recovery, source-off equilibrium, energy residuals, passive-query marginals and
foreclosure versus recovery distinctions. Retain all setup failures and resource
receipts. If feasible, use measured cost to choose a small source/feedback map
and an occupied-interaction comparison. No inventory is shrunk after ranking.

The first smoke completed under a4GiB cap at116MiB peak, but its separately
printed RAM preflight did not gate dispatch. The supervisor now enforces the
reserve; the repeated smoke uses2GiB caps and retains the original run. Only
the resource supervision changed. Source snapshots distinguish the versions.
