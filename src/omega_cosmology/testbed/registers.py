"""Reusable payments for physical register reactions in the native rule grammar.

This composes stoichiometry, not rates or a new source. A charged carrier must
already have an energy and native recharge mechanism in the encompassing model.
The compiler generates the exact thermal reverse, including refunds.
"""

from dataclasses import dataclass

from .physics import Condition, rational


@dataclass(frozen=True)
class RegisterPayment:
    bank_bill: str = ".5"
    use_carrier: bool = False

    def terms(self, model, quantum, *, bank="body.bank", carrier="carrier"):
        quantum, bill = rational(quantum), rational(self.bank_bill)
        if quantum <= 0 or bill < 0 or type(self.use_carrier) is not bool:
            raise ValueError(
                "Nonnegative bill, positive quantum and boolean fuel flag required"
            )
        ticks = bill / quantum
        if ticks.denominator != 1:
            raise ValueError("Register bill must be exactly representable in the bank")
        if bank not in model.indices:
            raise ValueError("Payment bank must be physical")
        capacity = max(model.domains[model.indices[bank]])
        if ticks > capacity or (ticks == 0 and not self.use_carrier):
            raise ValueError("A paid reaction must have an affordable physical input")
        guards, changes = [], []
        if ticks:
            guards.append(Condition(bank, "ge", int(ticks)))
            changes.append((bank, -int(ticks)))
        if self.use_carrier:
            if carrier not in model.indices or model.domains[
                model.indices[carrier]
            ] != {0, 1}:
                raise ValueError(
                    "Payment needs an existing binary charged/spent carrier"
                )
            guards.append(Condition(carrier, "eq", 1))
            changes.append((carrier, -1))
        return tuple(guards), tuple(changes)


def paid_register_rule(rule, model, payment, quantum, *, variable_changes):
    """Replace a payment explicitly while keeping guards unrelated to payment."""
    from dataclasses import replace

    guards, changes = payment.terms(model, quantum)
    # Callers supply the retained sensing/state guards, avoiding an implicit
    # claim that this adapter can infer which old guards were payment guards.
    return replace(
        rule, guards=rule.guards + guards, changes=tuple(variable_changes) + changes
    )
