# Generative ecology and physical control: implementation specification r2

Date: 23 October 2026. Intended implementer: Sol 6.1.

**Status: proposed engineering specification. No new scientific execution is authorized by this document.** The user paused runs on 18 October and has now requested a specification. Implementing, smoking and launching a survey are distinct subsequent actions. Do not restart old workers or interpret stale `running` receipts as live processes.

This is the foundation of a new experimental leg, built on the existing test bed rather than a replacement for it. The first deliverable is a small, verified, coupled productive world. Population, spatial organization, cross-scale composition, independent control and bounded agents must fit its interfaces, but need not all fit its first state space.

Revision r2 incorporates the user's follow-up and Opus's requested scope comparison, embodiment audit, compression assay and standard report. The reported Foundations r4 wording is adopted: **a frame specifies an admissible present section; the present is the sufficient physical specification on it.** Foundations r4 itself was not independently fetched in this pass. This local specification remains held back from commit, push, upload and external distribution. The manuscript is not edited by this handoff.

## 1. The question and the intended advance

Under a declared native law, physical endowment and boundary prescription, **which organizations and physically implemented ways of going on produce greater weighted continuation, and what do they enable, preserve or foreclose?**

The recent theory clarifications change the emphasis of the experiment:

- The object is the physical continuation field, including stochastic activity. An optimizer is one physical mechanism inside it, not the source of its possibilities.
- Access is represented by the transitions, dependencies and compositions the world supports. Do not multiply history perplexity by a separate access score.
- Generativity is an enabling relation within that structure: use can construct or maintain the conditions for further use. Its consequences enter the same continuation law.
- Value requires valuers motivates examining this substrate. Lushness is not a stipulated welfare sum, and this model does not prove the ethical thesis by definition.
- Frames specify present sections and their conditioning. A compartment, controller, projection or physical body is not automatically a frame. This classical adapter uses a declared common present and subsystem-history projections from it.

Earlier experiments separately established finite examples of recursive enabling, paid access, persistence and self/whole disagreements. This leg should join those mechanisms. It should reveal the difference between spending a gradient, maintaining an access channel, building further enabling structure, and redirecting another structure's resources.

The four scientific targets are:

1. **Productive organization:** compare immediate use, upkeep, reconstruction and expansion through their actual downstream effects.
2. **Composition and plurality:** compare concentrated, distributed, redundant and complementary arrangements without a reward for diversity or a presumption that more units is better.
3. **Scope of control:** resolve when a local material or continuation gain agrees or conflicts with whole-field continuation in the same productive ecology.
4. **Compression:** find whether physically different rebuilding capacities can accompany equal or nearly equal lushness at a specified query, and whether that equality survives longer or differently resolved continuations.

The first release covers target 1 and supplies the physical foundation for the others. The first controller family must already support the paired local/whole query; it need not wait for appropriation. It must not be described as a completed test of interpersonal ethics, consciousness, open-ended growth or a microscopic gas baseline.

## 2. Commitments that implementation must preserve

### 2.1 Primary quantity

For a finite classical CTMC with generator Q, full declared state X, fixed initial present x, cadence delta and horizon T=n delta:

    P_delta = exp(Q delta)
    ell_x(T, delta) = H(X_1, ..., X_n | X_0=x)
    L_x(T, delta) = 2 ** ell_x(T, delta)

Store and compare log-lushness `ell` in bits; retain the definition of L without overflowing floating-point exponentiation. A difference in ell specifies a perplexity ratio, not an additive number of physical histories.

For the full Markov state:

    ell_x(T, delta) = sum_{k=0}^{n-1} (mu_k dot h_delta)
    h_delta[i] = H(P_delta[i, :])

Initial preparation ensembles use **the average conditional score over roots**, unless explicitly testing an unobserved preparation distribution. Do not add the entropy of drawing a reference root to the continuation score.

Finite-history profiles are primary. Long-run rates, root offsets, repayment estimates and temporal coefficients are useful diagnostics. Do not introduce a default lexicographic rate-first optimizer. Do not erase a finite loss because an asymptotic tail eventually dominates.

T is the clock parameter of this classical physical adapter along its chosen continuation orientation. Using it computationally does not make time a primitive of the general ontology. Likewise, `whole-field` in a toy report means the whole **declared modeled field**, not the entire universe. Ideal work reservoirs and baths have accounted flows but no resolved microscopic histories here. State that boundary limitation; do not assume their unmodeled entropy cancels merely because their prescribed temperature or source settings match.

### 2.2 Randomness and resolution

Count all state-changing stochasticity represented by the chosen physical adapter: thermal channels, damage, controller switching and productive reactions. Do not add abstract action-label entropy, reaction-name entropy, uniformization self-events or query-monitor entropy. Parallel channels with the same physical endpoints sum in Q.

The full declared state is primary **within this adapter**. It is not certified as the finest physically faithful description of nature. Merging a coordinate is an observation/projection query, not an automatic coequal definition of the whole field. A finer physical adapter and a mere relabelling are different operations.

Cadences 0.125, 0.25 and 0.5 initially provide a temporal diagnostic corridor. They are not, by themselves, a proof of physical resolution adequacy. Register any proposed physical timing anchor separately; do not invent one to retain a preferred ranking. Rule A remains outside the primary objective.

### 2.3 Interpretation

Keep these statuses separate:

| Status | Meaning |
|---|---|
| Engineering failure | The implementation violates its physical or numerical contract. |
| Unsupported query | The requested object cannot be computed or instantiated by this adapter. |
| Unresolved comparison | Error bounds, sampling uncertainty or the tested resolution corridor do not decide the ordering. |
| Missed expectation | A recorded directional guess did not occur. This alone is not failure of the principle. |
| Mechanism demonstrated | A specified enabling, recovery or control mechanism occurs, with its measured consequence. |
| Limitation or tension | The measure favours activity, concentration or loss under the declared complete model. Preserve and explain it. |
| Scoped challenge to a claim | A result contradicts the actual stated claim under its applicable premises. Name those premises. |

No percentage of cost coverage, uptime, generation probability or service allocation is a universal pass threshold. No unfavourable functioning regime may be renamed non-generative merely because its lushness comparison loses.

Version and snapshot the inputs before executing them so results are reproducible. This is not a requirement to guess winners before exploration. Parameter changes create new study revisions and retain the old observations. Existing runner freeze checks must not be silently disabled: use their snapshot contract or an explicitly versioned successor.

## 3. Reuse the working architecture

Repository examined at HEAD `4ec30ca368ba4f73348d7cdf5adbcdede90f58df`, with substantial uncommitted work present. Hash the actual source files used, not just HEAD. Preserve all historical adapters and their manifests.

Paths below are relative to the repository root.

