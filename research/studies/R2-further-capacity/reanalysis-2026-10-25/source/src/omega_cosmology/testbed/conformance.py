"""Small transparent M2 cases, kept separate from ethical interpretation."""

import numpy as np

from .history import (
    entropy,
    foreclosure,
    full_state_foreclosure,
    history_profile,
    observed_history_law,
    refinement_certificate,
    strong_lumpability,
)


def run_reference_cases():
    records = []

    def record(id, source, residual, statement, guarantee="numerical_reference"):
        if not np.isfinite(residual) or abs(residual) > 1e-10:
            raise ArithmeticError(f"Conformance identity failed: {id}")
        records.append(
            {
                "id": id,
                "source": source,
                "status": "passed",
                "residual": float(residual),
                "statement": statement,
                "guarantee": guarantee,
            }
        )

    p = np.array([[0.8, 0.2], [0.3, 0.7]])
    mu = np.array([1.0, 0.0])
    law = observed_history_law(p, mu, [0, 1], 4)
    record(
        "chain_rule",
        "A.2.1",
        entropy(list(law.values())) - history_profile(p, mu, 4)[-1],
        "Enumerated full word entropy equals sum of conditional step entropies",
    )

    identity = np.eye(2)
    mixture = observed_history_law(identity, np.array([0.5, 0.5]), [0, 1], 3)
    record(
        "mixture_vs_root_average",
        "A.5.2",
        entropy(list(mixture.values())) - 1.0,
        "Unobserved root creates 1 bit of future uncertainty; each known-root history has zero",
    )

    p4 = np.array([[0, 0, 0.5, 0.5], [0, 0, 1, 0], [0, 0, 1, 0], [0, 0, 0, 1.0]])
    labels = [0, 0, 0, 1]
    prior = np.array([0.1, 0.9, 0, 0])
    own = float(entropy(list(observed_history_law(p4, prior, labels, 2).values())))
    point0 = float(
        entropy(
            list(observed_history_law(p4, np.array([1.0, 0, 0, 0]), labels, 2).values())
        )
    )
    point1 = float(
        entropy(
            list(observed_history_law(p4, np.array([0.0, 1, 0, 0]), labels, 2).values())
        )
    )
    if not point1 < own < point0:
        raise ArithmeticError("Pointwise versus average conditioning distinction lost")
    record(
        "own_vs_full_present",
        "A.7.1",
        own - entropy([0.95, 0.05]),
        "Own-present entropy lies below one compatible full-root entropy and above another",
    )

    hidden = np.array([[1.0, 0, 0], [0, 0, 1], [0.5, 0.5, 0]])
    nonmarkov = strong_lumpability(hidden, [0, 0, 1])
    lumpable = strong_lumpability(np.full((3, 3), 1 / 3), [0, 0, 1])
    if nonmarkov["lumpable"] or not lumpable["lumpable"]:
        raise ArithmeticError("Projection memory check failed")
    record(
        "projection_memory",
        "A.7.3",
        lumpable["residual"],
        "One projection fails strong lumpability; a separate uniform law passes",
    )

    deterministic = np.array([[0.0, 1, 0], [0, 0, 1], [1, 0, 0]])
    record(
        "nontrivial_determinism",
        "A.1 conditioning scope",
        history_profile(deterministic, np.array([1.0, 0, 0]), 12)[-1],
        "Deterministic state changes have ell=0, L=1; this is a discrete reference, not a CTMC limit",
        "analytic_construction_numerically_checked",
    )

    # Same row-entropy constant: all n-step entropies equal n*h by the chain rule.
    a = np.array([[0.8, 0.2], [0.2, 0.8]])
    b = np.array([[0.2, 0.8], [0.8, 0.2]])
    pulse = np.array([[0.0, 1.0], [1.0, 0.0]])
    difference = history_profile(pulse @ a, mu, 8) - history_profile(pulse @ b, mu, 8)
    if abs((pulse @ a)[0, 1] - (pulse @ b)[0, 1]) < 0.5:
        raise ArithmeticError("Different response was erased")
    record(
        "equal_entropy_different_response",
        "scalar compression; no normative inference",
        max(abs(difference)),
        "A common deterministic bit-flip input yields different response probabilities but equal constant row entropy at all horizons",
        "analytic_constant_row_entropy_construction_numerically_checked",
    )

    prior = {("one",): 0.5, ("two",): 0.5}
    changed = {("two",): 1 / 3, ("three",): 1 / 3, ("four",): 1 / 3}
    narrowed = {("one",): 0.9, ("two",): 0.1}
    determined = {("one",): 1.0}
    if (
        foreclosure(prior, narrowed)["reference_weight"] != 0
        or entropy(list(narrowed.values())) >= 1
    ):
        raise ArithmeticError("Contraction without foreclosure lost")
    if (
        foreclosure(prior, changed)["reference_weight"] != 0.5
        or entropy(list(changed.values())) <= 1
    ):
        raise ArithmeticError("Foreclosure without contraction lost")
    record(
        "contraction_foreclosure",
        "A.9.3,A.9.4",
        foreclosure(prior, determined)["reference_weight"] - 0.5,
        "Support loss and entropy contraction differ; a determined allowed future maximally contracts without total foreclosure",
    )
    record(
        "full_support_no_foreclosure",
        "A.9.3 finite support",
        full_state_foreclosure(
            a, np.ones((2, 2), bool), mu, np.array([True, False]), 8
        ),
        "Positive sampled support implies no finite full-state word foreclosure despite probability differences",
    )

    independent = np.full((2, 2), 0.25)
    correlated = np.array([[0.5, 0], [0, 0.5]])
    record(
        "correlated_exterior",
        "A.7.11 finite reference",
        entropy(independent) - entropy(correlated) - 1.0,
        "Both marginals remain fair; a one-bit mutual-information change changes the joint entropy",
    )

    cert = refinement_certificate(2.0, 1.0, refinement="named-two-state-refinement")
    if (
        not cert["certified"]
        or cert["faithfulness"] != "open"
        or cert["governing_status"] != "provisional"
    ):
        raise ArithmeticError("Certification and faithfulness were conflated")
    record(
        "named_refinement",
        "A.6.5,A.6.6",
        cert["margin"] - 1.0,
        "A certificate can cover a specified unverified refinement while governing status stays provisional",
    )

    record(
        "nonacting_register",
        "A.8.2",
        entropy([0.5, 0.5]) - 1.0,
        "An independent fair register adds one bit per sampled step even without action; no physical cost claim in this algebraic example",
    )
    # Both local entropies tie; whole-field gap comes exclusively from dependence.
    record(
        "self_whole_correlation",
        "A.7.6",
        entropy(independent.sum(axis=1)) - entropy(correlated.sum(axis=1)),
        "A local marginal ties while the joint entropy differs through correlations alone",
    )
    return records
