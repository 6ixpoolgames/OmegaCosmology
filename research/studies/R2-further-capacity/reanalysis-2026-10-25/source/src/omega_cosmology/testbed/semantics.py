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
    if law.adapter != "finite_local_ctmc":
        raise ValueError("This query adapter supports finite classical CTMCs only")
    return {
        "status": "validated_contract",
        "physical_sufficiency": "declared_not_empirically_proved",
        "model_hash": law.physical_model_hash,
        "quantity": quantity.id,
    }