| Existing component | Use in this leg | Required care |
|---|---|---|
| `omega_v2/testbed/contracts.py` | `Event`, `RuleModule`, `WorldSpec`, measurement and study contracts | Add compatible wrappers/metadata; avoid breaking old constructors. |
| `compiler.py` | One module event law feeding sparse Q and physical ledgers | Ledger balance alone is not a thermodynamic proof. Add pair-level audits. |
| `composition.py` | Product composition and strong-lumpability checks | Its energy composition is additive. Interaction energies require a joint adapter and all affected rates. |
| `energy_grid.py` | Exact rational energy units with decimal input | Never round a physical bill silently or replace it by a probabilistic mean payment. |
| `robust_generativity.py` and `analysis/generativity_depth.py` | Existing cyclic enabling mechanisms and conservative depth witnesses | Generalize semantics; do not assume tuple positions or infer lineage from counts. |
| `analysis/generativity_robustness.py` | Recovery, structural closure and joint path queries | Preserve unconditional recovery and monitor projection back to the native law. |
| `analysis/streamed_history.py`, `dyadic_history.py` | Streamed entropy rows and finite occupations | Verify supported cadence/horizon shapes; current dyadic routine has explicit restrictions. |
| `analysis/finite_classes.py`, `reachable_rates.py` | Reducible-chain rates and reachability | Use root-reachable class weights, not an arbitrary stationary vector. |
| `analysis/observed_history.py`, `sparse_marginal.py`, `marginal_likelihood.py` | True projected-history bounds and known-model filtering | Dense likelihood helper allocates P and block tensors. Never invoke it on a large world without its memory gate. |
| `analysis/temporal_profile.py`, `dyadic_history.py` | Expected jumps and the finite temporal term | The older temporal helper builds a dense jump matrix. Use sparse coefficient vectors for large worlds. |
| `analysis/registry.py` | Versioned readout registry and capability requirements | Extend result metadata, not a second objective system. |
| `workflow/manifest.py`, `runner.py`, `artifacts.py` | Source snapshots, capped Windows workers, cache identities and artifact index | Retain process-tree caps, immutable bundles and reconstruction safeguards. |

Extract a reusable helper when two real adapters need it. Do not build a universal simulator, arbitrary plugin loader or deep inheritance hierarchy first. No new heavy dependency is required for the initial slice; use the installed numerical stack.

## 4. Architecture and contracts

The dependency direction is:

    physical schema + boundary law + modules + physical controller implementation
        -> compiled native event model / Q
        -> preparations and continuation queries
        -> full and projected history measurements + structural readouts
        -> comparisons, interpretation and reports

Analysis cannot modify transition rates. Reports cannot decide which events count. A controller selected by an offline search must still execute through the native physical law.

### 4.1 Physical schema

Add a small `PhysicalSchema` wrapper with named coordinates, finite domains, units, conservation groups and version. It resolves names to tuple positions once. The numerical kernel may continue to use compact integer tuples and arrays.

Each coordinate declares:

- physical meaning and subsystem ownership, including shared/relational ownership;
- energy contribution or involvement in an interaction-energy function;
- whether it is a stored physical record, a resource, material count or selector state;
- valid observation projections;
- optional population/species identity, without assuming individuals are labelled.

No module may depend on another adapter's tuple offsets. Species names and dependency graphs are data, not hard-coded A/B/C branches throughout analysis.

### 4.2 Law and reaction contracts

Build `WorldSpec` from a versioned `EcologyLawSpec`. Each reversible mechanism declares a `ReactionPairSpec` containing:

- pair id and physical mechanism version;
- endpoint transformations and validity guards;
- material stoichiometry, support, work exchanged with each external reservoir;
- energy/degeneracy inputs and inverse transformation;
- a symmetric conductance or an independently validated forward/reverse propensity pair;
- catalytic dependencies and the actual assistance multiplier;
- endogenous, bath-coupled, driven-boundary or externally imposed damage classification.

The compiler may continue emitting existing `Event` objects. Keep pair metadata alongside them. Duplicate physical endpoints retain separate flux-accounting mechanisms but aggregate in Q for state-history entropy.

Energy accounting must distinguish stored energy, external work, heat exported and energy held by control hardware. A residual heat calculation verifies bookkeeping; independently check local detailed balance, drive-off stationary equilibrium and representative cycles. A bug must not be made consistent by defining a missing heat bill after the fact.

### 4.3 Preparations and comparisons

`PreparationSpec` declares a root or root distribution, its construction, conservation values, total energy and structured resource inventory. `ComparisonSpec` names:

1. same-law preparation comparison;
2. mechanism contrast between explicitly different laws;
3. physically implemented controller comparison in a common controlled-law family;
4. a physical intervention procedure, including its costs, when actually modeled.

These are not interchangeable. Different static controller wirings induce different Qs. Calling them options does not prove the system can physically switch its wiring. The first controller search compares matched implementations; a later programmable controller needs its memory, reprogramming transitions and bills in the state.

Matching metadata lists what is equal, intentionally changed, measured after the run and not matched. Include material, stored energy, selector energy, source prescription, temperature, density of states, timing, initial locations/contact and apparatus. Same energy alone is not the same endowment.

### 4.4 Subjects, queries and evidence

`SubjectProjection` maps the full physical state to the declared subsystem record. The conditioning remains the encompassing present. Shared resources are not silently awarded to one subject or counted twice in a whole-field sum.

The canonical local projection is `(local material counts, local bank, local selector if present, local sensor/memory registers if present)`. The canonical whole projection includes both pools and the shared resource. A projection that also includes the common resource is a separate, named question, not an unannounced widening of the local subject. Every report stores the resolved coordinate list.

`ContinuationQuery` declares preparation, horizon, cadence, projection, estimator, tolerances and resource budget. Structural monitors use a separate query interface; they do not enlarge the physical entropy alphabet.

Every readout returns value/bounds, units, method, assumptions, numerical residuals, source/query hashes and one of: `resolved`, `bounded`, `statistical`, `unresolved`, `unsupported`, `invalid`.

`AnalysisSpec` identifies explanatory metrics and claim predicates. `RunPlan` identifies the exact cases, source snapshot, execution authorization, resource caps and retained artifacts. The companion [handoff manifest](HANDOFF_PLAN_r2.json) is a design manifest, not an executable science configuration. Every result must also fill the [standard report form](STANDARD_REPORT_FORM_r1.md), including engineering and unresolved outcomes.

## 5. First substrate: two coupled material pools and one resource interface

### 5.1 Scope and state

Use a well-mixed contact model first. Two material pools L and R interact at a common resource interface. Pool labels record local ownership and coupling, not lattice position. This is not a dilute gas model and not a spatial separation test.

Each pool has a fixed number M_c of material slots. Initial species are:

- P: unassembled precursor;
- A: access apparatus;
- B: capture apparatus;
- C: construction-support apparatus.

Store counts `(a_c,b_c,c_c)`; infer `p_c=M_c-a_c-b_c-c_c`. Counts represent material, not moral standing or minds. Each pool has an energy bank `e_c`. The shared resource coordinate is `r in {empty, locked, usable}`. A resource can fluctuate and decay even when no apparatus can use it.

Engineering seed settings:

| Item | Initial setting |
|---|---|
| Inventories | 2+2 primary; 3+1 asymmetry check; total four slots |
| Bank capacity | 1 energy unit per pool |
| Bank quantum | 0.5 initially; 0.25 sensitivity only after size profiling |
| Apparatus internal energy | 0.5 per A/B/C unit |
| P internal energy | 0 |
| Resource energies | empty 0, locked 3, usable 2 |
| Beta | 1 in toy energy units; later 0.5 and 2 |
| Construction bill | 1 bank unit per new apparatus unit |
| Captured bank increment | 1 from a usable packet; full headroom required |

These are executable engineering starting points, not biological calibrations or chosen successes. Sol must publish their resulting state count, timescales and conservation tests before extending the survey. Reuse existing kinetics where the physical transformations agree; do not claim inherited validation when stoichiometry changes.

