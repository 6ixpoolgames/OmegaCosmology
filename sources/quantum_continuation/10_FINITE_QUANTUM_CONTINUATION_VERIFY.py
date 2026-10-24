#!/usr/bin/env python3
"""Exact finite checks for the Omega continuation-object formalization.

Python 3.10+, standard library only. All matrix arithmetic is over Q(i).
This verifies the worked instances, not the general proofs or physical claims.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
import json
from pathlib import Path


@dataclass(frozen=True)
class G:
    """Gaussian rational; no floating-point conversion is used."""
    re: F = F(0)
    im: F = F(0)

    @staticmethod
    def lift(x):
        return x if isinstance(x, G) else G(F(x))

    def __add__(self, other):
        z = G.lift(other)
        return G(self.re + z.re, self.im + z.im)

    __radd__ = __add__

    def __neg__(self):
        return G(-self.re, -self.im)

    def __sub__(self, other):
        return self + (-G.lift(other))

    def __mul__(self, other):
        z = G.lift(other)
        return G(self.re*z.re-self.im*z.im, self.re*z.im+self.im*z.re)

    __rmul__ = __mul__

    def conj(self):
        return G(self.re, -self.im)

    def __bool__(self):
        return bool(self.re or self.im)

    def __str__(self):
        if not self.im:
            return str(self.re)
        return f"({self.re})+({self.im})i"


Z0, ONE, II = G(), G(F(1)), G(F(0), F(1))


def zeros(n, m=None):
    return [[Z0 for _ in range(n if m is None else m)] for _ in range(n)]


def mat(rows):
    return [[G.lift(x) for x in row] for row in rows]


def eye(n):
    a = zeros(n)
    for i in range(n):
        a[i][i] = ONE
    return a


def dag(a):
    return [[a[j][i].conj() for j in range(len(a))] for i in range(len(a[0]))]


def trans(a):
    return [list(row) for row in zip(*a)]


def mm(a, b):
    if len(a[0]) != len(b):
        raise ValueError("matrix dimension mismatch")
    c = zeros(len(a), len(b[0]))
    for i, row in enumerate(a):
        for k, x in enumerate(row):
            if x:
                for j, y in enumerate(b[k]):
                    if y:
                        c[i][j] = c[i][j] + x*y
    return c


def add(a, b):
    return [[x+y for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def scale(a, x):
    return [[y*x for y in row] for row in a]


def kron(a, b):
    return [[a[i][j]*b[k][l] for j in range(len(a[0])) for l in range(len(b[0]))]
            for i in range(len(a)) for k in range(len(b))]


def trace(a):
    return sum((a[i][i] for i in range(len(a))), Z0)


def outer(v):
    v = [G.lift(x) for x in v]
    return [[x*y.conj() for y in v] for x in v]


def real(z):
    if z.im:
        raise ValueError(f"non-real exact result: {z}")
    return z.re


def expect(rho, effect):
    return real(trace(mm(rho, effect)))


def bits(i, n):
    return tuple((i >> (n-1-k)) & 1 for k in range(n))


def index(bs):
    out = 0
    for b in bs:
        out = 2*out+b
    return out


def ptrace(a, keep, n):
    keep = tuple(keep)
    lose = tuple(k for k in range(n) if k not in keep)
    out = zeros(2**len(keep))
    for i in range(2**n):
        bi = bits(i, n)
        for j in range(2**n):
            bj = bits(j, n)
            if all(bi[k] == bj[k] for k in lose):
                u, v = index(bi[k] for k in keep), index(bj[k] for k in keep)
                out[u][v] = out[u][v]+a[i][j]
    return out


def permutation(n, fn):
    u = zeros(2**n)
    for i in range(2**n):
        u[index(fn(list(bits(i, n))))][i] = ONE
    return u


def cnot_bits(b):
    b[1] ^= b[0]
    return b


def toffoli_bits(b):
    b[2] ^= b[0] & b[1]
    return b


I2 = eye(2)
X = mat([[0, 1], [1, 0]])
Y = mat([[0, -II], [II, 0]])
Z = mat([[1, 0], [0, -1]])
P0 = mat([[1, 0], [0, 0]])
P1 = mat([[0, 0], [0, 1]])
PX = scale(add(I2, X), F(1, 2))
PY = scale(add(I2, Y), F(1, 2))
PROJECTORS = [P0, P1, PX, PY]
PAULIS = [I2, X, Y, Z]
CNOT = permutation(2, cnot_bits)
TOFFOLI = permutation(3, toffoli_bits)
V = zeros(8, 4)
for _i in range(4):
    V[2*_i][_i] = ONE  # append actuator |0>


def embed(rho):
    return mm(mm(V, rho), dag(V))


def evolve(rho):
    return mm(mm(TOFFOLI, embed(rho)), dag(TOFFOLI))


def measure_prepare(rho, pu, pv):
    # A(|i><j|) = (Pu)_{j i} Pv, retaining the memory block.
    memory = zeros(2)
    for i, j in product(range(2), repeat=2):
        block = [[rho[2*i+m][2*j+n] for n in range(2)] for m in range(2)]
        memory = add(memory, scale(block, pu[j][i]))
    return kron(pv, memory)


def effect_pullback(output_effect, pu=None, pv=None):
    e = mm(mm(dag(TOFFOLI), output_effect), TOFFOLI)
    if pu is not None:
        # Adjoint of the measure/prepare operation on S only.
        b = zeros(4)
        for i, j in product(range(2), repeat=2):
            block = [[e[4*i+m][4*j+n] for n in range(4)] for m in range(4)]
            b = add(b, scale(block, pv[j][i]))
        e = kron(pu, b)
    return mm(mm(dag(V), e), V)


def hvec(a):
    if a != dag(a):
        raise ValueError("real span requires Hermitian operators")
    return [x.re for row in a for x in row] + [x.im for row in a for x in row]


class RationalSpan:
    """Incremental exact row elimination over Q."""
    def __init__(self):
        self.rows = {}

    def reduce(self, vector):
        v = list(vector)
        for p in sorted(self.rows):
            if v[p]:
                c = v[p]
                v = [x-c*y for x, y in zip(v, self.rows[p])]
        return v

    def add(self, vector):
        v = self.reduce(vector)
        p = next((i for i, x in enumerate(v) if x), None)
        if p is None:
            return False
        c = v[p]
        self.rows[p] = [x/c for x in v]
        return True

    def contains(self, vector):
        return not any(self.reduce(vector))

    def __len__(self):
        return len(self.rows)


def op_span(ops):
    s = RationalSpan()
    for a in ops:
        s.add(hvec(a))
    return s


def process_matrix(rho, full_output=False):
    """One intervention on S; order: final output, S_out, S_in.

    rho_out = Tr_slot[R (I tensor J(A)^T)].
    Built from matrix-unit responses, independently of the Gram certificate.
    """
    dout = 8 if full_output else 2
    r = zeros(dout*4)
    for o, p, i, j in product(range(2), repeat=4):
        sm = zeros(4)
        for m, n in product(range(2), repeat=2):
            sm[2*o+m][2*p+n] = rho[2*i+m][2*j+n]
        y = evolve(sm)
        f = y if full_output else ptrace(y, (2,), 3)
        a, b = 2*o+i, 2*p+j
        for u, v in product(range(dout), repeat=2):
            r[4*u+a][4*v+b] = f[u][v]
    return r


def comb_apply(r, j):
    dout = len(r)//4
    out = zeros(dout)
    for u, v in product(range(dout), repeat=2):
        out[u][v] = sum((r[4*u+a][4*v+b]*j[a][b]
                         for a, b in product(range(4), repeat=2)), Z0)
    return out


def gram_process(components, full_output=False):
    """Positive certificate: a positive weighted sum of exact outer products."""
    dout = 8 if full_output else 2
    out = zeros(4*dout)
    count = 0
    for weight, psi in components:
        if weight <= 0:
            raise ValueError("Gram weight must be positive")
        w = [Z0 for _ in range(32)]
        for o, i, m in product(range(2), repeat=3):
            source = index((o, m, 0))
            for f in range(8):
                w[4*f+2*o+i] = w[4*f+2*o+i] + TOFFOLI[f][source]*psi[2*i+m]
        parts = [w] if full_output else [
            [w[4*(2*q+a)+slot] for a in range(2) for slot in range(4)]
            for q in range(4)]
        for part in parts:
            if any(part):
                count += 1
                out = add(out, scale(outer(part), weight))
    return out, count


def stationary_closure():
    # H is stored unnormalized; conjugation is H E H / 2, exactly rational.
    h0 = mat([[1, 1], [1, -1]])
    phase = mat([[1, 0], [0, II]])
    swap = permutation(2, lambda b: [b[1], b[0]])
    gates = [(kron(h0, I2), F(1, 2)), (kron(phase, I2), F(1)),
             (CNOT, F(1)), (swap, F(1))]
    s = RationalSpan()
    basis = []
    for a in [eye(4), kron(Z, I2)]:
        if s.add(hvec(a)):
            basis.append(a)
    dimensions = [len(s)]
    for _ in range(17):
        for e in list(basis):
            for k, weight in gates:
                f = scale(mm(mm(dag(k), e), k), weight)
                if s.add(hvec(f)):
                    basis.append(f)
        dimensions.append(len(s))
        if dimensions[-1] == dimensions[-2]:
            closed = all(s.contains(hvec(scale(mm(mm(dag(k), e), k), weight)))
                         for e in basis for k, weight in gates)
            return dimensions, closed
    raise RuntimeError("finite-dimensional closure did not stabilize")


def sparse(a):
    return {"shape": [len(a), len(a[0])],
            "entries": [[i, j, str(x)] for i, row in enumerate(a)
                        for j, x in enumerate(row) if x]}


def run():
    checks = []

    def require(name, condition):
        if not condition:
            raise AssertionError(name)
        checks.append(name)

    bell_vector = [ONE, Z0, Z0, ONE]
    rho_c = scale(outer(bell_vector), F(1, 2))
    rho_d = scale(add(outer([1, 0, 0, 0]), outer([0, 0, 0, 1])), F(1, 2))
    coherent_components = [(F(1, 2), bell_vector)]
    dephased_components = [(F(1, 2), [ONE, Z0, Z0, Z0]),
                           (F(1, 2), [Z0, Z0, Z0, ONE])]
    require("unitary feedback gate", mm(dag(TOFFOLI), TOFFOLI) == eye(8))
    require("actuator initialization isometry", mm(dag(V), V) == eye(4))
    prepared = mm(mm(CNOT, kron(PX, P0)), dag(CNOT))
    require("record acquisition produces Bell state", prepared == rho_c)
    require("same source marginal", ptrace(rho_c, (0,), 2) == ptrace(rho_d, (0,), 2))
    require("same memory marginal", ptrace(rho_c, (1,), 2) == ptrace(rho_d, (1,), 2))

    outputs = [kron(eye(4), f) for f in PROJECTORS]
    no_probe_effects = [effect_pullback(e) for e in outputs]
    probe_effects = list(no_probe_effects)
    choi_basis = []
    r_c, r_d = process_matrix(rho_c), process_matrix(rho_d)
    rf_c, rf_d = process_matrix(rho_c, True), process_matrix(rho_d, True)
    for ri, (pu, pv) in enumerate(product(PROJECTORS, repeat=2)):
        j = kron(pv, trans(pu))
        choi_basis.append(j)
        for label, rho, r in [('coherent', rho_c, r_c), ('dephased', rho_d, r_d)]:
            y = evolve(measure_prepare(rho, pu, pv))
            direct = ptrace(y, (2,), 3)
            require(f"Choi/direct agreement {label} operation {ri}", comb_apply(r, j) == direct)
            complement = add(I2, scale(pu, -1))
            z = evolve(measure_prepare(rho, complement, pv))
            require(f"instrument normalization {label} operation {ri}",
                    trace(add(y, z)) == ONE)
            for oi, ef in enumerate(outputs):
                pulled = effect_pullback(ef, pu, pv)
                require(f"forward/backward agreement {label} operation {ri} outcome {oi}",
                        expect(y, ef) == expect(rho, pulled))
        probe_effects.extend(effect_pullback(e, pu, pv) for e in outputs)

    require("physical Choi operations span all Hermitian slot matrices", len(op_span(choi_basis)) == 16)
    require("restricted processes are exactly equal", r_c == r_d)
    require("expanded processes differ", rf_c != rf_d)
    require("restricted equivalence for all basis effects", all(
        expect(rho_c, e) == expect(rho_d, e) for e in probe_effects))

    gram_counts = {}
    for label, rho, comps in [('coherent', rho_c, coherent_components),
                              ('dephased', rho_d, dephased_components)]:
        for full in (False, True):
            r = process_matrix(rho, full)
            g, count = gram_process(comps, full)
            tag = f"{label}_{'full' if full else 'actuator'}"
            gram_counts[tag] = count
            require(f"positive Gram certificate {tag}", r == g)
            require(f"Hermitian process {tag}", r == dag(r))
            # Partial trace of final output leaves S_out tensor S_in.
            n = 5 if full else 3
            require(f"causal trace constraint {tag}",
                    ptrace(r, (n-2, n-1), n) == kron(I2, ptrace(rho, (0,), 2)))

    coarse_span, probe_span = op_span(no_probe_effects), op_span(probe_effects)
    all_output_ops = [kron(kron(a, b), c) for a, b, c in product(PAULIS, repeat=3)]
    full_effects = [effect_pullback(e) for e in all_output_ops]
    full_span = op_span(full_effects)
    ranks = {"actuator_observation_only": len(coarse_span),
             "all_source_instruments_actuator_output": len(probe_span),
             "full_joint_output": len(full_span)}
    require("observation-only effect rank is 2", ranks["actuator_observation_only"] == 2)
    require("source-instrument effect rank is 8", ranks["all_source_instruments_actuator_output"] == 8)
    require("full-output effect rank is 16", ranks["full_joint_output"] == 16)
    require("exact restriction from full to probe scope", all(full_span.contains(hvec(e)) for e in probe_effects))
    require("exact restriction from probe to observation scope", all(probe_span.contains(hvec(e)) for e in no_probe_effects))

    # Reopen the output, undo feedback, undo record acquisition, measure X on S.
    cnot3 = kron(CNOT, I2)
    recover = mm(cnot3, TOFFOLI)
    plus_s = kron(PX, eye(4))
    witness = mm(mm(dag(recover), plus_s), recover)
    pc, pd = expect(evolve(rho_c), witness), expect(evolve(rho_d), witness)
    require("coherent recovery probability is 1", pc == 1)
    require("dephased recovery probability is 1/2", pd == F(1, 2))
    witness_input = effect_pullback(witness)
    require("expanded witness is absent from restricted effect span", not probe_span.contains(hvec(witness_input)))
    require("expanded witness is present in full effect span", full_span.contains(hvec(witness_input)))

    mode_table = []
    for m, s in product(range(2), repeat=2):
        v = [0]*4
        v[2*s+m] = 1
        p = expect(evolve(outer(v)), kron(eye(4), P1))
        require(f"memory-conditioned response m={m}, s={s}", p == m*s)
        mode_table.append({"memory": m, "source": s, "p_actuator_1": str(p)})
    memory_flip = kron(I2, X)
    rho_flip = mm(mm(memory_flip, rho_c), dag(memory_flip))
    p_keep = expect(evolve(rho_c), kron(eye(4), P1))
    p_flip = expect(evolve(rho_flip), kron(eye(4), P1))
    require("record-preserving intervention p=1/2", p_keep == F(1, 2))
    require("record-flipping intervention p=0", p_flip == 0)
    require("both interventions preserve normalization", trace(rho_c) == trace(rho_flip) == ONE)

    dimensions, closed = stationary_closure()
    require("stationary closure reaches full Hermitian space", dimensions[-1] == 16)
    require("stationary closure is invariant under every declared generator", closed)

    # HS projection onto the qutrit tridiagonal Hermitian operator system.
    projected = scale(mat([[1, 1, 0], [1, 1, 1], [0, 1, 1]]), F(1, 3))
    a = projected
    determinant = (a[0][0]*(a[1][1]*a[2][2]-a[1][2]*a[2][1])
                   -a[0][1]*(a[1][0]*a[2][2]-a[1][2]*a[2][0])
                   +a[0][2]*(a[1][0]*a[2][1]-a[1][1]*a[2][0]))
    require("trace-one projection counterexample", trace(projected) == ONE)
    require("projection is not positive", real(determinant) == -F(1, 27))

    return {
        "status": "passed",
        "scope": "exact finite instances; general proofs are in the formal note",
        "arithmetic": "Gaussian rationals Q(i), with exact rational span elimination",
        "checks_passed": len(checks),
        "checks": checks,
        "effect_space_dimensions": ranks,
        "restricted_process_equal": True,
        "expanded_process_equal": False,
        "positive_gram_terms": gram_counts,
        "recovery_probabilities": {"coherent": str(pc), "dephased": str(pd)},
        "memory_conditioned_response": mode_table,
        "physical_interventions": {"keep_record_p_actuator_1": str(p_keep),
                                   "flip_record_p_actuator_1": str(p_flip)},
        "stationary_closure_dimensions": dimensions,
        "nonphysical_projection_determinant": str(real(determinant)),
        "restricted_process_matrix": sparse(r_c),
        "expanded_coherent_process_matrix": sparse(rf_c),
        "expanded_dephased_process_matrix": sparse(rf_d),
        "limitations": [
            "No Planck cutoff or quantum-gravity model is derived.",
            "No valuerhood, phenomenal correspondence, lushness measure, or ordering is supplied.",
            "Boundaries, permitted operations, and causal schedule are declared model inputs.",
            "Finite closure is algebraic predictive completeness for the declared controls, not a minimum physical length.",
            "This is not a Lean proof or a re-execution of the existing Omega repository suite."
        ]
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out-dir', type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    report = run()
    report['verification_script_sha256'] = sha256(Path(__file__).read_bytes()).hexdigest()
    args.out_dir.mkdir(parents=True, exist_ok=True)
    stem = '10_FINITE_QUANTUM_CONTINUATION'
    (args.out_dir / f'{stem}_RESULTS.json').write_text(json.dumps(report, indent=2)+'\n')
    ranks = report['effect_space_dimensions']
    lines = [
        '# Finite quantum continuation — verification', '',
        '**Status:** passed. **Arithmetic:** exact Gaussian rationals; no floating-point tolerance.', '',
        f"{report['checks_passed']} named checks completed. These verify the worked instances, not the general proofs.", '',
        '| Quantity | Exact result |', '| --- | --- |',
        f"| Actuator-only observation effect dimension | {ranks['actuator_observation_only']} |",
        f"| All source instruments with actuator output | {ranks['all_source_instruments_actuator_output']} |",
        f"| Full joint output effect dimension | {ranks['full_joint_output']} |",
        '| Coherent/dephased processes at restricted output | Equal |',
        '| Coherent/dephased processes at full output | Different |',
        '| Recovery outcome, coherent preparation | 1 |',
        '| Recovery outcome, dephased preparation | 1/2 |',
        '| Record kept / flipped: actuator-1 probability | 1/2 / 0 |',
        f"| Stationary observable closure dimensions | {' → '.join(map(str, report['stationary_closure_dimensions']))} |",
        '| Qutrit orthogonal-projection determinant | −1/27 |', '',
        'The effect dimensions measure retained predictive coordinates in this model. They are not lushness scores.', '',
        'The process matrices satisfy exact causal trace constraints and have independently checked positive Gram decompositions. Sixteen physically realizable measure/prepare operations span the intervention Choi space; direct circuit and process-matrix outputs agree on all sixteen. Backward effect propagation agrees with forward probabilities.', '',
        '## Reproduce', '', 'Run with Python 3.10 or newer; no third-party packages are required.', '',
        '```bash', f'python3 {stem}_VERIFY.py', '```', '',
        f'Complete check names and sparse process matrices: [{stem}_RESULTS.json]({stem}_RESULTS.json).', '',
        f"Script SHA-256: `{report['verification_script_sha256']}`", '',
        '## Boundaries', '', *['- '+x for x in report['limitations']], ''
    ]
    (args.out_dir / f'{stem}_VERIFICATION.md').write_text('\n'.join(lines))
    print(json.dumps({k: report[k] for k in ('status', 'checks_passed', 'effect_space_dimensions',
                                           'stationary_closure_dimensions')}, indent=2))


if __name__ == '__main__':
    main()
