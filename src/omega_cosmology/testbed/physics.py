"""Finite local rule grammar over count coordinates and relational slots."""

from collections import defaultdict
from dataclasses import asdict, dataclass
from fractions import Fraction
from math import exp, isfinite, log

from .semantics import fingerprint


def rational(value):
    return Fraction(str(value))


@dataclass(frozen=True)
class Coordinate:
    name: str
    domain: tuple[int, ...]
    role: str
    owner: str = "shared"

    def __post_init__(self):
        object.__setattr__(self, "domain", tuple(self.domain))
        if (
            not self.name
            or not self.role
            or not self.domain
            or len(set(self.domain)) != len(self.domain)
        ):
            raise ValueError(
                "A coordinate needs a name, role and distinct finite domain"
            )
        if any(type(x) is not int for x in self.domain):
            raise ValueError("The initial adapter uses integer physical state values")


@dataclass(frozen=True)
class Condition:
    coordinate: str
    operator: str
    value: int

    def __post_init__(self):
        if (
            not self.coordinate
            or self.operator not in ("eq", "ge", "le")
            or type(self.value) is not int
        ):
            raise ValueError(
                "A local condition requires a named integer coordinate and supported operator"
            )

    def test(self, state, indices):
        x = state[indices[self.coordinate]]
        if self.operator == "eq":
            return x == self.value
        if self.operator == "ge":
            return x >= self.value
        if self.operator == "le":
            return x <= self.value
        raise ValueError("Unsupported local condition")


@dataclass(frozen=True)
class EnergyTerm:
    coefficient: str
    coordinate: str | None = None
    conditions: tuple[Condition, ...] = ()

    def __post_init__(self):
        object.__setattr__(self, "conditions", tuple(self.conditions))
        rational(self.coefficient)


@dataclass(frozen=True)
class Rule:
    id: str
    guards: tuple[Condition, ...]
    changes: tuple[tuple[str, int], ...]
    conductance: float
    work: str = "0"
    boundary: str = "native"
    support: tuple[str, ...] = ()
    mechanism: str = "unspecified"
    roles: tuple[str, ...] = ()
    parent: str | None = None
    child: str | None = None

    def __post_init__(self):
        object.__setattr__(self, "guards", tuple(self.guards))
        object.__setattr__(self, "changes", tuple(tuple(x) for x in self.changes))
        object.__setattr__(self, "support", tuple(self.support))
        object.__setattr__(self, "roles", tuple(self.roles))
        if len(set(self.roles)) != len(self.roles) or any(
            not isinstance(v, str) or not v for v in self.roles
        ):
            raise ValueError("Rule roles must be distinct nonempty names")
        if (
            not self.id
            or not self.changes
            or len(dict(self.changes)) != len(self.changes)
            or any(type(v) is not int or not v for _, v in self.changes)
            or not isfinite(self.conductance)
            or self.conductance <= 0
        ):
            raise ValueError(
                "A reversible rule needs distinct nonzero changes and positive conductance"
            )
        rational(self.work)


@dataclass(frozen=True)
class Event:
    rule_id: str
    direction: int
    target: tuple[int, ...]
    rate: float
    work: float
    heat: float
    delta_energy: float
    support: tuple[str, ...]
    boundary: str