In this first adapter, each pool's material inventory is separately conserved. Consequently 2+2 versus 3+1 is a **boundary/endowment-allocation contrast**, not two reachable reallocations of the same present. Within a world, construction changes species composition and energy allocation, but does not move material between pools. Testing freely chosen concentration versus distribution requires the material-transport extension in section 12. Do not overstate this first slice as that experiment.

The physical energy and count degeneracy are:

    H(x) = e_L + e_R + 0.5 sum_c(a_c+b_c+c_c) + E_r
    g(x) = product_c M_c! / (p_c! a_c! b_c! c_c!)

Selectors, damage stores and interactions add explicit terms when enabled. Degeneracy participates in the thermal law. It is not added as an extra history-entropy bonus at this count grain.

Before selectors, the product state count is:

    N = choose(M_L+3,3) choose(M_R+3,3) B_L B_R R

At B_L=B_R=3 and R=3: 2+2 gives 2,700 states; 3+1 gives 2,160. One three-mode selector multiplies by 3, two by 9. These are size estimates before reachability and aliases; do not promise runtime from state count alone.

The first selector worlds therefore have 8,100 and 6,480 states. Two selectors have 24,300 and 19,440. Quarter-unit banks have five rather than three states each, increasing these counts by 25/9. Adding an unavailable-material species changes the combinatorial factor to `choose(M_c+4,4)`; do not estimate that extension as one extra Boolean flag.

### 5.2 Canonical reversible-pair construction

For an unordered admissible edge {x,y}, choose the canonical forward orientation once. Let W_xy be external work into the system and deltaH=H(y)-H(x). A valid generic pair implementation is:

    R_xy = (g(y)/g(x)) exp(beta * (W_xy - deltaH))
    q_xy = k_xy sqrt(R_xy)
    q_yx = k_xy / sqrt(R_xy)

Here `k_xy=k_yx` is one symmetric edge conductance and `W_yx=-W_xy`. Do not enumerate the pair twice. If using mass-action propensities instead, show they satisfy the same ratio under the declared combinatorics. Use stable log calculations and reject overflow rather than clipping physical rates.

Catalysts multiply conductance in both directions. A catalyst can change throughput without changing the equilibrium ratio. If its abundance differs at the two endpoints, use an explicitly symmetric conductance; do not apply the forward state's count separately in each direction and accidentally insert a drive.

For drive-off tests, turn off external source channels and external damage, retain bath and reversible internal channels, and verify `pi proportional to g exp(-beta H)` on each relevant closed class. Driven operation need not satisfy global detailed balance.

### 5.3 Mechanisms and seed conductances

All conductances below are per declared edge in the canonical construction. They are not asserted to reproduce the older mass-action constants numerically.

| Module | Physical transformation | Seed conductance / condition |
|---|---|---|
| Native resource fluctuations | empty <-> locked; empty <-> usable | 0.002 each, W=0, present in every arm |
| Maintained source | empty <-> locked | 0.08, forward W=3, reverse W=-3; separate from the bath channel |
| Native unlocking | locked <-> usable | 0.002, no apparatus required |
| Access assistance | same locked <-> usable edge | extra `0.1 * effective_A**alpha`, both directions |
| Basal capture | usable + bank headroom <-> empty + one bank unit | 0.002 per pool |
| Capture assistance | same capture pair | extra `0.1 * local_B**alpha` |
| Paid construction | local P + one bank unit <-> local A/B/C | basal 0.0001 plus `0.008 * effective_parent**alpha` |
| Thermal assembly | local P <-> local A/B/C | 0.00001, no bank consumption; energy supplied/returned by bath |
| Disassembly/reassembly | local A/B/C <-> P | extra reversible conductance 0.002; no missing reverse |
| Apparatus-associated overhead | bank e <-> e-0.5 | conductance `0.01 * local_apparatus_count`; inverse is retained |
| Bank background | bank e <-> e-0.5 | conductance 0.002 independent of apparatus |

Rates are determined by the pair law, not these conductances alone. At capacity, reject invalid transformations rather than diverting missing mass or energy. Capturing a packet dissipates its unretained energy. The first slice has no partial capture; adding it later changes the law and requires explicit reverse endpoints.

Overhead is an apparatus-associated dissipative coupling, **not protective maintenance**. Do not label it repair. Paid reconstruction restores apparatus after disassembly; a later worn-state module will distinguish repairing a damaged unit from making a new one. The reversible disassembly/reassembly pair is not a monotone damage knob: increasing its conductance accelerates both directions. External damage and its irreversible version require the separate damage module.

### 5.4 Recursive enabling and cross-pool composition

The construction graph is A assists B, B assists C, C assists A. For child i in pool c:

    effective_parent = n_parent,c + lambda * n_parent,other

Use alpha=1 initially and alpha=0.5 as a shape sensitivity. The assisting type is unchanged by a construction event, making the multiplier symmetric on that edge. Lambda represents contact-mediated assistance available at the common interface; it is not remote sensing. Lambda=0 removes cross-pool construction assistance, but the pools still compete for the shared resource and are therefore not fully independent.

A assists resource unlocking, B helps capture, and all three participate in the construction cycle. C's role is consequential through constructing further A. The loop is:

    access -> capture -> paid construction -> more enabling apparatus -> access

For unlocking the common resource, `effective_A = a_L + a_R`; it is a shared-interface reaction, counted once, not once per observer. For capture, B assistance is local to the bank receiving the packet. Cross-pool assistance in construction is partitioned into local and contact-mediated catalytic mechanisms. When alpha is sublinear, allocate the total assisted conductance between eligible parent pools in proportion to their nonnegative weighted counts, with zero assistance at total count zero. This decomposition sums to the specified unmarked rate. It is an implementation mark for queries, not a new entropy outcome or an identified parent molecule.

Four slots permit a seed-connected A -> B -> C -> A witness. Four occupied slots do not themselves demonstrate this history. The query must distinguish assisted construction from thermal assembly and use the existing conservative ancestry machinery or a validated generalization.

The well-mixed cross-pool assistance is a coarse chemical contact assumption. A later spatial adapter must replace it with contact, transport and encounter mechanics; it must not inherit a free all-to-all multiplier.

### 5.5 Preparations

Include at least these explicit roots for both inventory arrangements where valid:

- Seed: one A in L, banks (0.5,0), locked packet, all remaining material P.
- Unassembled energy-matched root: all P, banks (1,0), locked packet.
- Mirror seed: exchange L/R and their inventories when testing symmetry.

The first two both have H=4 and the same material and source prescription, but their stored energy is distributed differently. State this; it is precisely a preparation comparison. Do not call the unassembled root an equilibrium gas.

For an additional thermal reference, define an energy-shell or canonical count ensemble explicitly. A canonical ensemble will generally not have exactly the seed's energy. If it is not energy-matched, report it as a different reference rather than calling the matching automatic. A mixture of fixed-energy roots is scored by average conditional histories, without root-selection entropy.

## 6. Paid control, added after the physical world works

### 6.1 First controller slice

Start with one physical selector in L and passive R. Its three modes are `idle`, `access`, `build`; all have equal stored energy and equal degeneracy. This avoids importing an initial mode-energy refund advantage. It does not delete switching entropy.

Modes allocate an **additional fixed catalytic budget per local apparatus type** between its functions. Idle allocates none; access allocates A's controllable capacity to unlocking and B's to capture, leaving C's unused; build allocates A's to B construction, B's to C construction and C's to A construction. The default additional capacity equals that type's existing autonomous assistance coefficient for the selected function. Thus the allocated fraction is either zero or one per type, and no type receives its full controllable budget simultaneously on two functions. This is a matched capacity allocation, not a claim that unlike reactions consume equal work. Autonomous and basal mechanisms remain present.

