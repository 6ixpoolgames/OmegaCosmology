# J — joint resource-load physical pilot

31 October 2026. Completed locally at the user's “Ok go next”; no commit,
push or manuscript application. Engineering status: **no_joint_match_in_bounded_search**.

## Outcome

No evaluated control meets both moment tolerances. This bounded one-start search does not establish impossibility elsewhere in the same family, still less in other families. No history scoring follows.

|Stationary quantity|Productive target|Selected control|Absolute residual|Allowed absolute error|
|---|---:|---:|---:|---:|
|event_rate|0.182404770656|0.16043853815|-0.021966232506|0.000182404870656|
|net_work_rate|0.0237976830978|0.0245534667337|+0.000755783635902|2.37977830978e-05|


Selected conductances: `{'k_L': 9.965648261220834e-27, 'k_U': 0.003562533587914402}`. Per-route stationary net heat
(energy/time): load_locked: 1.56358795431e-26, load_usable: 0.00213067687205. Selected physical payment qualification:
**False**. Finite T64 and gross/refunded flows are
retained in full, including source-off at these unchanged conductances.

The solver's termination is `completed`; solver
success is not the simultaneous physical-match criterion. The target is
inside the convex hull of sampled moment pairs:
**True**. This is not proof
that one static physical model attains it. A random mixture or switching among
laws is not silently substituted for a single control: a physical selector
would need its own state, energy accounting and changed continuation law.

The local dimensionless stationary sensitivity condition number is
81.55669408730735; its aligned affine-generator
identity residual is 1.735e-17.
The responses are locally distinct, but this does not prove global feasibility
or optimality of the selected point. Matrices were aligned by physical states
before differencing; no new sensitivity probe models were needed.



## Interpretation of the physical boundary

Selected event-rate mismatch: -12.04%; selected
net-work mismatch: +3.18%, against the frozen
.1% relative allowances. The selected conductances and each route's heat
above make negligible or importing routes visible. No evaluated point met
both moment tolerances. This is not a failed lushness prediction: no lushness
comparison was run.

Adjustability of each moment somewhere does not guarantee simultaneous
attainability in one static physical model. A local full-rank response and
the sampled convex-hull diagnostic do not settle this nonlinear family's
global moment surface. This one-start bounded search supplies no global
impossibility proof. Before another search, review energy per event and the
physical attainable surface. Any multistep load or selector would be a new
costed construction, not a silent extra knob in this completed pilot.


## Physical construction and scope

The fixed source-.08 R1 anchor retains its built root,75-state grammar,
Hamiltonian, temperature, material, baths, basal routes and construction/capture
costs. The control ablates only motif unlocking and adds two bond-gated
resource-to-heat channels: locked1->spent0 releases3 energy; usable2->spent0
releases2. Both native reverses remain. There is no new bank, register,
constituent or source. Original native rules are checked unchanged, loads
change only the carrier, and their individual bills/refunds stay visible.
Parallel outcomes aggregate normally; event labels are not added futures.

The two parameters were calibrated only on stationary event count and net
external work. Gross work, finite T64 totals, occupancy and path laws are
not jointly matched. Direct dissipation does not imply absence of indirect
access effects. No history entropy, entropy rate, bias or desired ranking
entered the objective. Original single-load, rotor and manuscript-audit
records are unchanged. No control family, common noise or source was retuned
after seeing the outcome.

## Budget and validation

105 compiled physical evaluations; state counts [75].
Source-on control evaluations 64, of which
54 meet the physical payment
gate; net importer count 0. Physical
qualification alone is not moment matching.

Runtime 27.14s; peak process-tree memory
155.02MiB; worker output
1.36MiB. Declared caps300s/1GiB/64MiB,
132 evaluations and 200 states; cap reason None.
Integrated first-law residual 1.9895196601282805e-12;
stationary residual 1.6393136847980827e-16; source-off load
net heat residual 3.365363543395006e-16.

The frozen plan is 7446091a870619448fc7bbf575296f0a318908480155bb7f240f2506d28562f4. See
[CALIBRATION.json](physical/CALIBRATION.json), [SUMMARY.json](SUMMARY.json),
[QUALITY.json](QUALITY.json), [RECEIPT.json](RECEIPT.json),
[VALIDATION.json](VALIDATION.json) and [REPRODUCE.md](REPRODUCE.md).
All grid/fit points and the source snapshot are retained. No physical grain
faithfulness, chemical closure, global impossibility or ethical result is
claimed. Stop at this physical report; no history stage was executed.
