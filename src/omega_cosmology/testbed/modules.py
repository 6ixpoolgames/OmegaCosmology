"""Explicit coordinate ports for composing the existing local physical grammar.

Bindings add no state, events, entropy or work. They only resolve local names.
This initial contract supports distinct slots and an additive Hamiltonian.
"""

from dataclasses import dataclass, replace

from .physics import Condition, Coordinate, EnergyTerm, LocalModel, Rule, rational


@dataclass(frozen=True)
class Port:
    name: str
    role: str
    domain: tuple[int, ...]
    energy_tick: str | None = None

    def __post_init__(self):
        object.__setattr__(self, "domain", tuple(self.domain))
        Coordinate(self.name, self.domain, self.role)
        if self.energy_tick is not None and rational(self.energy_tick) <= 0:
            raise ValueError("Energy ports need a positive rational tick")


@dataclass(frozen=True)
class Module:
    id: str
    coordinates: tuple[Coordinate, ...] = ()
    ports: tuple[Port, ...] = ()
    rules: tuple[Rule, ...] = ()
    energy: tuple[EnergyTerm, ...] = ()
    forbidden: tuple[tuple[Condition, ...], ...] = ()
    material: tuple[dict, ...] = ()


@dataclass(frozen=True)
class Binding:
    module: Module
    namespace: str
    ports: dict[str, str]


def compose(id, bindings, *, beta=1.0):
    """Bind all modules at once; no implicit bank, carrier or coordinate alias."""
    bindings = tuple(bindings)
    if not bindings or len({b.namespace for b in bindings}) != len(bindings):
        raise ValueError("Distinct nonempty module namespaces required")
    coordinates, mappings = [], []
    for binding in bindings:
        module, namespace = binding.module, binding.namespace
        if not module.id or not namespace:
            raise ValueError("Module and namespace must be named")
        local = [c.name for c in module.coordinates] + [p.name for p in module.ports]
        if len(set(local)) != len(local) or set(binding.ports) != {
            p.name for p in module.ports
        }:
            raise ValueError("Every distinct local port must be bound exactly once")
        if len(set(binding.ports.values())) != len(binding.ports):
            raise ValueError("Aliased ports need an explicit adapter")
        mapping = {c.name: namespace + "." + c.name for c in module.coordinates}
        mapping.update(binding.ports)
        mappings.append(mapping)
        coordinates.extend(
            replace(c, name=mapping[c.name], owner=namespace)
            for c in module.coordinates
        )
    by_name = {c.name: c for c in coordinates}
    if len(by_name) != len(coordinates):
        raise ValueError("Owned module coordinates collide")
    rules, energy, forbidden, material = [], [], [], []
    for binding, mapping in zip(bindings, mappings):
        module = binding.module

        def name(key, mapping=mapping):
            if key not in mapping:
                raise ValueError(f"Undeclared module coordinate: {key}")
            return mapping[key]

        def condition(c):
            return replace(c, coordinate=name(c.coordinate))

        def term(t):
            return replace(
                t,
                coordinate=name(t.coordinate) if t.coordinate else None,
                conditions=tuple(condition(c) for c in t.conditions),
            )

        for port in module.ports:
            target = by_name.get(binding.ports[port.name])
            if (
                target is None
                or target.role != port.role
                or target.domain != port.domain
            ):
                raise ValueError(f"Port {port.name} has incompatible role or domain")
        for rule in module.rules:
            rules.append(
                replace(
                    rule,
                    id=binding.namespace + "." + rule.id,
                    guards=tuple(condition(c) for c in rule.guards),
                    changes=tuple((name(k), v) for k, v in rule.changes),
                    support=tuple(name(k) for k in rule.support),
                    parent=name(rule.parent) if rule.parent else None,
                    child=name(rule.child) if rule.child else None,
                )
            )
        energy.extend(term(t) for t in module.energy)
        forbidden.extend(
            tuple(condition(c) for c in pattern) for pattern in module.forbidden
        )
        for item in module.material:
            if "inventory" not in item:
                raise ValueError("Modules need executable material inventories")
            inventory = []
            for row in item["inventory"]:
                t = term(
                    EnergyTerm(
                        row["coefficient"],
                        row.get("coordinate"),
                        tuple(Condition(**c) for c in row.get("conditions", ())),
                    )
                )
                inventory.append(
                    {
                        "coefficient": t.coefficient,
                        "coordinate": t.coordinate,
                        "conditions": [vars(c) for c in t.conditions],
                    }
                )
            material.append(
                {
                    **item,
                    "id": binding.namespace + "." + item["id"],
                    "inventory": inventory,
                    "exchange_by_rule": {
                        binding.namespace + "." + k: v
                        for k, v in item.get("exchange_by_rule", {}).items()
                    },
                }
            )
    for binding in bindings:
        for port in binding.module.ports:
            if port.energy_tick is not None:
                target = binding.ports[port.name]
                if any(
                    t.conditions
                    and (
                        t.coordinate == target
                        or any(c.coordinate == target for c in t.conditions)
                    )
                    for t in energy
                ):
                    raise ValueError(
                        "Energy port needs an additive, interaction-free tick"
                    )
                tick = sum(
                    (rational(t.coefficient) for t in energy if t.coordinate == target),
                    rational(0),
                )
                if tick != rational(port.energy_tick):
                    raise ValueError("Bound energy port has a different physical tick")
    return LocalModel(
        id,
        coordinates,
        rules,
        energy,
        beta=beta,
        forbidden=forbidden,
        material=material,
    )