For alpha=1 the coefficients act directly on the contributing pool's parent count. For alpha=0.5 use the same pool contribution weights defined in section 5.4; do not change the aggregate nonlinear law by independently taking the square root in each pool. A selector redirects only the controllable contribution attributable to its local apparatus. Cross-pool assistance supplied by R remains autonomous until R has its own selector. Pair symmetry must still hold after every allocation multiplier is applied.

The additional control is embodied: its command conductance is proportional to local working apparatus, zero when none is present. A command changes mode and spends 0.5 bank energy; its physical inverse refunds that amount. Native policy-independent mode relaxation at conductance 0.002 remains in both directions even with no working apparatus. It prevents a dead controller from retaining policy-dependent command activity while not freezing a special residual setting by fiat.

Seed command conductance is 0.02 per working unit. Audit the complete command pairs with all modes and bills enabled. Reissuing the current mode is not a counted abstract event. If an actual reset or futile payment is modeled, it must change physical state and receive its own mechanism definition.

The first observation is whether local apparatus count is below 2 or at least 2. Command changes leave that observation unchanged. Enumerate all 3^2=9 stationary response tables, including the three constants. The state contains the selector, not the table lookup operation. This is idealized state-dependent physical kinetics, not a paid perceptual memory model.

The observation restriction matters: when a command spends bank energy, a rule conditioned on that same bank can accidentally give its reverse a different conductance. Later observations must either remain invariant over command endpoints or use an explicit sensor/memory mechanism with its own inverse physics.

### 6.2 Required controller controls

Compare every candidate with:

1. the same selector and policy commanding idle;
2. the best constant command in the declared family;
3. a sham selector with the same command implementation but no catalytic coupling;
4. a held selector, explicitly a mechanism contrast disabling command transitions;
5. the best candidate already evaluated, with uncertainty and search scope shown.

The sham has matched mechanism settings, not necessarily matched realized switching flux: downstream occupancy can change its activity. Report that difference. No subtraction of sham entropy enters the objective.

Use command conductance multipliers 0.5, 1 and 2 and bill 0.25/0.5 in a later diagnostic slice. The finer bill requires a finer energy grid. Do not enlarge the full survey automatically. Re-evaluate all candidates in a small family or label finalist-only results as a robustness check, not a new exhaustive optimum.

### 6.3 What an oracle search means

The offline oracle knows the transition law, not the future random realization. It chooses a stationary physical implementation separately for each horizon. This is not receding-horizon replanning and not a proof of an optimum over arbitrary policies.

Do not maximize a sum of scores from several horizons unless that composite objective is separately requested and justified. Each horizon produces its own comparison and optimizer set. Maximizing ell at a fixed query is equivalent to maximizing L there.

Declare the policy family before each comparison batch for reproducibility. It can be enlarged in subsequent batches. Report the exact number of candidates, distinct generators, evaluated candidates, excluded candidates and unresolved ties.

Use identical-Q detection, but retain differences in physical ledgers, labels and query semantics where applicable. A Q alias permits reuse of full-state entropy; it does not automatically permit reusing mechanism-attribution results.

### 6.4 Paired scope optimization: required from the first controller family

Evaluate the **same candidate implementations once**, then optimize the resulting table under two objective columns. For each fixed law, root, endowment, horizon, cadence and physical information interface:

    Pi_whole = argmax_pi ell_whole(pi)
    Pi_local = argmax_pi ell_L(pi)

The only changed selection criterion is the subject projection. Hardware, candidate family, information access, action channels, source and initial physical state remain matched. Different chosen policies induce different Qs; this is a common encompassing controlled-law comparison, not an assertion that every arm has identical Q.

Report both optimizer sets, not only one tie-broken table. Re-evaluate the selected implementations on both objectives and all structural readouts. With uncertainty, retain candidate sets compatible with the data and report pairwise intervals. Distinguish a resolved opposite preference from overlapping optimizer sets, a common optimum, and an unresolved private ranking.

For a selected whole winner w and local winner l, report:

    whole scope gap = ell_whole(w) - ell_whole(l)
    local scope gap = ell_L(l) - ell_L(w)

When exact maxima exist these gaps are nonnegative **by optimization**, so their nonnegativity is not evidence for the thesis. The empirical content is whether they are strictly positive, which physical choices differ, and what those choices do to access, persistence, reconstruction and the other pool. A scope difference may be driven by selector noise; do not automatically describe it as protection or domination.

In the two-controller extension, first hold the other controller to the same declared implementation while changing the focal controller's objective. Joint whole-field optimization, a local optimizer controlling both parties, and a game of independently optimizing controllers are different experiments. Give each its own comparison id. Do not grant extra control rights to the whole-field optimizer and attribute the resulting advantage to scope alone.

### 6.5 Embodiment levels and a paid sensor substage

The offline enumeration is a scientific instrument; its computer runtime is not a physical decision process occurring inside this toy. Do not charge the simulated world an arbitrary share of research-computer electricity. Conversely, do not call an externally selected stationary table a fully modeled deliberating optimizer. Physical execution is inside the field; in-world search, learning and reprogramming remain later mechanisms.

Every arm carries an embodiment manifest with `represented`, `idealized` or `absent` for: selector register, sensor, memory, communication, command work/refunds, controller upkeep, controller damage, policy storage and in-world computation. Include every represented coordinate and physical bill in the whole-field score. Keep the manifest and the local projection identical across the paired scope experiment.

Split M3 into two engineering substages:

- **M3a:** the existing nine-table direct-kinetic observation model. This is the computational and physical-command benchmark. Sensing is idealized and that limitation remains in its claim.
- **M3b:** add one physical sensor bit z in L. The table reads z, not the actual apparatus count. The target reading is `z*=1[local apparatus >=2]`. All nine response tables retain the same stored-bit observation interface. This adds a factor of two to the state count: 16,200 states for 2+2 and 12,960 for 3+1 before other extensions.

For a concrete M3b implementation, add a paid correction pair from an incorrect z to z*, consuming 0.5 from the local bank. Its exact reverse flips the bit back and refunds the bill. Use the existing canonical pair law, equal bit energies/degeneracies, and seed correction conductance `0.02 * local working count`. Apparatus count is unchanged across this pair, so the target and conductance are well defined for the inverse. Guard on bank headroom and funding. Without working apparatus there is no powered correction.

Retain unbiased native bit relaxation, conductance 0.002 in each direction, independent of the policy. The correct reading is not imposed deterministically or continuously. Paid commands read the stored bit, which they do not change; this keeps their inverse guard coherent. The bit, its correction/refund events and its relaxation all count. Initialize it to the same declared physical state in both scope arms, rather than giving each arm a free optimal memory preparation.

Initially this is an explicit, fuel-consuming coarse sensor, not a microscopic measurement model. Add no compulsory positive housekeeping bill merely to look realistic. Any separate upkeep claim must specify what the spending physically maintains. The existing bank/actuator overhead remains represented and reported; the minimal bit has update cost and native loss of accuracy, with no additional refresh benefit asserted. If a protected memory/refresh mechanism is later added, model that relation and its costs together.

Run a sensor-sham control with the same bit, relaxation and upkeep prescription but a fixed correction target independent of apparatus. Call this a nontracking-target control, not automatically an uninformative bit: apparatus-dependent update speed may still carry information. Measure the resulting statistical dependence. Its realized update rate and occupancy may differ: report that rather than claiming exact activity matching. An activity-matched, empirically uninformative sensor control is an additional calibrated comparison.

