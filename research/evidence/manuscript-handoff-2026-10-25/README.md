# Manuscript evidence handoff

25 October 2026. S0 deliverable of the
[ecology scope](../../platform/specs/ECOLOGY_PROGRAMME_SCOPE_r1.md). These are
draft model cards/evidence rows for editorial use. No chapter or Drive file has
been edited. All quoted quantities are log lushness in bits unless stated.

- [R1 model card](R1_MODEL_CARD.md), [R2 model card](R2_MODEL_CARD.md),
  [E1 model card](E1_MODEL_CARD.md).
- [Corrections and diagnostics](CORRECTIONS.md).
- [Claim rows](CLAIMS.json): candidate editorial tiers with explicit limitations.
- Complete numerical profiles: [R1](R1_PROFILES.json), [R2](R2_PROFILES.json),
  [E1](E1_PROFILES.json).1010 profiles total; no physics rerun.
- Complete comparison maps: [R1](R1_COMPARISONS.json),
  [R2](R2_COMPARISONS.json), [E1](E1_COMPARISONS.json).2571 rows total;
  overlapping horizons and contrasts are not independent replications.
- Native models, endowments and preparations: R1_MODEL.json, R2_MODEL.json,
  E1_MODEL.json. [Source hashes](SOURCES.json), [export checks](VALIDATION.json).

Five-item report fields accompany each comparison/profile: finite profile and
applicable long-horizon reading; whole and requested parts; foreclosure status;
present/horizon/cadence/resolution; resolved/unresolved evidence. An uncomputed
field is null with a reason. Unknown foreclosure is not zero foreclosure.
Coordinate shares in retained originals are explanatory, never private entropy.

Editorial mapping is deliberately qualified: whole results are M2 candidates
at their represented model level, with physical faithfulness open. E1 part
intervals may resolve or remain M3 individually. The donor filtering estimates
remain M3 under the manuscript's request for certified signs. Extra cadences
alone cannot upgrade any of these to a physically certified finest grain.

The original protocols supply questions and any prospective expectations. This
packet does not reconstruct guessed signs after seeing outcomes. It states
physical limitations and potentially contrary observations as clearly as gains.
Retained historical evidence not yet replicated on this platform stays historical;
it is not withdrawn automatically.

Rebuild the numerical export into a fresh directory from the repository root:

```text
python scripts/package_manuscript_evidence.py --out-dir research/evidence/handoff-fresh
```

The export script copies numerical fields without recalculation and retains
source row indices/keys and hashes. Narrative cards are reviewed text. Receipt
hashes are in EVIDENCE.json once the packet is finalized. Read SOURCES.json for
the input documents, rather than assuming its newest filename is canonical.
