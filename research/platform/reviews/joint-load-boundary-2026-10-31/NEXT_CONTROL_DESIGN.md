# Prospective J2: costed two-step carrier discharge

31 October 2026. Design recommendation after the retained-J boundary review.
**Not implemented, compiled, fitted or scored.** This does not authorize
another run. It is a new common substrate version, not a repair of J's record.

## Physical change

Resolve one intermediate conformation I of the existing single carrier.
Carrier integer code3 denotes I with energy1.5. Keep the old spent0,
locked1 and usable2 codes with energies0,3 and2. Code is not energy.
The intermediate contains the same retained carrier material; it is not
a new independent register, clock or extra fuel unit.

Keep I in **all** arms. Give all arms the same native, reversible locked↔I
and I↔spent thermal routes, initially proposed at the existing carrier-bath
conductance .002 for each pair. Keep the old direct baths and basal unlocking,
capture, assembly, upkeep, source and root. Beta stays1. These are proposed
stipulated kinetics, not an empirical chemical calibration. They must be
explicitly reviewed as such before execution.

The old source supplies three energy units per forward locked-carrier
arrival; the built root still has its original endowment4.5 and I unoccupied.
Do not add entropy for choosing a root or reset I on apparatus loss.
Ordinary native dynamics let I relax or re-excite even while no bond works.

## Arms

1. Productive: old motif-assisted locked↔usable path on the expanded carrier
   grammar; no added discharge catalysis.
2. Plain ablation: remove only that motif-assisted pair, leaving I and every
   native thermal route present.
3. Discharge control: plain ablation plus bond-gated catalysis of locked↔I
   and I↔spent, with independently declared nonnegative conductances.

Each discharge forward leg releases1.5 energy to the bath, changes no bank,
and has zero direct work. The reverse consumes1.5 from the bath. Local
detailed balance fixes forward/reverse ratios; catalysis accelerates both
directions. Native useful routes remain in the control: no unrelated
capture channel is disabled. New indirect effects on supply, bank or assembly
remain part of the physics and cannot be vetoed after observing a score.

All three arms share the expanded state grammar, Hamiltonian, material,
native routes, boundary and root. They have about100 allowed states rather
than75:25 old apparatus/bank configurations times four carrier states.
Validate actual reachability and budgets before a run; this is a combinatorial
estimate, not a benchmark. This enlargement changes the underlying dynamics
in all arms, so old productive targets cannot be reused.

## Why this is a different question

The proposed control has a real two-step resource-to-heat route rather than
two alternative one-step drains. It may change events per net work in the
direction missing from the old fit. It may also fail to do so. A shared
thermal intermediate can change the useful arm's target too.

An event is counted only when a resolved physical state changes. Parallel
channel labels aggregate. The existence of an intermediate chemical
conformation is a modeling assumption, not a numerical subdivision trick:
document its energy, material identity, allowed couplings, residence times
and what the declared state grain resolves. If no such physical interpretation
can be supplied, do not use this construction merely to add entropy.

This count-world design still does not establish a finest faithful grain or
microscopic chemistry. Native stochasticity stays in every arm. No event
class is subtracted and no score is renormalized by work or activity.

## Required gate before any scoring

Review the new grammar and energetics first. Recompute both stationary
targets from the expanded productive law. Inspect source-on/off flows and
actual residence/occupancy before fitting two physical moments. Matching
uses no history, rate or bias objective. Keep finite T64 work/activity
mismatches and gross/refunded flows separate from the stationary match.

Retain the preceding physical thresholds: stationary residual1e-10,
finite energy/source-off flow residuals1e-8, positive stationary net source
work and net heat from every active added discharge leg, and positive finite
T64 total discharge heat. Each matching allowance is1e-10+.001*abs(target).
Evaluate the native reverses; counting forward bills without refunds is
insufficient. Report a matched but unqualified fit distinctly from no match.

A future pilot should remain one source anchor, one declared family and
about the existing132-evaluation/300s/1GiB/64MiB cap, with a hard state ceiling
checked before dispatch. Its grid, solver starts, parameters and budget are
to be made explicit in an executable plan before physical evaluation.
The prior one-start search did not prove global infeasibility, so the next
plan should diagnose boundary versus interior solutions explicitly rather
than rely on a solver success flag.

Stop at physical qualification again, regardless of outcome. Only a separately
authorized later stage would calculate lushness. No desired sign is required.

## Alternatives and their limitations

- Adding a parallel bank-relaxation channel can be a valid versioned kinetic
  intervention, but at the current grain it can be exactly equivalent to
  increasing existing upkeep. It should not be called distinct physical
  machinery merely because a new event label was added.
- Adding a neutral register can generate paid variation, but its hardware
  must exist in all comparisons and be counted. It tests a different mechanism
  from carrier discharge and should not be hidden in a matching adjustment.
- Altering the source or clock breaks the current common-boundary/control
  question. Mixing fitted laws needs a physical selector and its costs;
  the sampled convex hull is not such a selector.

The choice of comparator is substantive model design, not a choice of which
histories to count. Preserve all prior results whatever J2 eventually shows.