Measure sensing accuracy, lag, correction/refund counts, accepted work and functional outcomes. Repeat the paired scope analysis under this shared sensor implementation before making a claim that survives paid sensing. The M3a result remains valid within its stated idealization; it is not retroactively discarded. No full M3b survey launches before its enlarged-state smoke/profile fits the execution budget.

## 7. Independent control, sharing and appropriation

This is the next milestone, not an alternative bespoke toy. Add a selector to R and extend the physical action vocabulary with share and extract. All compared policies must inhabit the same extended world, including its available thermal modes.

Before claiming domination, instantiate:

- productive apparatus in both pools and material that each can lose;
- a real transfer benefit to the controlling pool, compared with its actual alternatives;
- the other pool's downstream construction/recovery consequences;
- common source and energy accounting;
- a declared local history projection for each pool and full-field history.

### 7.1 Transfer module contract

A resource transfer is a physical pair, not a sign on a reward. For payload u and handling bill c, a candidate extraction event has:

    e_S -> e_S-u
    e_D -> e_D+u-c

with an explicit mechanism requiring donor payload, D's ability to pay c, receiver capacity and working actuation. Stored-energy change is -c; export c as heat when no other energy store changes. Include the exact inverse and its thermodynamic ratio. A concerted event may be used at this coarse grain, but document the upfront-payment guard. A later charged-pump intermediate must reproduce or deliberately refine it, not silently add free energy.

The share event pays its bill from the giving pool and transfers payload to the receiving pool. It is not called cooperation merely because a mode has that name. Verify measured net directions. If forward/reverse pairs alias another named action, say so and do not count two choices.

Use rational c values with 0<c<u for a potentially profitable extraction path; start u=0.5, c=0.25 on the quarter-unit grid. Material profitability is an outcome against the matched comparator, not guaranteed by positive per-event payload. Bidirectional turnover, reduced native capture and opportunity cost can change the result.

Do not require ten victims to balance the books. Population aggregation is a later test. First map the existing two-pool transfer budget, gross/net flux and payback.

### 7.2 Policy family and compute gate

For two controllers, publish independent response tables and action sets. Start with the nine-table reserve family per controller before adding every new command, then a compact explicitly listed transfer family. A factorial 5-mode family must not launch accidentally.

Cross-pool observations such as neighbour reserve, bank headroom and contact are allowed only with declared physical coupling. At this stage state-dependent rate rules are idealized; paid sensing is a subsequent module. Never claim that information is free in nature because this adapter reads a coordinate.

Exhaustively enumerate a genuinely small family when feasible. If it is not feasible, report a search over evaluated candidates and its stopping rule. Statistical screening cannot certify an exhaustive optimum without valid bounds covering discarded candidates.

### 7.3 Comparisons and evidence

For each relevant pair, independently report:

    delta ell_L, delta ell_R, delta ell_whole
    delta owned energy, apparatus, reconstruction and access for each pool

Local histories need not sum to the whole; shared dependence is part of the result. A gain in one and a loss in another is not itself the whole-field verdict.

Map effects as cross-assistance, transfer bill, recoverability and source supply change. Do not define a favourable complementarity threshold from observed rankings and then use the same threshold as a premise protecting the thesis.

Include genuine zero-coupling diagnostic worlds only by removing *all* shared interactions, including the common resource bottleneck. Lambda=0 alone is not such a world.

Separate matched-work and matched-event-count comparisons. Calibrate realized matching by a named observable and tolerance, not by choosing a parameter value with the desired entropy. Where exact matching is infeasible, report the residual and the unmatched comparison.

## 8. Structural analysis: mandatory beside scalar results

Every comparison has an automated mechanism sheet answering: what changed, what depends on it, how it is paid for, what repairs or substitutes for it, what it enables next, and what survives its loss.

### 8.1 Access and enabling

Report resource-state occupancy, capture rates, accepted source work, gross/net bank flows, births by mechanism, assisted construction, thermal construction and disassembly. Distinguish enabled reachability, actual probability of use and realized flow. Basal routes can make reachability identical while assistance changes probabilities and timescales substantially.

For a named capability, return:

- physical predicate or transition set defining its availability;
- probability of reaching it by each horizon;
- first-passage distribution where finite;
- occupancy and usable flux;
- dependency graph and specified module ablations.

These are explanatory readouts, not a universal scalar access multiplier. A graph edge alone is not proof of a productive feedback loop.

### 8.2 Recursive enabling

Generalize the existing query-side three-link monitor to named species and pools. Report separately:

- conservative seed-connected depth-three probability;
- depth-three plus retained enabling structure on the same path;
- any-start completed-chain count/rate, with overlap convention;
- construction caused by native assistance channels versus basal construction;
- loop-cut effects on unlabelled material, access and continuation.

If interchangeable counts cannot identify an ancestor, retain a conservative bound or report non-identifiability. Do not assign arbitrary parent identities and call the result genealogy. A three-type cycle supplies type dependencies, not unique individual ancestry.

Monitors may augment a query process. Summing their distributions must recover the original physical marginal. Entropy is always computed on the original physical state. Assistance-event marks help describe an implementation; corroborate their consequences with unmarked physical outcomes and matched ablations.

### 8.3 Persistence, harm and recovery

Report functional uptime, interruption durations, unconditional recovery probability, endpoint recovery, first return and its durability. Reaching a state once is not retaining it. A body that failed before a pulse cannot be excluded from the recovery denominator.

Define structural closure by graph reachability to a declared functional set. In the first reversible world it may be empty. Report `no irreversible closure in this law`, not perfect protection.

Two subsequent modules add genuinely different harm:

1. `Worn`: recoverable nonfunctional material, with a paid repair edge distinct from new construction.
2. `Unavailable`: material/capability permanently removed from productive reachability, with external damage/heat accounting.

Maintain shock hazard and effect as separate parameters. Reversible wear, costly repair, loss of repair machinery, substitution and permanent loss are different laws. Damage events count in history entropy.

A pulse can be a deterministic external intervention query, explicitly outside autonomous policy comparisons, or a physical stochastic hazard within the world. Do not mix those meanings. Apply its material/energy bill and account for the pulse's own outcomes where stochastic.

### 8.4 Funding and compounding

Report accepted external work, captured bank energy, bank changes, construction spending, selector spending/refunds, overhead, heat and thermal rebuilding separately. Gross capture/build ratio is a useful flow ratio, not a certificate that a particular joule funded its descendants.

Without provenance states, source attribution is an accounting convention or an intervention contrast. Label it. Do not use a flow ratio above one as a universal definition of generativity. Capacity four tests bounded enabling/renewal; an expanded cap tests a longer bounded expansion. Neither proves unbounded compounding.

### 8.5 Mechanism decomposition

Declare a coordinate chain-rule order, initially: shared resource, L material, R material, L bank, R bank, L selector, R selector, L sensor, R sensor; omit absent fields explicitly. Show whole-history entropy separately from coordinate shares. A chain-rule share conditioned on the full past is not the marginal history entropy of that subject.

Event-family counts, expected native destination surprisal and coordinate entropy are distinct readouts. Do not call the fraction of events due to switching the fraction of entropy caused by switching. Attribute causally through a matched mechanism intervention, with changed downstream behaviour acknowledged.

### 8.6 Equal-score rebuilding assay

