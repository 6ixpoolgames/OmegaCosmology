# Formal baseline and the current lushness lead

**Status:** technical handoff, not a new theorem paper. The exact source is sources/quantum_continuation/10_FINITE_QUANTUM_CONTINUATION_FORMALIZATION.md. The proposed extensions below are not implemented.

## 1. Declared finite realization

Inputs are a finite Hilbert space H of dimension d, a component decomposition when locality is used, a causal schedule, physically specified instruments, resource/control restrictions, stopping effects, and an initial state. Include environmental or controller memory whenever it can return and affect continuation.

An instrument branch is CP and trace-nonincreasing:

$$
\Phi_{k,a,r}:\operatorname{Herm}(H)\to\operatorname{Herm}(H),
\qquad \sum_r\Phi_{k,a,r}\ \text{is trace-preserving}.
$$

The operation menu is a model input. Controller state or protocol types must encode state-dependent availability and cross-time constraints. An external action label describes a physical interaction; it is not an oracle giving a situated agent arbitrary control of the completed world.

For a recorded history h, retain the subnormalized conditional state:

$$
\sigma_h=\Phi_h(\rho_0),\quad
w_h=\operatorname{Tr}\sigma_h,\quad
\rho_h=\sigma_h/w_h \quad(w_h>0).
$$

These are actual instrument records. Arbitrary coherent paths do not acquire ordinary probabilities merely by being drawn as branches.

## 2. Exact effect spaces and residual states

With stopping effects F and a specified access scope p:

$$
\mathcal E_{N,p}=\operatorname{span}_{\mathbb R}\mathcal F_{N,p},
$$

$$
\mathcal E_{k,p}=
\operatorname{span}_{\mathbb R}
\left(\mathcal F_{k,p}\cup
\bigcup_{a,r}\Phi^\dagger_{k,a,r}(\mathcal E_{k+1,p})\right).
$$

Include I in the span. Equality of expectations on E is equivalent to equality of all allowed finite continuation-record probabilities. Effects in the linear span need not individually be measurement outcomes.

The residual is a restricted functional:

$$
q_{k,p}(\rho)(E)=\operatorname{Tr}(\rho E).
$$

Retain the image cone and its normalized section:

$$
\mathcal K_{k,p}=q_{k,p}(\operatorname{Pos}(H)),\qquad
\mathcal S_{k,p}=\{f\in\mathcal K_{k,p}:f(I)=1\}.
$$

Arbitrary coordinate vectors are not automatically physical. An orthogonal Hilbert–Schmidt projection onto E need not be positive; the note gives a qutrit trace-one projection with determinant -1/27.

The quotient is minimally sufficient for the stated predictive questions in a factorization sense. This is not minimum physical memory, efficient computation, or a discovered valuer boundary.

## 3. Composition, closure, and scope

An exact quotient update exists iff:

