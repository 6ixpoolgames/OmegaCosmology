# J2 — shared-intermediate qualification-gated run

31 October 2026. The user's “Run it all and then push” authorizes this run
and publication. Prior reports retain their own delivery status. Physical
outcome: **no_joint_match_in_bounded_search**; execution: **completed**.

## Outcome

No evaluated point matches both stationary moments within the .1% relative allowances. This two-start bounded search does not prove global infeasibility. No new lushness conclusion follows.

|Stationary quantity|New productive target|Selected control|Relative mismatch|
|---|---:|---:|---:|
|event_rate|0.159057260407|0.158477299413|-0.3646%|
|net_work_rate|0.0213185740189|0.0221486604925|+3.8937%|


The new productive targets were recomputed. They are not the old 75-state
J targets, and a smaller residual here is not a replay or a direct improvement
of the old comparison. All arms now include a thermally active intermediate.

Selected parameters: `{'k_entry': 6.899024701859616e-35, 'k_exit': 0.08914225160224247}`.
Selected physical payment gate: False.
The detailed solver starts and every physical point remain in
[CALIBRATION.json](physical/CALIBRATION.json). Successful numerical termination
does not establish matching. A start stopped at its evaluation budget is
explicitly identified, not treated as proof that no solution exists.

## Actual history stage

**Not run:** no qualified joint match was available. No new log-lushness, stationary entropy rate, bias, cadence ordering or ending-law total is reported. These quantities are not zero; they were not computed. The conditional history path was not exercised by this scientific run.

## Physical model

The same retained carrier has four conformations with integer codes 0/1/2/3
and energies 0/3/2/1.5. All arms share the additional native locked↔intermediate
and spent↔intermediate pairs at conductance .002, plus every old native bath,
basal unlocking/capture, construction and upkeep route. Temperature, source .08,
and root energy 4.5 stay common. The source and bath histories remain unresolved.

The control ablates motif unlocking and adds bond-gated locked->intermediate
and intermediate->spent discharge. Each forward leg exports 1.5 heat, changes
no bank and has zero direct work; each reverse consumes 1.5 heat. Native
thermal motion remains when apparatus is absent. The intermediate is an
explicit energetic state with physical residence, not an event label or clock.
Physical faithfulness to a microscopic carrier remains an assumption.

This is a new common finite grammar, not a silent correction or a refinement
certificate for older evidence. Construction and maintenance retain R1's
known limitations. Captured energy and bath fluctuations both remain in the
ledger; no event class is removed from the score.

## Resources and limits

122 physical evaluations; state counts [100];
32 evaluated source-on points
pass the physical payment gate, which is distinct from moment matching.
The physical worker took 42.64s,
peaked at 172.20MiB and
wrote 1.79MiB, within
300s/1GiB/64MiB/132-evaluation caps. No parameter box, source strength or
desired sign was changed after examining outcomes.

Maximum finite first-law residual 1.3533618670180658e-12;
stationary residual 1.3536264123481523e-16; source-off per-load
net heat residual 1.2701428450667684e-16.

The source-on intermediate's stationary occupation and mean residence are
retained for every evaluated point, as are finite T64 occupation and exit
counts. Full source gross/returned/net work and per-leg refunds are retained.
Positive forward bills are never substituted for net consumption.

## Interpretation

This is a result about the construction and qualification of one comparator
family. No failed design guess becomes a theory failure, no unqualified point
becomes evidence for organization winning or losing, and no global
impossibility follows from the bounded search. The prior separate-moment
lushness results remain unchanged and keep their limitations.

See [MODEL_CARD.md](MODEL_CARD.md), [QUALITY.json](QUALITY.json),
[VALIDATION.json](VALIDATION.json), [IMPLEMENTATION_NOTES.md](IMPLEMENTATION_NOTES.md)
and [REPRODUCE.md](REPRODUCE.md). Private manuscripts are not included.