Build the query interface in M2; run an informative assay once reconstruction, loss and substitution supply genuinely different rebuilding structures. Start with a small named family of preparations under one law, with matched total material, energy, source and controller implementation. Differences may include which assisting type is redundant, how precursor is distributed, or which recovery dependency is present. Do not label two different local inventories reachable rearrangements before transport exists.

Search for pairs whose finite-history ell is close at a declared selection query, then examine rebuilding outcomes and continuation profiles. Preserve the whole search table and the selection rule. This is an adversarial/equivalence search, so data-guided pair selection is legitimate when disclosed; do not present its discovery as an independent prediction.

Three outcomes must be distinct:

1. **Exact equality:** established analytically or by a justified symmetry at the declared query.
2. **Resolved approximate equality:** the full difference interval lies inside a separately declared equivalence band, in bits. Report the corresponding maximum perplexity ratio `2^epsilon_equiv`.
3. **Unresolved difference:** the interval merely crosses zero. This does not establish a tie or compression failure.

Choose and document the equivalence band before selecting pairs; it is a scientific resolution criterion separate from numerical solver error. If no pair qualifies, report that without widening the band silently.

For a qualifying pair, report unconditional recovery, reconstruction time, capability availability, retained function and structural closure. Test whether the equality persists at longer horizons and other cadences, and whether the recovery mechanism was already reachable under the original native law. A new imposed disaster is a new boundary/intervention comparison; its consequences cannot be retroactively charged to the original no-disaster query.

A tie in one scalar at one horizon does not imply equal continuation structures or refute the claim that their downstream effects enter full-history lushness. Conversely, if a physically relevant distinction is compressed away throughout the declared comparison, retain that limitation rather than adding a reconstruction bonus. The report names the exact sufficiency claim being challenged and the scope of the equality established.

## 9. Measurement and numerical requirements

### 9.1 Full histories and rates

Use sparse Q and streamed `exp(Q delta)` blocks to obtain row entropies. Reuse rows across preparations and horizons. Use dyadic occupation propagation for the supported T/delta grids; fall back to a general finite propagator for unsupported values without changing the horizon.

Compute root-conditioned recurrent-class rates for reducible worlds. An offset is reported only if its asymptotic definition and numerical convergence are supported. Same finite irreducible Q implies a common stationary rate; it does not force equal finite histories. Different policies may induce different Q and different rates.

For `ell_i(T) ~= h_i T+b_i`, a horizon-crossing estimate is `(b_2-b_1)/(h_1-h_2)` when defined. Verify relevant crossings against finite profiles. Do not apply that approximation while a transient or source shutdown invalidates it. Functional persistence is a distribution, not automatically equivalent to a single mean exceeding this estimate.

### 9.2 Temporal profile

For each key comparison compute sparse versions of:

    Nbar_T = integral_0^T E[q(X_t)] dt
    F_T = integral_0^T E[q(X_t) log2(e)
                   - sum_j q_Xtj log2(q_Xtj * tau0)] dt
    ell(T,delta) = Nbar_T log2(tau0/delta) + F_T + o(1)

Use aggregated state-changing Q rates. Fix tau0 in metadata. F is reference-dependent and is not an organization score. Predicted cadence crossings are asymptotic estimates, not exact certificates; verify them with sampled-history calculations when practical. Equal Nbar cancels the leading divergence but does not prohibit a coarser-cadence reversal.

The entropy of a random-length jump sequence is not the sum of local destination surprisals. Report `H(N_T)` and event-order entropy conditioned on count only if actually computed/bounded. Otherwise mark that decomposition unsupported and report the correctly named available diagnostic.

### 9.3 Local histories

For pool c, the target is:

    H(Y^c_1,...,Y^c_n | X_0=x), Y^c=projection_c(X)

Never fit a Markov chain on the merged coordinates and call it this quantity unless lumpability and the necessary initialization conditions are established.

Use three levels:

1. Exact short-prefix enumeration on tiny calibration worlds.
2. Deterministic lower/upper history bounds on all candidates where affordable.
3. Known-model hidden-state filtering on sampled native histories for unresolved leading comparisons, validated against level 1.

The sampled estimator uses actual marginal sequence likelihoods; it must not reward empirical histogram sparsity. Preserve projection semantics, conditioning and the complete hidden law. Record sampling seeds, batches, effective precision and whether an interval is deterministic or statistical.

Adaptive refinement targets overlapping candidates. Use independent confirmation samples after selection, or a valid sequential interval procedure. Do not keep peeking at ordinary confidence intervals until they exclude zero. Paired seeds require covariance-aware difference intervals; same seed alone is not a variance guarantee. Declare the comparison family and multiplicity treatment.

Stop honestly at unresolved if the allocated budget cannot separate the candidates. Engineering a narrower interval is useful; it does not authorize changing the scientific comparison.

### 9.4 Error contract

Separate integration error, entropy-row truncation, tail bounds, linear-solver residuals and Monte Carlo uncertainty. Probability conservation alone is not an entropy error bound. For a distribution approximation with total-variation bound eta on m outcomes, use a valid entropy-continuity bound or an explicitly justified tighter method.

A result is certified only if its difference interval excludes zero after propagated deterministic errors. Otherwise give a numerical estimate with convergence evidence, or a statistical interval, using the correct label. Strict tolerance values come from calibration and the error budget, not from the margin observed in a preferred comparison.

Initial engineering tolerances may use per-edge energy residual 1e-12 in toy units, normalized generator row residual 1e-12, and log forward/reverse-ratio residual 1e-10. Scale these against floating-point operations and conditioning, and record any revision. The dense/streamed tiny-world calibration should agree within 1e-8 bits before larger-world profiling. These are engineering checks, not certificates of that accuracy for every later history. Numerical evidence must travel with the result.

## 10. Staged implementation and first study plan

Each milestone produces a brief `ENGINEERING.md` entry with measured size, runtime, peak memory, numerical quality and scope. Scientific outcomes do not gate engineering acceptance.

| Milestone | Implement | Acceptance evidence | Do not add yet |
|---|---|---|---|
| M0: contracts and audit | Named schema, reaction-pair metadata, comparison records, source snapshot | Legacy outputs unchanged on tiny fixtures; round-trip serialization; pair tests | General plugin framework |
| M1: productive physics | Two pools, resource interface, cycle, rational banks, native thermal baseline | Conservation, reverses, dark equilibrium, native SSA/Q agreement, state counts | Optimizer or population labels |
| M2: analysis | Finite histories, structural monitors, rates, temporal coefficients, reference roots | Dense/streamed agreement on small world; monitor projection; complete report | Claims about ethical behaviour |
| M3: paid control | M3a one selector/nine tables; M3b paid sensor; paired local/whole selection in each | Paid switching/sensing audits; matched rights and hardware; local-history precision; cost profile | Full two-controller action Cartesian product |
| M4: scope conflict | Second selector, transfer mechanisms, local-history inference | Actual transfer budget; exact/filter calibration; resolved or honestly unresolved local comparisons | Spatial confinement or revolt |
| M5: structure expansion | Worn/unavailable modules, complementarity/redundancy, source windows, equal-score rebuilding assay | Closure/recovery validation; certified equivalence versus unresolved distinctions; matching | A claim of open-ended ecology |

### 10.1 Engineering smoke, when separately authorized

Begin with inventory 1+1 solely for equations and solver checks; it cannot demonstrate a three-link cycle. Then compile 2+2 and 3+1 and run one controlled finite-profile smoke under caps. Retain the intended four-slot scientific world; do not quietly substitute the small validation world if resources are insufficient.

