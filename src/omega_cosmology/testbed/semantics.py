"""Six public metadata records; no physical law is supplied by these records."""

import json
from dataclasses import asdict, dataclass, field
from hashlib import sha256
from math import isfinite
from typing import Any


def fingerprint(value):
    return sha256(
        json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            allow_nan=False,
        ).encode()
    ).hexdigest()


class Record:
    def record(self):
        return asdict(self)

    def fingerprint(self):
        return fingerprint(self.record())


@dataclass(frozen=True)
class PresentSpec(Record):
    id: str
    roots: tuple[tuple[tuple[int, ...], float], ...]
    conditioning: str = "full_present"
    section: str = "synchronous_classical_state"
    sufficiency: str = ""
    hidden_root_provenance: str | None = None
    version: str = "1"

    def content_fingerprint(self):
        """Identity of conditioning, not its editable display name or prose."""
        return fingerprint(
            {
                "roots": sorted(self.roots),
                "conditioning": self.conditioning,
                "section": self.section,
                "hidden_root_provenance": self.hidden_root_provenance,
            }
        )

    def __post_init__(self):
        object.__setattr__(
            self, "roots", tuple((tuple(s), float(p)) for s, p in self.roots)
        )
        if (
            not self.id
            or not self.sufficiency
            or self.section != "synchronous_classical_state"
        ):
            raise ValueError(
                "A supported section and explicit sufficient-state argument are required"
            )
        if self.conditioning not in (
            "full_present",
            "root_conditioned_average",
            "unobserved_root_mixture",
            "own_present",
        ):
            raise ValueError("Unknown present conditioning")
        if (
            not self.roots
            or len({s for s, _ in self.roots}) != len(self.roots)
            or any(not isfinite(p) or p <= 0 for _, p in self.roots)
            or abs(sum(p for _, p in self.roots) - 1) > 1e-12
        ):
            raise ValueError(
                "Distinct roots with normalized positive probabilities required"
            )
        if self.conditioning == "full_present" and len(self.roots) != 1:
            raise ValueError("An exact full present has one root")
        if self.conditioning == "own_present" and not self.hidden_root_provenance:
            raise ValueError(
                "Own-present conditioning requires the hidden-root law provenance"
            )


@dataclass(frozen=True)
class LawSpec(Record):
    id: str
    physical_model_hash: str
    boundary: dict[str, Any]
    conserved: tuple[str, ...] = ()
    adapter: str = "finite_local_ctmc"
    version: str = "1"

    def __post_init__(self):
        if not self.id or not self.physical_model_hash or not self.boundary:
            raise ValueError(
                "Law identity and physical boundary prescription are required"
            )


@dataclass(frozen=True)
class ObservationSpec(Record):
    id: str
    coordinates: tuple[str, ...]
    scope: str = "whole_modeled_field"
    conditioning: str = "full_present"
    resolution: dict[str, Any] = field(
        default_factory=lambda: {
            "faithfulness": "open",
            "certification": [],
            "reversal": "none",
            "governing_status": "provisional",
        }
    )
    version: str = "1"

    def __post_init__(self):
        object.__setattr__(self, "coordinates", tuple(self.coordinates))
        if (
            not self.id
            or not self.coordinates
            or len(set(self.coordinates)) != len(self.coordinates)
        ):
            raise ValueError("Distinct named observation coordinates are required")
        if self.scope not in ("whole_modeled_field", "projected_history"):
            raise ValueError("Scope must name the modeled field or a projection")
        if self.resolution.get("faithfulness") not in ("open", "established"):
            raise ValueError("Physical faithfulness must be explicit")
        if self.resolution.get("certification") and not all(
            all(k in c for k in ("refinement", "bound", "margin", "method"))
            for c in self.resolution["certification"]
        ):
            raise ValueError("A certificate must identify its refinement and bound")