class LocalModel:
    """One reversible event law consumed unchanged by both numerical backends."""

    def __init__(
        self,
        id,
        coordinates,
        rules,
        energy_terms,
        *,
        beta=1.0,
        forbidden=(),
        degeneracy=(),
        symmetry=(),
        relations=(),
        material=(),
        legacy_material=False,
    ):
        self.id = id
        self.coordinates = tuple(coordinates)
        self.rules = tuple(rules)
        self.energy_terms = tuple(energy_terms)
        self.beta = float(beta)
        self.forbidden = tuple(tuple(x) for x in forbidden)
        self.degeneracy_terms = tuple(degeneracy)
        self.relations = tuple(relations)
        self.material = tuple(material)
        self.material_status = "not_declared" if not material else "executable"
        self._inventories = {}
        self.indices = {c.name: i for i, c in enumerate(self.coordinates)}
        self.domains = tuple(frozenset(c.domain) for c in self.coordinates)
        n = len(self.coordinates)
        identity = tuple(range(n))
        self.symmetry = tuple(tuple(p) for p in symmetry) or (identity,)
        if len(self.indices) != n or len({r.id for r in self.rules}) != len(self.rules):
            raise ValueError("Unique physical coordinates and rule IDs required")
        if not isfinite(self.beta) or self.beta <= 0:
            raise ValueError("Positive finite bath beta required")
        perms = set(self.symmetry)
        if identity not in perms or any(sorted(p) != list(range(n)) for p in perms):
            raise ValueError(
                "Explicit finite symmetry group must include identity and bijections"
            )
        if any(
            tuple(a[b[i]] for i in range(n)) not in perms for a in perms for b in perms
        ):
            raise ValueError(
                "Supply the complete finite symmetry group, not generators alone"
            )
        for p in perms:
            if any(self.domains[i] != self.domains[p[i]] for i in range(n)):
                raise ValueError("Symmetry changes physical domains")
        for rule in self.rules:
            self._validate_conditions(rule.guards)
            if any(k not in self.indices for k, _ in rule.changes) or any(
                k not in self.indices for k in rule.support
            ):
                raise ValueError("Rule references an unknown coordinate")
        for term in (*self.energy_terms, *self.degeneracy_terms):
            rational(term.coefficient)
            self._validate_conditions(term.conditions)
            if term.coordinate and term.coordinate not in self.indices:
                raise ValueError("Energy/degeneracy references an unknown coordinate")
        for pattern in self.forbidden:
            self._validate_conditions(pattern)
        material_ids = set()
        for item in self.material:
            name = item.get("id")
            if not name or name in material_ids:
                raise ValueError("Material declarations require distinct IDs")
            material_ids.add(name)
            if "inventory" not in item:
                if not legacy_material:
                    raise ValueError(
                        "Material conservation requires an executable inventory; prose is not a constraint"
                    )
                self.material_status = "legacy_unverified"
                continue
            terms = tuple(
                EnergyTerm(
                    t["coefficient"],
                    t.get("coordinate"),
                    tuple(Condition(**c) for c in t.get("conditions", ())),
                )
                for t in item["inventory"]
            )
            for term in terms:
                self._validate_conditions(term.conditions)
                if term.coordinate and term.coordinate not in self.indices:
                    raise ValueError("Inventory references unknown coordinate")
            exchanges = item.get("exchange_by_rule", {})
            known = {r.id: r for r in self.rules}
            if any(k not in known or known[k].boundary == "native" for k in exchanges):
                raise ValueError("Material exchange requires a declared boundary rule")
            self._inventories[name] = (
                terms,
                {k: rational(v) for k, v in exchanges.items()},
            )
        for rule in self.rules:
            if rule.parent is not None or rule.child is not None:
                guards = {(c.coordinate, c.operator, c.value) for c in rule.guards}
                changes = dict(rule.changes)
                if (
                    rule.child not in self.indices
                    or changes.get(rule.child) != 1
                    or (rule.child, "eq", 0) not in guards
                ):
                    raise ValueError(
                        "Construction role requires an absent child and a birth"
                    )
                if rule.parent is not None and (
                    rule.parent not in self.indices
                    or rule.parent == rule.child
                    or rule.parent in changes
                    or (rule.parent, "eq", 1) not in guards
                ):
                    raise ValueError(
                        "Assistance role requires a present, preserved parent"
                    )

    def inventory(self, state):
        self.validate(state)
        return {
            k: str(self._value(state, terms))
            for k, (terms, _) in self._inventories.items()
        }

    def audit_material_pair(self, rule, source, target):
        for name, (terms, exchanges) in self._inventories.items():
            before, after = self._value(source, terms), self._value(target, terms)
            if (
                before < 0
                or after < 0
                or after - before != exchanges.get(rule.id, Fraction())
            ):
                raise ValueError(f"Rule {rule.id} violates material inventory {name}")

    def _validate_conditions(self, conditions):
        if any(
            c.coordinate not in self.indices or c.operator not in ("eq", "ge", "le")
            for c in conditions
        ):
            raise ValueError("Unknown coordinate or unsupported condition")

    def valid(self, state):
        return (
            isinstance(state, tuple)
            and len(state) == len(self.coordinates)
            and all(type(v) is int and v in d for v, d in zip(state, self.domains))
            and not any(
                all(c.test(state, self.indices) for c in pattern)
                for pattern in self.forbidden
            )
        )

    def validate(self, state):
        if not self.valid(state):
            raise ValueError(
                "State violates its declared physical domains or constraints"
            )
        if any(
            self._value(state, terms) < 0 for terms, _ in self._inventories.values()
        ):
            raise ValueError("State has a negative material inventory")

    def _value(self, state, terms):
        return sum(
            (
                rational(t.coefficient)
                * (state[self.indices[t.coordinate]] if t.coordinate else 1)
                for t in terms
                if all(c.test(state, self.indices) for c in t.conditions)
            ),
            Fraction(),
        )

    def energy(self, state):
        return self._value(state, self.energy_terms)

    def log_degeneracy(self, state):
        return float(self._value(state, self.degeneracy_terms))

    def orbit(self, state):
        return {tuple(state[p[i]] for i in range(len(state))) for p in self.symmetry}

    def canonical(self, state):
        return min(self.orbit(state))

    def transform(self, state, changes, direction=1):
        values = list(state)
        for k, v in changes:
            values[self.indices[k]] += direction * v
        return tuple(values)

    def rule_dependencies(self, rule):
        """Actual local rate/validity dependencies, including energetic couplings.

        User-supplied support can enlarge this set, but cannot hide a guard,
        target-validity constraint or energetic dependency of the event.
        """
        changed = {name for name, _ in rule.changes}
        dependencies = changed | set(rule.support) | {c.coordinate for c in rule.guards}
        for term in (*self.energy_terms, *self.degeneracy_terms):
            fields = {c.coordinate for c in term.conditions}
            if term.coordinate:
                fields.add(term.coordinate)
            if fields & changed:
                dependencies.update(fields)
        for pattern in self.forbidden:
            fields = {c.coordinate for c in pattern}
            if fields & changed:
                dependencies.update(fields)
        return tuple(c.name for c in self.coordinates if c.name in dependencies)

    def pair_rates(self, rule, source, target):
        self.audit_material_pair(rule, source, target)
        delta = self.energy(target) - self.energy(source)
        lr = (
            self.log_degeneracy(target)
            - self.log_degeneracy(source)
            + self.beta * float(rational(rule.work) - delta)
        )
        forward, reverse = (
            exp(log(rule.conductance) + lr / 2),
            exp(log(rule.conductance) - lr / 2),
        )
        if not all(isfinite(r) and r > 0 for r in (forward, reverse)):
            raise ArithmeticError(
                "Native rates are not representable; no clipping permitted"
            )
        return forward, reverse, delta

    def events(self, state, *, include_drive=True):
        self.validate(state)
        for rule in self.rules:
            if not include_drive and rule.boundary != "native":
                continue
            support = self.rule_dependencies(rule)
            if all(c.test(state, self.indices) for c in rule.guards):
                target = self.transform(state, rule.changes)
                if self.valid(target):
                    f, _, de = self.pair_rates(rule, state, target)
                    w = rational(rule.work)
                    yield Event(
                        rule.id,
                        1,
                        target,
                        f,
                        float(w),
                        float(w - de),
                        float(de),
                        support,
                        rule.boundary,
                    )
            source = self.transform(state, rule.changes, -1)
            if self.valid(source) and all(
                c.test(source, self.indices) for c in rule.guards
            ):
                _, r, de = self.pair_rates(rule, source, state)
                w = rational(rule.work)
                yield Event(
                    rule.id,
                    -1,
                    source,
                    r,
                    -float(w),
                    -float(w - de),
                    -float(de),
                    support,
                    rule.boundary,
                )

    def quotient_log_degeneracy(self, state):
        logs = [self.log_degeneracy(s) for s in self.orbit(state)]
        high = max(logs)
        return high + log(sum(exp(v - high) for v in logs))

    def audit_symmetry(self, state):
        def signature(s):
            values = defaultdict(float)
            for e in self.events(s):
                target = self.canonical(e.target)
                if target != self.canonical(s):
                    values[(target, e.work, e.heat, e.boundary)] += e.rate
            return values

        expected = signature(state)
        for s in self.orbit(state):
            self.validate(s)
            if (
                self.energy(s) != self.energy(state)
                or self.inventory(s) != self.inventory(state)
                or abs(self.log_degeneracy(s) - self.log_degeneracy(state)) > 1e-12
            ):
                raise ValueError(
                    "Declared symmetry changes physical energy, material or degeneracy"
                )
            actual = signature(s)
            if expected.keys() != actual.keys() or any(
                abs(v - actual[k]) > 1e-11 * max(1.0, abs(v))
                for k, v in expected.items()
            ):
                raise ValueError(
                    "Declared symmetry does not preserve aggregate physical event law"
                )

    def record(self):
        def rule_record(rule):
            row = asdict(rule)
            for key in ("roles", "parent", "child"):
                if not row[key]:
                    row.pop(key)
            return row

        return {
            "schema": "omega.local-model/1",
            "id": self.id,
            "beta": self.beta,
            "coordinates": [asdict(c) for c in self.coordinates],
            "rules": [rule_record(r) for r in self.rules],
            "energy_terms": [asdict(t) for t in self.energy_terms],
            "forbidden": [[asdict(c) for c in p] for p in self.forbidden],
            "degeneracy": [asdict(t) for t in self.degeneracy_terms],
            "symmetry": self.symmetry,
            "relations": self.relations,
            "material": self.material,
        }

    def fingerprint(self):
        return fingerprint(self.record())

    @classmethod
    def from_record(cls, value):
        if value.get("schema") != "omega.local-model/1":
            raise ValueError(
                "Unsupported local-model schema; explicit migration required"
            )
        conditions = lambda xs: tuple(Condition(**x) for x in xs)
        terms = lambda xs: tuple(
            EnergyTerm(
                x["coefficient"],
                x.get("coordinate"),
                conditions(x.get("conditions", ())),
            )
            for x in xs
        )
        return cls(
            value["id"],
            [Coordinate(**x) for x in value["coordinates"]],
            [Rule(**{**x, "guards": conditions(x["guards"])}) for x in value["rules"]],
            terms(value["energy_terms"]),
            beta=value["beta"],
            forbidden=[conditions(x) for x in value.get("forbidden", ())],
            degeneracy=terms(value.get("degeneracy", ())),
            symmetry=value.get("symmetry", ()),
            relations=value.get("relations", ()),
            material=value.get("material", ()),
            legacy_material=True,
        )