Required smoke outputs: state/edge counts, maximum exit rate, sparse matrix bytes, row-block allocation, compile time, finite-profile time, peak process-tree memory, source import paths and hash, conservation/detailed-balance residuals, and a complete numerical-result record. A timeout is a compute finding, not a theory result.

### 10.2 First physics study, after authorization and feasibility review

Start at alpha=1, lambda=1, beta=1 with the seed conductances above. Include:

- full loop;
- C-to-A assistance removed in both directions;
- all construction assistance removed, preserving basal/bath routes;
- access assistance removed, preserving native locked-resource fluctuations.

Evaluate seed and unassembled roots under each law, T=16/64/256/1024 and the three cadences where feasible. Publish finite profiles and rates together. These mechanism ablations are between-law comparisons; their paired roots are same-law comparisons.

Then map one axis at a time: source conductance 0.02/0.08/0.32, assistance multiplier 0.25/1/4, alpha=0.5/1, and beta=0.5/1/2. Do not start a full Cartesian sweep. Add an explicit interaction slice if single-axis results identify a mechanism worth separating. Preserve every evaluated point and disclose data-guided additions.

Both signs are meaningful. The seed can lose to assembly activity from an unassembled start. The loop can function but produce less total breadth. A positive rate does not prove robustness. A positive preparation offset does not establish a sustained rate difference under one mixing law.

### 10.3 Controller study

At a physically characterized law, run the nine-table family with all required controls. Examine the best finite-history policy by horizon, not just the largest stationary rate. Replaying the same policies across source/assistance conditions distinguishes changed occupancy from changed preferred response.

The next transfer family must be listed explicitly in its own configuration. Its objective is a map of local/whole agreements and disagreements, not a mandated altruistic winner. Before spending heavily on subjective ranking, ensure the substrate actually permits materially profitable extraction and productive alternatives.

## 11. Compute, storage and reproducibility

### 11.1 Preflight and scheduling

This workstation exposed 24 logical processors and about 1.58 TiB free on C: during the specification pass. RAM queries were denied, so available memory was **not established**. Sol must read current available memory through a supported method or require an explicit configured limit before choosing concurrency. Free disk does not replace RAM for exponentiation or filtering.

Initial engineering settings: one worker, 2 GiB process-tree cap, 180-second small smoke. A separately reported four-slot profile may use 4 GiB and 600 seconds after its memory estimate fits. These are conservative initial budgets, not permanent limits. No full batch starts automatically after a smoke.

For later surveys choose workers from measured per-worker peak memory, available RAM with OS headroom, and CPU. Start with BLAS/OpenMP threads limited to one per worker; benchmark alternatives rather than multiplying both worker and thread counts. Measure aggregate memory. Keep a configurable global cap in addition to per-worker caps. Checkpoints permit interruption without a final monolithic allocation.

Preflight includes N, nnz(Q), exit-rate range, estimated semigroup cost, projected-state group sizes, monitor expansion factor, number of distinct Qs, and estimated total hours. N alone is insufficient: fast rates/stiffness and hidden-state group sizes can dominate.

Never allocate dense N-by-N matrices by accident. A single double matrix at N=24,300 is about 4.40 GiB before copies. Streaming blocks reduce memory, not necessarily arithmetic. Memory maps on HDD are cache storage, not a promise that random-access filtering will run efficiently.

If exact analysis exceeds the budget, the fallback order is: reuse common operators; reduce live blocks; schedule fewer workers; profile the backend; use a declared validated sampled/bounded analysis. Reducing the physical world changes the experiment and must be a new manifest with reduced scope.

### 11.2 Cache identities

Retain existing `semantic_keys` compatibility. A new layered cache may distinguish:

- law/compiler key -> Q, physical index and event metadata;
- law + cadence + solver key -> sampled entropy rows/transition blocks;
- law + preparation + horizon key -> occupations;
- projection/monitor + query key -> readouts;
- comparison and interpretation version -> report.

Changing interpretation must not rebuild Q. Changing physical reaction code must invalidate it. Roots share kernel calculations; horizons share occupation work. Cache permissions and checksums are validated before reuse.

### 11.3 Artifacts and cleanup

Keep compact manifests, configurations, source snapshots or immutable reconstructable source bundles, environment versions, seeds, numerical summaries, interpretation revisions and reconstruction recipes. Use JSON for metadata, typed tables for compact results, NPZ for small arrays and chunked formats only when justified by access patterns.

Do not store raw trajectories by default. Keep sufficient statistics, selected diagnostic traces and exact reproduction seeds. Source snapshots must include uncommitted code actually used; a Git hash alone is insufficient.

Large Q/P arrays, transition blocks, long traces and regenerable monitor matrices live under the existing ignored local-runs tree. Set an initial cache budget of 20 GiB, configurable after profiling, and a minimum-free-space floor. The first study must not consume the disk simply because space is available.

Cleanup operates only on manifest-listed artifacts whose dependencies and reconstruction recipe are present. Skip pinned runs, cited indispensable artifacts and all unique input material. Resolve and validate every path under the cache root; do not follow junctions/symlinks outside it. Use the existing artifact index and log each deletion. Rebuild a small selected artifact and compare compact results before treating a new artifact class as disposable.

Numerical recomputation may not be byte-identical across BLAS/platform changes. Preserve exact input hashes; compare reconstructed numerical results with declared tolerances, plus hashes where bit reproducibility is actually guaranteed. Never delete source, manuscript attachments or handoff notes as cache.

No unattended cleanup daemon or scheduled automation is part of this implementation. Provide `cache plan` and `cache evict` commands under explicit storage policy. No automatic commits, pushes or Drive uploads.

## 12. Expansion interfaces and limits

| Expansion | Interface prepared now | What must be implemented before making the stronger claim |
|---|---|---|
| More population | Named species/pool counts, inventories as parameters | State-size profiling; labelled two-unit comparison and lumpability/physical-grain audit; no assumption count entropy equals labelled-history entropy |
| More capacity | Material conservation and source ledger | Matched resource/boundary comparisons; clarify fixed endowment versus growing external supply; no unbounded-growth claim from caps 4/6/8 |
| Reachable concentration/distribution | Explicit conservation groups and local occupancy constraints | Add empty sites and material transport so local inventories can change under one law; pay transport and construction costs |
| Differentiated ecology | Species dependency graph and reaction modules | Generalist/self-assisting controls with equal material and explicit catalytic budgets, not a diversity reward |
| Redundancy/substitution | Multiple mechanisms implementing one capability | Damage/repair tests and specified independent/correlated failures |
| Cross-scale composition | Pool/assembly relation metadata and query predicates | Actual assembly/disassembly transitions, interaction energy, nested resource bills; no free macro-agent label |
| Space | Contact graph and module support | Locations, transport, encounter rates and costs; spatial state entropy and density controls; face the prior lattice reversal directly |
| Genuine gas reference | Native resource/background module and preparation interface | Mobile same-law physical adapter; count-mixture results do not settle gas comparisons |
| Paid sensing/memory | Observation declarations separated from policy tables | Physical sensor states, update channels, memory costs and coupling to control |
| Bounded control | Solver-independent physical kernel and query API | Receding-horizon/partially observed protocols distinct from current stationary oracle search |
| ML controllers | Serializable observation/action implementation contracts | Training/evaluation split, equal implementation budgets, held-out laws, constrained physical actuation; no entropy of software action labels |
| Quantum/relativistic frame adapters | Measurement and conditioning metadata separated from CTMC code | A separately justified quantum instrument/history construction; do not treat every quantum family as one classical Q |