@dataclass(frozen=True)
class ComparisonSpec(Record):
    id: str
    kind: str
    horizon: float
    cadence: float
    matched: dict[str, Any]
    implementation: str = ""
    common_present: str | None = None
    invariance_status: str = "required_unproved"
    orientation: str = "adapter_forward"
    version: str = "1"
    common_present_hash: str | None = None

    def __post_init__(self):
        if self.kind not in ("single_query", "preparation", "mechanism", "process"):
            raise ValueError("Unknown comparison kind")
        if (
            not self.id
            or not self.matched
            or any(not isfinite(x) or x <= 0 for x in (self.horizon, self.cadence))
        ):
            raise ValueError(
                "Positive finite horizon/cadence and matching statement required"
            )
        if abs(self.horizon / self.cadence - round(self.horizon / self.cadence)) > 1e-9:
            raise ValueError("Horizon must contain a whole number of sampled intervals")
        if self.kind == "process" and (
            not self.common_present or not self.implementation
        ):
            raise ValueError(
                "A process contrast needs a common present and physical implementation"
            )


@dataclass(frozen=True)
class QuantitySpec(Record):
    id: str
    definition: str
    units: str
    conditioning: str
    version: str = "1"
    functional: str = "sampled_history_entropy"

    def __post_init__(self):
        if not all((self.id, self.definition, self.units, self.conditioning)):
            raise ValueError("Quantity definition, units and conditioning are required")


@dataclass(frozen=True)
class EvidenceSpec(Record):
    id: str
    method: str
    guarantee: str
    source_versions: tuple[str, ...]
    uncertainty: dict[str, Any]
    scope: str
    version: str = "1"

    def __post_init__(self):
        if self.guarantee not in (
            "analytic",
            "numerical_full_model",
            "rigorous_bound",
            "statistical",
            "heuristic",
            "unsupported",
        ):
            raise ValueError("Unknown evidence guarantee")
        if not all(
            (self.id, self.method, self.source_versions, self.uncertainty, self.scope)
        ):
            raise ValueError(
                "Evidence method, assumptions and precision must be explicit"
            )


def validate_query(present, law, observation, comparison, quantity):
    if quantity.functional != "sampled_history_entropy" or quantity.units != "bits":
        raise ValueError(
            "History evaluator requires the sampled-history entropy functional in bits"
        )
    if (
        present.conditioning != observation.conditioning
        or quantity.conditioning != present.conditioning
    ):
        raise ValueError("Present, observation and quantity conditioning disagree")
    if comparison.kind == "process" and comparison.common_present != present.id:
        raise ValueError("Process comparison uses a different present")
    if (
        comparison.kind == "process"
        and comparison.common_present_hash != present.content_fingerprint()
    ):
        raise ValueError(
            "Process query requires the actual common-present content hash"
        )
    if law.adapter != "finite_local_ctmc":
        raise ValueError("This query adapter supports finite classical CTMCs only")
    return {
        "status": "validated_query_contract",
        "comparison_status": "not_validated_without_both_arms",
        "conservation_declaration": "descriptive_only_use_executable_model_inventory",
        "physical_sufficiency": "declared_not_empirically_proved",
        "model_hash": law.physical_model_hash,
        "quantity": quantity.id,
    }


