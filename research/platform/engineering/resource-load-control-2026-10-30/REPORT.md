# Source-fed relaxation control — physical qualification and compact comparison

30 October 2026. Local engineering and one fixed-anchor smoke; no manuscript edits, commit or push.

## What was built and why it qualifies

The original R1 assembled apparatus can catalyse direct locked-carrier relaxation to heat, instead of the useful unlocking pair. Apparatus construction, its original costs, material, native thermal routes, energy function and source settings stay common. Each forward load step releases 3 resource-energy units; its native reverse returns 3 from the bath. No bank increment, usable-fuel production, new register or new constituent is added. This is a mechanism contrast, not a controller changing chemistry at no cost.

Both selected source-on controls have positive stationary net load heat, positive stationary net external work and positive T64 net load heat. Source-off stationary load heat/work vanish to numerical precision while thermal switching remains. Thus the paid-flow qualification is not merely spending the initial store, counting labelled events or overlooking refunds. It is a source-driven resource-dissipation loop; individual energy quanta are not genealogically traced to the source.

The old bank-returning rotor attempts stay retained and are not rerun or relabelled. This load is a different physical coupling. The first preparation-only snapshot preceded lint-only changes; no science ran under it. The executed source version and unchanged input plan are retained here.

## Calibration, frozen before history scoring

The productive arm has stationary event rate **0.182404770656 events/time** and net external work **0.0237976830978 energy/time**. Forty physical evaluations, including source-off references and every fit probe, are retained. Calibration used only physical moments and budget gates; no history entropy was computed or optimized during selection.

|Control|Load conductance|Stationary event rate|Stationary net work|Stationary net load heat|Qualified match|
|---|---:|---:|---:|---:|---|
|activity_matched|0.0636451103025|0.182404770656|0.0604210003065|0.0426240787741|True|
|net_work_matched|0.00121696344986|0.156649213015|0.0237976830979|0.00181263495291|True|

These are TWO separate controls. The activity-matched control uses about 2.54 times the productive arm's net external work. The net-work-matched control has about 14.1% fewer stationary jumps. Neither is jointly matched, and net external work is not gross accepted work. All accepted/returned/gross/net flows are retained.

The load merely catalyses relaxation; the apparatus must exist for the extra channel to fire. It does not directly enable bank capture or construction. Its reverse can feed the resource pool, and changing occupancy can indirectly affect other functions. These consequences are reported, not used as a post-score veto.

## Complete finite-history profiles

Primary cadence .25. Positive means productive exceeds the named control, in bits:

|Control|Physical horizon|Productive minus control|
|---|---:|---:|
|ablation|16|+5.844203098|
|ablation|64|+11.215079547|
|ablation|256|+35.735153905|
|ablation|1024|+140.925510196|
|activity_matched|16|+1.208652505|
|activity_matched|64|-0.022543609|
|activity_matched|256|-0.474133861|
|activity_matched|1024|+10.413313104|
|net_work_matched|16|+5.634594023|
|net_work_matched|64|+10.706232614|
|net_work_matched|256|+34.087969144|
|net_work_matched|1024|+134.954034789|

At matched stationary activity, the productive arm does not dominate every finite horizon. At .25 it leads at T16, trails at T64 and T256, then leads at T1024. The full evaluated prefix contains three sign changes, including one before T16. At .125 it also trails at T64/T256; at .5 it leads at those endpoints. These are disclosed temporal-resolution-dependent intermediate rankings, not a universal protection/generativity result or a solver error.

Finite work and jump totals are not matched by a stationary match. At T64, expected jumps are 13.3093 productive versus 13.6855 activity-control; net work is 1.36692 versus 4.80759. For the net-work control, T64 net work is only .461689 despite its stationary work match. These transient differences remain part of the complete comparison.

## Sustained-rate diagnostic

|Control|Cadence|Delta rate (bits/time)|Delta at T1024 (bits)|
|---|---:|---:|---:|
|ablation|0.125|+0.165752421|+171.865461493|
|ablation|0.25|+0.136222111|+140.925510196|
|ablation|0.5|+0.105675932|+108.923807486|
|activity_matched|0.125|+0.013063447|+8.070582778|
|activity_matched|0.25|+0.014343991|+10.413313104|
|activity_matched|0.5|+0.016026970|+13.225619642|
|net_work_matched|0.125|+0.159080388|+164.737713663|
|net_work_matched|0.25|+0.130628381|+134.954034789|
|net_work_matched|0.5|+0.101205611|+104.157036664|

The productive arm has a positive stationary entropy-rate difference against both separately matched controls at all three tested cadences. In particular, its activity-matched advantage is not attributable solely to a greater mean stationary jump rate: that moment matches to 8.4e-17 events/time, while the sampled history rates still differ. Transition destinations, state occupancy, sequences and correlations remain different. This is an existence example under these declared laws, not a unique subtraction of an organization-only component.

The net-work comparison removes a different nuisance coordinate but leaves an activity mismatch. Passing both separate comparisons is not proof of a simultaneous two-moment match. Thermal, reverse and apparently futile branching stays in every score. Kernel rates/biases and independent-ending readouts accompany the finite profiles; a rate is not substituted for the complete profile.

## Source-off diagnostic

The source-off arms reuse the fitted source-on conductances; they are not refitted and are not called activity-matched. At cadence .25:

|Control|Delta at T1024|Delta stationary rate|
|---|---:|---:|
|ablation|+56.147922972|+0.017636922|
|activity_matched|+30.671642080|-0.014045941|
|net_work_matched|+57.146847000|+0.016718524|

The activity control has the larger source-off stationary history rate even while the productive preparation still leads at T1024. Thermal activity persists and finite offsets/transients matter. Do not claim an eternal finite lead, subtract this background from the authoritative score, or call this a spatial thermal-gas baseline.

## Evidence and limits

96 arm profiles, 72 signed endpoint comparisons and 72 passing current paired checks. Maximum integrated first-law residual 1.0436096431476471e-13. Combined worker wall time 15.63s; peak memory 121.64 MiB. All inputs and selected physical matches were frozen before scoring; no sign was required for completion.

[CALIBRATION.json](physical/CALIBRATION.json) retains the full physical map and refunds; [RESULT.json](history/RESULT.json) retains every profile, comparison, contract, physical/functional readout and independent-ending value; [SUMMARY.json](SUMMARY.json) and [QUALITY.json](QUALITY.json) separate observed facts and limits. SNAPSHOT.zip and the receipts permit restoration without private run caches.

This remains a coarse fixed-slot whole-modeled-field example, with retained-unit inventory scope and unresolved bath/source histories. Original R1 maintenance/transport limitations remain. It is not chemical closure, recursively compounding ecology, physical-resolution faithfulness or ethical confirmation. The V register arm, a joint-match control and any wider physical map remain unrun. No automatic manuscript tier promotion or publication follows.

Final checks: **201 unit tests**, source/archive/evidence/local links, the
233-check baseline and exact P001 reproduction pass. The source snapshot
restores 44 inputs without running another simulation. See
[VALIDATION.json](VALIDATION.json) for provenance and privacy checks.