$$
q'\Phi=\widehat\Phi q
\quad\Longleftrightarrow\quad
\Phi^\dagger(\mathcal E')\subseteq\mathcal E.
$$

This is an exact full-state predictive condition. It is not a claim that every safe decision requires preserving every prediction.

In a stationary finite model, iterating adjoint closure stabilizes after at most d² minus the initial dimension strict increases. The resulting space suffices for all finite legal protocols under those fixed assumptions. It does not remove horizon dependence from assessments, discretize all states, or establish a minimum probability difference.

Scope restriction factors exactly when the effect spaces nest. Nonnested scopes need not be points along a single resolution slider. A full descriptive scope can retain all state information; it does not entail arbitrary control for an embodied agent.

## 4. The process object

The note's finite continuation object retains:

$$
\mathfrak F_{\Lambda,p}^{N}(\rho_0)
=
\left(
\{\mathcal K_{k,p},\mathcal S_{k,p}\},
\{\widehat\Phi_{k,a,r}\},
\{\text{effects and pairings}\},
q_{0,p}(\rho_0)
\right),
$$

with instrument grouping, types, and legal composition. The reachable part is generated from the initial state; the entire abstract state cone is not presumed reachable.

Keep the underlying full physical realization and the diagram of scope relations. A single bounded quotient is not the global substrate. Future predictive equivalence does not identify historical occurrences or phenomenal subjects.

For an action-conditioned comparison, use a common full model and initial situation whenever possible. Treat different actions as distinct physical operations in that model, including their costs and records. Do not compare a tiny local model with a richly supplemented model and attribute the difference solely to the action.

## 5. Worked source–memory–actuator fixture

The fixture has qubits S, M, A. CNOT acquires a record, and a Toffoli interaction flips A when S=M=1. The exact response is p(A=1|s,m)=sm. Keeping versus flipping the record yields actuator-1 probabilities 1/2 and 0 in the supplied preparation; no preference is asserted.

Coherent and dephased SM boundary states are:

$$
\rho_c=|\Phi^+\rangle\langle\Phi^+|,\qquad
\rho_d=\tfrac12(|00\rangle\langle00|+|11\rangle\langle11|).
$$

With one arbitrary S operation, then Toffoli, and only A exposed, their processes agree for every CP branch. With full joint output and a later undoing interaction, an X-basis test distinguishes them with probabilities 1 and 1/2.

The full process operators have a Gram form. The one-slot convention is:

$$
\rho_O(\mathcal A)=
\operatorname{Tr}_{slot}\!\left[
R\left(I_O\otimes J(\mathcal A)^T\right)
\right],
\quad
\operatorname{Tr}_O R=I_{out}\otimes\rho_{in}.
$$

R has the causal normalization of a process operator, not that of a density matrix. Do not silently divide traces and reuse state entropy as a canonical process measure.

Recorded exact results:

- Effect dimensions 2, 8, 16 for the three stated scopes.
- Restricted processes equal, expanded processes different.
- Coherent/dephased diagnostic probabilities 1 and 1/2.
- Stationary control example dimensions 2 → 4 → 8 → 12 → 16 → 16.
- 233 named checks; exact rational arithmetic over Q(i).

The dephased preparation is a boundary description, not proof that a purification has ceased to exist. A global extension must retain any relevant environment.

## 6. What is already a plausible aspect of lushness?

The physically reachable portion of the continuation object, its joint constraints, and its composition maps are the strongest available carrier. They encode consequential organization that raw terminal distributions miss.

Effect-space dimension measures independent predictive coordinates. It often saturates at d² under full access and is not a standalone richness measure. It also concerns distinctions between possible input states, not directly a count of futures reachable from one fixed input.

Global unitary evolution preserves state eigenvalues. State rank and entropy alone therefore cannot capture all changes of organization relative to fixed laws, components and physical opportunities. This is a reason to investigate relational process geometry, not a proof that any chosen process statistic is value.

## 7. Proposed distinguishability geometry

For matched normalized residual processes P and Q, let a common declared tester family T produce complete outcome distributions. Define:

$$
d_{\mathcal T}(P,Q)
=\sup_{T\in\mathcal T}
\frac12\sum_r
|\Pr(r|P,T)-\Pr(r|Q,T)|.
$$

This gives a pseudometric: nonnegative, symmetric, and satisfying the triangle inequality. Identity of indiscernibles requires a separating tester family or a quotient by its exact observational equivalence. That quotient remains relative to the family. It is not an ontological erasure of distinctions outside the family.

Keep interfaces, schedule, permitted memory, and resource semantics matched. A difference in available controls is itself consequential data; do not hide it by silently changing the tester domain. If P and Q have different types, report them as differently typed until a justified comparison/embedding is supplied.

A finite chosen tester list supplies a lower bound on the supremum, not the complete quantum distance unless a sufficiency theorem is given. The 16 linear-spanning CP maps in the baseline reconstruct the one-slot map but do not automatically optimize every nonlinear distinguishability objective or represent every resource-constrained tester.

Let C_a be a specified family of reachable residual processes after action a. A candidate aspect is:

$$
N_\varepsilon(C_a)
=\sup\{|S|:S\subseteq C_a,\ 
d(P,Q)>\varepsilon\text{ for distinct }P,Q\in S\}.
$$

For a finite family the supremum is a maximum. For continuous or noncompact families, finiteness and attainment require separate justification. Exact finite-dimensional state spaces are still continuous. Taking epsilon to zero is not justified by invoking the Planck length.

The multiscale profile records differentiated continuation responses. It omits weights and much of the metric/composition structure. It is a candidate diagnostic, not lushness itself.

## 8. Keep weights conditional and preserve coherence

Quantum outcome weights belong to an implemented instrument or justified record family. There is no automatic Born-weighted distribution over every counterfactual policy in the operation menu.

For a declared policy, records inherit weights. Across policies, retain a family of such processes or model a physical randomized controller explicitly. A uniform average over policy names can change under duplicating labels and is not a canonical global measure.

Forgetting an actual recorded outcome sums CP branches. Summing coherent amplitudes is different. A classical weighted graph cannot represent arbitrary interference without additional amplitude/process structure. Graph visualizations should declare which recorded/decoherent layer they depict.

Likewise, the same normalized residual process reached with different probability cannot replace the whole subnormalized process. A packing profile of normalized residuals can be equal even when probabilities differ.

## 9. The compositional question needs precision

The proposed next witness seeks equal or similar diversity summaries but different organization of continuation. There are several distinct targets:

1. Same endpoint distributions, different future intervention responses: already demonstrated in related forms.
2. Same number of residual processes, different transition/incidence structure: straightforward finite diagnostic, not by itself new physics.
3. Same packing profile, different metric or composition data: possible because a profile is lossy; must exhibit exact equality and the differing data.
4. Same complete continuation semantics under every relevant interaction, but a claimed consequential difference: this is inconsistent within the declared semantics unless the alleged difference lies outside its scope.

Do not demand target 4 and call its failure evidence against lushness. Do not call target 1 a discovery of a new value theory.

If a “residual process” includes the entire remaining temporal response, its metric may already detect some compositional differences. Specify whether the object being summarized is an endpoint state, a one-step response, or the entire remaining process before interpreting a witness.

## 10. GE bridge retained from the foundation draft

Fix a policy set and a justified violation record whose effect is retained. A license of the form:

$$
\operatorname{Tr}(\rho E_{\mathrm{bad}}^\pi)\le\epsilon
$$

transfers between states with the same sufficient residual when policy availability and violation semantics are also preserved. If model error is bounded by delta, a modeled risk at most epsilon minus delta is sufficient for true risk at most epsilon.

These are conditional statements. They do not derive a protected requirement, the error bound, model coverage, rights, standing, or moral authority. An arbitrary hidden classical “bad” flag cannot be attached across incompatible quantum histories and treated as a physically justified record.

## 11. The mathematical debts

The next program must identify a faithful global finite comparison, typed reachable residual families, admissible testers, probability semantics, and a nonarbitrary representation of composition. Then it can ask whether a candidate descriptor explains value-capable differentiation.

Canonical valuerhood, phenomenal coupling, identity, terminal physical resolution, and a normative ordering remain unsolved. The structural work can proceed without pretending those debts are settled.