def validate_comparison(
    comparison, left, right, *, state_mapping=None, require_material=False
):
    """Validate both executable arms, rather than trust matching prose.

    Each arm supplies compiled, present, law, observation, quantity and its
    own comparison/window. Current adapter requires a common named coordinate
    grammar; coordinate renamings require an explicit future mapping adapter.
    """
    if type(require_material) is not bool:
        raise ValueError("Material requirement must be explicit Boolean")
    mapping_record = None
    if state_mapping is not None:
        from .state_mapping import ConstraintStateMapping

        if (
            not isinstance(state_mapping, ConstraintStateMapping)
            or comparison.kind != "mechanism"
            or any(
                arm["observation"].scope != "whole_modeled_field"
                for arm in (left, right)
            )
        ):
            raise ValueError(
                "Explicit constraint mappings require a full-state mechanism contrast"
            )
        mapping_record = state_mapping.verify(left["compiled"], right["compiled"])
    if comparison.kind == "single_query":
        raise ValueError("A single query is not a paired comparison")
    for arm in (left, right):
        compiled = arm["compiled"]
        compiled.require_complete()
        validate_query(
            arm["present"],
            arm["law"],
            arm["observation"],
            arm["comparison"],
            arm["quantity"],
        )
        if arm["law"].physical_model_hash != compiled.model_hash:
            raise ValueError("Comparison arm does not execute its declared law")
        window = arm["comparison"]
        if (window.horizon, window.cadence, window.orientation) != (
            comparison.horizon,
            comparison.cadence,
            comparison.orientation,
        ):
            raise ValueError("Comparison windows differ")
        for root, _ in arm["present"].roots:
            compiled.model.validate(root)
            if compiled.model.canonical(root) not in compiled.index:
                raise ValueError("Comparison root outside compiled law")
        names = tuple(c.name for c in compiled.model.coordinates)
        observed = arm["observation"]
        if any(k not in names for k in observed.coordinates) or (
            observed.scope == "whole_modeled_field"
            and set(observed.coordinates) != set(names)
        ):
            raise ValueError(
                "Comparison observation omits or invents physical coordinates"
            )
    for name in ("observation", "quantity"):
        a, b = left[name].record(), right[name].record()
        # Human-readable identity and description do not determine the quantity.
        for k in ("id", "definition"):
            a.pop(k, None)
            b.pop(k, None)
        if a != b:
            raise ValueError("Comparison observations/quantities differ")
    if left["law"].boundary != right["law"].boundary:
        raise ValueError(
            "Boundary prescriptions differ; not a matched-boundary comparison"
        )
    lp, rp = left["present"], right["present"]
    lm, rm = left["compiled"].model, right["compiled"].model
    if (lp.conditioning, lp.section, lp.hidden_root_provenance) != (
        rp.conditioning,
        rp.section,
        rp.hidden_root_provenance,
    ):
        raise ValueError("Present conditioning differs")
    if comparison.kind == "preparation":
        if lm.fingerprint() != rm.fingerprint():
            raise ValueError("A preparation contrast must use one law")
    else:
        if lp.content_fingerprint() != rp.content_fingerprint():
            raise ValueError("Process/mechanism arms require the same physical present")
        a, b = lm.record(), rm.record()
        for k in ("id", "rules"):
            a.pop(k)
            b.pop(k)
        if a != b and mapping_record is None:
            raise ValueError(
                "Physical grammar/endowment differs; explicit mapping required"
            )

    def endowments(model, present):
        values = {}
        for root, weight in present.roots:
            key = (
                str(model.energy(root)),
                tuple(sorted(model.inventory(root).items())),
            )
            values[key] = values.get(key, 0.0) + weight
        return values

    a, b = endowments(lm, lp), endowments(rm, rp)
    if a.keys() != b.keys() or any(abs(a[k] - b[k]) > 1e-12 for k in a):
        raise ValueError("Energy/material endowment distributions differ")
    if (
        lm.material_status == "legacy_unverified"
        or rm.material_status == "legacy_unverified"
    ):
        raise ValueError(
            "Matched material claim needs executable inventory definitions"
        )
    if require_material and (
        lm.material_status != "executable"
        or rm.material_status != "executable"
        or not lm.material
        or not rm.material
        or any(not item.get("inventory") for item in (*lm.material, *rm.material))
    ):
        raise ValueError(
            "Material-required comparison needs nonempty executable inventories"
        )
    if (
        comparison.kind == "process"
        and comparison.common_present_hash != lp.content_fingerprint()
    ):
        raise ValueError("Paired process has a different common present")
    return {
        "status": "validated_paired_comparison",
        "kind": comparison.kind,
        "left_model": lm.fingerprint(),
        "right_model": rm.fingerprint(),
        "left_present": lp.content_fingerprint(),
        "right_present": rp.content_fingerprint(),
        "state_mapping": mapping_record,
        "material_endowment": "declared_executable_totals_checked"
        if lm.material and rm.material
        else "not_declared_not_certified",
        "material_inventory_scopes": {
            item["id"]: item.get("inventory_scope", "declared_inventory_only")
            for item in lm.material
        },
        "process_enactment": "declared_requires_encompassing_process_audit"
        if comparison.kind == "process"
        else "not_a_process_contrast",
        "scope": "Declared finite grammar/endowment checked; exterior cancellation and physical faithfulness not established",
    }
