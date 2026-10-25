# Coupled autocatalytic engineering smoke

25 October 2026. Five cases and ten full-profile queries complete. This is a
physics/analysis/computational smoke, not a parameter survey or a scientific
ranking of ecological strategies. Original R2-v1 evidence is unchanged.
Specification: [engineering slice](../../specs/COUPLED_AUTOCATALYTIC_SLICE_SPEC_r1.md).

## What was exercised

| Case | States | Seconds | Peak MiB |
|---|---:|---:|---:|
| shared_pair | 432 | 3.535 | 180.13 |
| repaired_capacity | 180 | 1.317 | 126.23 |
| three_member_cycle | 72 | 1.014 | 155.00 |
| cross_assistance_pair | 432 | 3.536 | 180.21 |
| source_off_pair | 432 | 3.435 | 180.05 |

Cadence .25; horizons 4 and 16. Total 12.900 s, peak
180.21 MiB,
run output 575,740 bytes. Largest shared-pair case gated the
rest. Caps: 150 s/3 GiB/32 MiB per case; 600 s/128 MiB batch.

## Physical changes

R2-v2 adds store breakdown/spill at every load and bound-constituent damage
independent of bank. It removes the dissipative-only rule named upkeep. Paid
activation restores damaged constituents; native thermal substitutes remain.
Payment is not made logically necessary. Full-bank storage no longer has
protection through lack of refund space along every breakdown path.

The new blocks compose costed component cycles, distinct banks and one finite
shared carrier. Capturing it changes the other group's opportunity. Additional
cross-assistance uses recipient energy. Every channel has its paired reverse,
source-off Gibbs checks pass, and maximum first-law residual is 8.22e-15.
No conditional moral reward, noise subtraction or activity normalization is used.

## Local histories are actually projected histories

Conditional history of each group's components and bank is bounded under the
known full present. The shared carrier stays in the whole model and is hidden
from these local observations. Finite-memory bounds retain hidden state and
do not assume the projection is Markov. Widths, in bits:

| Case / scope | T16 m1 width | T16 m2 width |
|---|---:|---:|
| shared_pair / A | 0.383084 | 0.336219 |
| shared_pair / B | 0.383084 | 0.336219 |
| three_member_cycle / A | 0.412114 | 0.374284 |
| cross_assistance_pair / A | 0.415153 | 0.367638 |
| cross_assistance_pair / B | 0.415153 | 0.367638 |
| source_off_pair / A | 0.360665 | 0.320164 |
| source_off_pair / B | 0.360665 | 0.320164 |

The lower conditions on an older hidden boundary state plus observed memory;
the upper conditions on observed memory only. Increasing memory is checked to
tighten both. Tiny exhaustive hidden-Markov word laws independently validate
the inequalities. These are float64 evaluations of analytic bounds, not rigorous
interval arithmetic. Positive width is unresolved information, not a local score
estimate. No private/whole conflict or optimal policy is inferred from this smoke.

## Connected native assistance ancestry

| Case / scope | P(ever depth >=3), T16 | Expected births depth >=3 | Query states |
|---|---:|---:|---:|
| shared_pair / A.construction_depth | 0.0031820879 | 0.0033498769 | 3780 |
| shared_pair / B.construction_depth | 0.0031820879 | 0.0033498769 | 3780 |
| three_member_cycle / A.construction_depth | 0.0010632955 | 0.0011218172 | 1611 |
| cross_assistance_pair / A.construction_depth | 0.0030465951 | 0.0032434706 | 3780 |
| cross_assistance_pair / B.construction_depth | 0.0030465951 | 0.0032434706 | 3780 |
| source_off_pair / A.construction_depth | 0.0032637773 | 0.003436064 | 3780 |
| source_off_pair / B.construction_depth | 0.0032637773 | 0.003436064 | 3780 |

Initial instances have depth zero. Newly constructed children can become parents;
basal or unlisted reconstruction resets depth, and loss ends the instance.
Query-only labels preserve the physical marginal. This is actual connectivity
in declared native marked channels, not merely event order. The last count bin
means >=3 and counts assisted births, not independent chains. Small probabilities
at T16 are neither a theory failure nor evidence of long-horizon robustness.

Coupled-case monitors track within-group ancestry. Cross-group assistance
is conservatively treated as an unlisted birth for that local genealogy; the
query is not a complete cross-community pedigree. The one-group three-member
case follows the full local cycle. No material/energy packet ancestry is claimed.

## Boundaries and next assessment

Contacts, banks and slots are fixed; no general population or transport is
represented. Banks are existing local infrastructure, not free new storage.
Capture, construction and damage coefficients are stipulated. Native capture
and thermal repair remain, so these are assisted routes, not exclusive channels.
The reversible source can receive returned work during a transient; source-on
does not guarantee net accepted work at every short horizon. All histories of
source/bath variables outside the model remain unresolved.

The one-group and two-group cases have different inventories and are not
matched competitors. Pair cases share an initial endowment; adding helper
channels or removing source channels changes the law. Mutualism, parasitism,
competition outcomes, repayment windows and ethical correspondence are not
established here. Horizon 16 is a smoke window, not a claim of sufficient
scientific duration. Parameter/cost/source-lifetime maps and matched preparations
are next study design work, after assessing these physical assumptions.

No commit, push or upload performed. All exact input/result hashes are retained;
no dense kernels, generated paths or genealogy-state arrays are stored.