For the first future labelled/count audit, distinguish two questions: whether aggregated dynamics are Markov/lumpable, and whether a chosen physical identity distinction adds legitimate history entropy. Strong lumpability answers the first only.

For the first transport extension, a useful bounded construction is three sites per pool but four total material units, with vacancy V distinct from precursor P. Movement exchanges a material unit with a vacancy through a reversible, possibly powered channel. The total four-unit inventory is conserved while 2+2 and 3+1 become reachable allocations under one law. Update energy, degeneracy and contact rates for this state space; do not keep the original formula inferring P from a fixed local material inventory. Profile the enlarged world before any search. This is the prerequisite for a direct optimization claim about concentrating or distributing the same matter.

The architecture should accept an empirical body or controller only through its actual interactions. Do not reserve a privileged `valuer=true` flag that changes the score. Optional annotations can describe the model's intended interpretation without entering Q or the objective.

## 13. Required tests

Write tests for real physical and inferential failure modes, not every field getter.

1. **Legacy preservation:** selected old tiny generators, entropy rows and reported balances remain unchanged.
2. **Rational bills:** exact representability, boundary headroom, inverse endpoints; reject off-grid inputs with a useful grid-refinement estimate.
3. **Material/energy:** every event and full trajectory ledger; source/refund/heat signs; no missing apparatus or selector store.
4. **Thermodynamics:** pair ratios, reverse presence, dark equilibrium and catalytic acceleration preserving ratios, including every controller mode.
5. **Outcome aggregation:** splitting one rate into duplicate event labels leaves Q and full-state entropy unchanged; a genuinely new physical outcome can change them.
6. **Relabelling:** pool/species/state permutation commutes with compilation, projections and comparisons when physical parameters are permuted too.
7. **Sampler consistency:** native SSA uses the same events as Q; endpoint/flux estimates agree with exact propagation within statistical error on small fixtures.
8. **History solvers:** dense versus streamed finite entropy; all roots; absorbing/reducible examples; precision improvement; no hidden tail deletion.
9. **Projected histories:** exact short words versus filter/bounds; an explicitly non-Markov projection catches naive lumped-chain substitution.
10. **Depth/robustness:** witness cannot restart secretly; query marginal recovers native law; retained-depth is a joint event; unconditional recovery includes pre-pulse failure.
11. **Control embodiment:** no apparatus means no paid commands, while native relaxation remains; any residual policy dependence is reported and traced.
12. **Comparison semantics:** matched-root energy including selector; root-ensemble entropy excluded; mechanism and preparation contrasts labelled correctly.
13. **Resource limits:** cap hit kills the child tree, writes incomplete receipt, preserves checkpoints; stale statuses cannot launch work.
14. **Cache safety:** physical-source change invalidates Q; report-only change does not; manifest-listed path checks and reconstruction prerequisite prevent unsafe eviction.
15. **Scope pairing:** changing only the objective column leaves the candidate kernels, root, action rights, observation interface and budgets unchanged; score both selected sets under both projections.
16. **Paid sensor:** bit included in projections and entropy; no perfect live-state leak to the table; funding and inverse pairs verified; zero apparatus removes powered correction, not native relaxation.
17. **Equivalence:** an interval crossing zero is not an equivalence certificate; an imposed hazard is not silently part of an earlier law; pair selection and confirmation queries remain identifiable.
18. **Report contract:** every run has the six mandatory manuscript fields, a named comparator, query status and claim/comparator applicability check, including incomplete and unsupported runs.

## 14. Files and implementation handoff

Suggested new code organization, subject to small adjustments for existing conventions:

    omega_v2/testbed/ecology/
      schema.py             # named physical coordinates and conservation
      pairs.py              # reversible pairs and thermodynamic audit metadata
      world.py              # aggregate adapter -> existing WorldSpec
      preparations.py       # matched roots and declared reference ensembles
      controllers.py        # physical implementations and finite table families
      studies.py            # resolved cases and comparison graph
    omega_v2/testbed/modules/
      ecology_resource.py
      ecology_construction.py
      ecology_damage.py     # later milestone, not an empty placeholder module
      ecology_transfer.py   # later milestone
    omega_v2/testbed/analysis/
      ecology_structure.py
      comparison_records.py
    scripts/
      run_generative_ecology.py
      generative_ecology_worker.py
      report_generative_ecology.py
    tests/
      test_ecology_physics.py
      test_ecology_control.py
      test_ecology_queries.py
      test_ecology_workflow.py

Reuse existing analyses rather than copying them into these files. Keep a single native event source for exact and sampled execution. Expose importable functions as well as CLI entry points so a future training environment can call the physical kernel without parsing reports.

Required handoff artifacts from implementation:

- `MODEL.md`: actual equations, units, rates, costs and implemented scope;
- `ENGINEERING.md`: profile, limitations and milestone completion;
- `REPRODUCE.md`: exact source/config commands and environment;
- machine-readable complete case/comparison tables and query status;
- `RESULTS.md`: numerical findings with uncertainty and all controls;
- `INTERPRETATION.md`: mechanisms, correspondence to claims, remaining gaps, clearly dated revisions;
- a reconstruction manifest for every disposable artifact class.

The report's first page should answer: **what organization won at which horizon, what physical channel made the difference, whether it remains after activity/energy controls, and what we can and cannot conclude about possible valuing.** Do not lead with the number of forecast checkboxes passed.

Use [STANDARD_REPORT_FORM_r1.md](STANDARD_REPORT_FORM_r1.md) to generate that page from structured records. Every run states the mechanism, ranking, parameter relationship, comparison kind, horizon and what was challenged. A single parameter point must say that a relationship has not yet been mapped. A run stopped by a cap must not emit a scientific winner.

Each claim record includes its comparator and applicability conditions. Examples: a preparation-head-start claim needs matched roots under the same law; a sustained mechanism rate contrast needs the declared mechanism ablation and boundary/work controls; a scope claim needs matched candidate rights with a changed subject; a compression claim needs an established equivalence rather than a wide uncertainty interval. Lack of a rate difference is not a negative verdict on a finite-profile/offset claim.

Provisional manuscript destinations, following the supplied outline references: organization/disorder chapter 12; persistence/compounding chapter 14; activity chapter 15; cooperation chapter 19; domination chapter 20; plurality chapter 22; hard cases chapter 31; model definitions Appendix C. Scope pairing also bears on chapter 4. Store stable claim/topic identifiers separately from chapter numbers, so renumbering changes presentation rather than source data. These references are a handoff map, not edits to the manuscript or a claim that its current text was verified.

## 15. Definition of a successful first delivery

Sol should deliver a verified, bounded four-slot productive ecology, with native background fluctuations, physical reconstruction and three-link assistance; reusable whole-history and structural analysis; and a profiled path to the nine-policy embodied controller slice. The code must support further pools/species/modules without changing the meaning of existing measurements.

The first delivery is successful whether its scientific comparison is positive, negative or unresolved. The engineering must expose that answer without silently removing noise, adding welfare rewards, conflating local shares with local histories, rewarding a hidden selector energy store, or counting analysis labels as physical futures.

The subsequent two-controller experiment then asks a stronger question in the same world: **when physical control redirects the conditions of further generativity, do local and encompassing continuations agree, and where do they diverge?**
