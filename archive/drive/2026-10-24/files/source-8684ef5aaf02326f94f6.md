# A finite quantum continuation object

## Exact consequence, composition, and situated access before valuation

**Omega Cosmology v2 — formal development note 10**  
**Version:** 0.1, 15 September 2026  
**Originator:** S. Poole  
**Development:** AI-assisted mathematical construction and exact computational checking under the originator's direction.

**Status:** a complete specification and ordinary mathematical proofs for the stated finite model class, with an executable worked instance. This is not a formalization of quantum gravity or a completed theory of valuerhood. The proofs have not been checked in a proof assistant.

Companions: [verification report](10_FINITE_QUANTUM_CONTINUATION_VERIFICATION.md), [executable verification](10_FINITE_QUANTUM_CONTINUATION_VERIFY.py), and [exact results](10_FINITE_QUANTUM_CONTINUATION_RESULTS.json).

## 1. The question and the correction to the earlier packet

The immediate question is what a choice changes about the structure of continuation. It precedes the question of which continuation is better. The object must retain interference, memory, correlations, lawful composition, and the effects of activity on subsequent capacities to act. A distribution over terminal outcomes alone does not meet that specification.

Lushness remains the proposed structural property through which Gradient Ethics might eventually compare continuations. This note does not supply a lushness formula, ordering, preference relation, or optimization objective. In particular, persistence and generativity are not stipulated as requirements for a continuation to enter the object. Whether they emerge as important properties is subsequent work.

This updates the intended interpretation of chapter 04 of the first v2 packet and its chapter 07 placeholder functional. Those passages built persistence or generativity into the description of richness more strongly than the originator intends. The present construction represents lawful continuations before assessing their character.

The cosmological motivation is that a specified Logos determines the distinctions its manifestation supports. The godly perspective names completeness with respect to that structure. Here we construct an exact, finite, model-relative instance of predictive completeness. We do not identify its algebraic closure with a Planck length or the final resolution of our universe.

## 2. Declared inputs: a finite Logos realization

Let a finite realization of a Logos supply:

1. A finite-dimensional Hilbert space $\mathcal H$, of dimension $d$, with a declared decomposition into primitive components when locality is used.
2. A finite causal schedule $k=0,\ldots,N$.
3. Lawful quantum evolution and physically specified interaction opportunities.
4. A family of admissible instruments at each opportunity, including any restrictions on resources, control, records, and access.
5. Allowed terminal or stopping observations.

An initial state $\rho_0\geq0$, $\operatorname{Tr}\rho_0=1$, together with these data specifies a finite manifestation. Initial states can be mixed. Any purification, apparatus, or environment whose later interaction matters must either be included explicitly or represented by an adequate process description.

Write a branch of an admissible instrument, followed by the scheduled evolution, as a completely positive trace-nonincreasing map

$$
\Phi_{k,a,r}:\operatorname{Herm}(\mathcal H)\longrightarrow
\operatorname{Herm}(\mathcal H).
$$

Here $a$ identifies an instrument and $r$ its recorded outcome. For each $a$,

$$
\sum_r\Phi_{k,a,r}\quad\text{is trace-preserving}.
$$

For example, with a supplied unitary $U_{k+1}$ and local operation $\mathcal A_{k,a,r}$,

$$
\Phi_{k,a,r}(\rho)
=U_{k+1}\,\mathcal A_{k,a,r}(\rho)\,U_{k+1}^{\dagger}.
$$

All maps act on a sufficiently complete state. A reduced state that omits returning environmental memory is not presumed sufficient.

These are model inputs, not discoveries about our universe. A finite tensor decomposition, a causal schedule, and an operation set are not derived by naming them Logos. In particular, finite dimension is an explicit modeling restriction, not a result of Planck quantization.

### 2.1 What a choice means here

A choice is an admissible physical operation, or a policy selecting operations from available records. Policies may use only the records and memory permitted by the model. A choice is not an instruction to set an inaccessible state variable freely.

Feedback can be internal. A physical memory register can control which interaction occurs next. Its value changes the effective interaction while the governing law stays fixed. If availability depends on a resource or mode, that variable belongs in the state and control mechanism. An externally supplied menu must not silently grant an agent powers absent from its physical implementation.

An operational instrument can be represented with additional apparatus and records in a larger closed model. The external operation label is a description of that interaction, not a commitment to an unphysical intervention from outside a completed universe. The block reading regards the full causal model as specified; it adds no moving global present.

## 3. Histories and their quantum organization

For a recorded sequence $h=(a_0,r_0;\ldots;a_{k-1},r_{k-1})$, define the unnormalized conditional state

$$
\sigma_h=\Phi_{k-1,a_{k-1},r_{k-1}}\circ\cdots\circ
\Phi_{0,a_0,r_0}(\rho_0).
$$

Its probability is $w_h=\operatorname{Tr}\sigma_h$. If $w_h>0$, the normalized conditional state is $\rho_h=\sigma_h/w_h$. Zero-probability records have no normalized conditional state in this construction.

This is an instrument history, with actual recorded alternatives. It does not assign ordinary probabilities to every arbitrarily drawn quantum path. Coherent alternatives remain inside the quantum maps until an instrument or a justified decoherent history family supports a classical outcome description. Inserting a resolution of identity into an amplitude is a change of representation; physically measuring those alternatives can change the process. The histories distinction follows the existing quantum appendix and decoherent-histories framework. [Hartle, 2016](https://arxiv.org/abs/1608.04145).

For an actual instrument, forgetting its outcome replaces the branches by their sum:

$$
\Phi_a=\sum_r\Phi_{a,r}.
$$

Summation of recorded branches and coherent summation of amplitudes are different operations. No branch-counting measure is introduced here.

The field contains complete modeled process relations, including intervening records. Two different processes can reach the same terminal state. Future equivalence of suffixes therefore does not establish equivalence of their pasts, their whole histories, or their phenomenal character.

## 4. From all future tests to an explicit effect space

Let $\mathcal F_k$ be the allowed stopping measurement effects at time $k$. We include $I$ in their real span; it represents the certain event and tracks normalization. Stopping measurements are terminal for that protocol. Measurements followed by further activity appear as instrument branches in $\Phi$.

The adjoint map is defined by

$$
\operatorname{Tr}\!\left[\Phi(\rho)E\right]
=\operatorname{Tr}\!\left[\rho\,\Phi^{\dagger}(E)\right].
$$

For each declared access scope $p$, define backward effect spaces:

$$
\mathcal E_{N,p}=\operatorname{span}_{\mathbb R}\mathcal F_{N,p},
$$

$$
\mathcal E_{k,p}
=\operatorname{span}_{\mathbb R}\!\left(
\mathcal F_{k,p}\ \cup\
\bigcup_{a,r}\Phi_{k,a,r}^{\dagger}(\mathcal E_{k+1,p})
\right).
\tag{1}
$$

The union ranges over the instruments available to that scope. The schedule and instrument model must include any admissibility constraints across time. The simple recursion assumes that a permitted branch can be followed by the permitted continuation protocols at the next stage. A controller or resource that enforces additional restrictions must be included in the state or explicitly in the protocol type.

An element of $\mathcal E_{k,p}$ is a linear combination of effects, not necessarily itself a measurement effect. This is an operator system in the elementary sense of a self-adjoint linear space containing $I$. It need not be closed under operator multiplication.

### Proposition 1 — exact predictive equivalence

For a fixed model, stage, and scope, the following are equivalent:

$$
\rho\sim_{k,p}\rho'
\quad\Longleftrightarrow\quad
\operatorname{Tr}(\rho E)=\operatorname{Tr}(\rho'E)
\quad\forall E\in\mathcal E_{k,p};
\tag{2}
$$

and $\rho,\rho'$ give the same joint outcome probabilities for every permitted continuation protocol from that stage.

**Proof.** At the terminal stage, the assertion follows from the definition of $\mathcal F_{N,p}$ and linearity. A complete recorded branch followed by a later event has an effect obtained by pulling the later effect backward through $\Phi^{\dagger}$. Equation (1) includes every such pullback. An adaptive protocol selects later instruments using earlier records; each of its complete recorded branches has this form, and a union of recorded outcomes has the sum of their effects. Induction therefore puts every protocol effect in $\mathcal E_{k,p}$. Conversely, every generator in (1) is an allowed stopping effect or a linear combination of effects of protocols formed by preceding an allowed continuation with an allowed branch. Agreement on all protocols gives agreement on their real span. $\square$

Operationally distinct here means unequal predicted statistics in some allowed context. It does not mean perfect discrimination in one trial, exact experimental recovery of an unknown probability, or access to incompatible observables simultaneously.

## 5. The residual state is a restricted functional

Define

$$
q_{k,p}(\rho)=\rho|_{\mathcal E_{k,p}},
\qquad
q_{k,p}(\rho)(E)=\operatorname{Tr}(\rho E).
\tag{3}
$$

A finite basis $E_1,\ldots,E_m$ represents this object by the vector of expectations $(\operatorname{Tr}\rho E_i)_i$. This vector is a coordinate presentation of a functional, not a selected list of values the agent likes.

Retain its physical range:

$$
\mathcal K_{k,p}=q_{k,p}\bigl(\operatorname{Pos}(\mathcal H)\bigr),
\qquad
\mathcal S_{k,p}=\{f\in\mathcal K_{k,p}:f(I)=1\}.
\tag{4}
$$

Thus quantum compatibility constraints are inherited from physical states. Arbitrary coordinate vectors are not admitted. The cone describes unnormalized states; its normalized section describes states of unit probability.

### Proposition 2 — minimal sufficient identification

The map $q_{k,p}$ identifies exactly the states equivalent under (2). If another statistic $s(\rho)$ preserves all of those protocol probabilities, then there is a unique map $g$ on the range of $s$ such that $q_{k,p}=g\circ s$.

**Proof.** Exact identification follows immediately from (3). If $s(\rho)=s(\rho')$, preservation of protocol probabilities and Proposition 1 give $q_{k,p}(\rho)=q_{k,p}(\rho')$. Hence defining $g(s(\rho))=q_{k,p}(\rho)$ is well-defined. Its values on the range of $s$ are forced. $\square$

This is minimality relative to the stated predictive questions. It is not a theorem of minimum physical memory cost, efficient computation, or uniquely correct process boundaries.

### 5.1 Why an orthogonal projection is not generally a quantum state

Using the Hilbert–Schmidt inner product, one can represent the same restricted functional by an orthogonal projection onto $\mathcal E$. This projected operator need not be positive.

For example, project the valid qutrit state with every entry equal to $1/3$ onto the tridiagonal Hermitian operator space. The result is

$$
\frac13
\begin{pmatrix}
1&1&0\\1&1&1\\0&1&1
\end{pmatrix},
\qquad \det=-\frac1{27}.
$$

It has trace one but is not positive semidefinite. Consequently, the statistical quotient must not automatically be called a density matrix, a physical erasure channel, or a physical decoherence process. Those stronger realizations require additional conditions.

## 6. Composition descends exactly when future effects pull back correctly

Let $q$ and $q'$ be quotients defined by effect spaces $\mathcal E$ and $\mathcal E'$, both containing $I$. Let $\Phi$ be a fixed allowed physical branch map.

### Proposition 3 — necessary and sufficient condition for a quotient update

A well-defined linear update $\widehat\Phi$ on the quotient exists with

$$
q'\circ\Phi=\widehat\Phi\circ q
\tag{5}
$$

if and only if

$$
\Phi^{\dagger}(\mathcal E')\subseteq\mathcal E.
\tag{6}
$$

The statement is on the full Hermitian spaces and their image quotients; condition (6) is also necessary if exact prediction is required for all density matrices.

**Proof.** If (6) holds and $q(X)=q(Y)$, then for every $E'\in\mathcal E'$,

$$
\operatorname{Tr}\!\left[(\Phi(X)-\Phi(Y))E'\right]
=\operatorname{Tr}\!\left[(X-Y)\Phi^{\dagger}(E')\right]=0.
$$

Therefore $\widehat\Phi(q(X)):=q'(\Phi(X))$ is well-defined and linear. Conversely, if a pullback $\Phi^{\dagger}(E')$ lies outside $\mathcal E$, finite-dimensional orthogonality provides a Hermitian $Z\perp\mathcal E$ having nonzero inner product with that pullback. Since $I\in\mathcal E$, $\operatorname{Tr}Z=0$. For sufficiently small $\epsilon>0$, $\rho_\pm=I/d\pm\epsilon Z$ are density matrices. They have equal $q$ but different $q'\Phi$, contradicting (5). $\square$

Equation (1) enforces (6) for every modeled branch. Thus the quotient states have well-defined sequential dynamics. A composition of admitted maps descends by successive application of (5).

On the physical cone, $\widehat\Phi$ is positive in the induced sense: it sends the image of a positive state to the image of a positive state. It is not thereby a completely positive map between matrix algebras; the quotient is not generally such an algebra.

For a record $r$, branch probability and conditioning are retained:

$$
w_r=\bigl(\widehat\Phi_{a,r}f\bigr)(I),
\qquad
f_r=\widehat\Phi_{a,r}f/w_r\quad(w_r>0).
$$

A normalized conditional state alone omits branch probability, so unnormalized states or explicit weights must be kept when records are compared or recombined.

### 6.1 Limits of the composition claim

The theorem covers the declared contexts. It does not license attachment of arbitrary new systems after distinctions have been removed. New apparatus, newly exposed subsystems, or new coherent couplings can enlarge the effect space and invalidate the quotient.

In particular, separate marginal quotients of correlated systems do not in general determine the joint quotient. Entanglement and classical correlations can carry consequential distinctions absent from both marginals. Joint composition must be computed from the joint state or a sufficient joint process. One cannot replace it by the tensor product of marginal summaries unless the required factorization is justified.

Arbitrary external quantum memory requires the corresponding enlarged or complete process semantics. In the state formulation it must be included in $\mathcal H$ and the allowed contexts. In a quantum-network formulation it belongs in the permissible testers. Neither route follows from testing isolated subsystems alone.

## 7. A finite all-horizon closure under stationary assumptions

There is a stronger construction when the Hilbert space, allowed instrument family, and stopping effects are time-independent and arbitrary finite sequences of the declared operations are allowed. Any relevant controller memory is again included in the state.

Starting from $\mathcal E^{(0)}=\operatorname{span}_{\mathbb R}\mathcal F$, set

$$
\mathcal E^{(n+1)}
=\operatorname{span}_{\mathbb R}\!\left(
\mathcal E^{(n)}\cup
\bigcup_{a,r}\Phi_{a,r}^{\dagger}(\mathcal E^{(n)})
\right).
\tag{7}
$$

### Proposition 4 — saturation and exact continuation closure

The sequence stabilizes at a space $\mathcal E_*$ after at most $d^2-\dim\mathcal E^{(0)}$ strict dimension increases. It is the smallest real space containing the stopping effects and invariant under every declared branch adjoint. Equality of restrictions to $\mathcal E_*$ is equivalent to equality of all finite recorded continuation probabilities in this stationary model.

**Proof.** Each space is contained in the next and has dimension at most $d^2$. If two successive spaces are equal, (7) already closes the space under all adjoints, so all subsequent spaces are equal. Any invariant space containing the seeds contains every iterate by induction and hence contains $\mathcal E_*$. Iterating Proposition 1 identifies each finite-depth protocol effect; their union spans $\mathcal E_*$. $\square$

For a finite or effectively spanned operation family with exact accessible coefficients, this gives an explicit linear-algebra algorithm. The worked implementation uses Gaussian rational arithmetic, so span membership and stabilization do not rely on numerical rank tolerances.

This closure does not eliminate horizon dependence of assessments, collapse all histories into a finite list, or solve unbounded computation for arbitrary models. It says that the initial-state distinctions needed to predict all finite protocols in this fixed model lie in a finite invariant space. The dynamics still determine arbitrarily long sequences. For time-dependent models without a finite stationary representation, this saturation theorem does not apply.

The closure may be the entire Hermitian space. Even then the state space is continuous: finite linear dimension does not establish a minimum nonzero distinguishability, a smallest amplitude difference, or a spacetime pixel.

## 8. Perspectives and transport

An access scope $p$ gives a physically specified family of questions and interactions. It is an operational component of a perspective. It is not a complete definition of perspective, awareness, identity, or the soul invariant.

### Proposition 5 — exact restriction between scopes

On the same underlying Hilbert space, a linear restriction map $r_{p\leftarrow q}$ satisfying

$$
q_p=r_{p\leftarrow q}\circ q_q
\tag{8}
$$

exists if and only if $\mathcal E_p\subseteq\mathcal E_q$.

**Proof.** Inclusion gives restriction of functionals. If inclusion fails, choose $E\in\mathcal E_p\setminus\mathcal E_q$ and an orthogonal separating $Z$ as in Proposition 3. Density matrices $I/d\pm\epsilon Z$ agree under $q_q$ but differ under $q_p$. Thus no function of the $q_q$ data can reproduce $q_p$ for every state. $\square$

For nested scopes, restrictions compose. Scopes that preserve different, nonnested sets of distinctions need not form one resolution slider.

For a change of presentation represented by a unitary identification $W$, exact transport additionally requires that the state, dynamics, observations, and permitted operations all transform consistently. Equal Hilbert-space dimension or identical observed trajectories alone is not enough. Under a verified correspondence, $\rho\mapsto W\rho W^\dagger$ and $E\mapsto WEW^\dagger$ preserve all pairings and therefore transport the quotient. No canonical tensor factorization is derived by this fact.

The repository already establishes finite classical obstructions to transporting interventions across incompatible component partitions. The present criterion preserves that lesson in the quantum construction. It is not a proof that every classical implementation has already been translated. [Omega process-interface transport report](repository://Omega/blob/506ef363a3f27ec4713617089f4f7f3caf8a7d9c/docs/research_notes/omega_v2/process_interface_transport_report_v0.md).

## 9. The continuation object itself

For a declared scope, the finite residual continuation object consists of

$$
\mathfrak F_{\Lambda,p}^{N}(\rho_0)
=\left(
\{\mathcal K_{k,p},\mathcal S_{k,p}\}_{k=0}^{N},
\{\widehat\Phi_{k,a,r}\},
\{\text{retained effects and their pairings}\},
q_{0,p}(\rho_0)
\right),
\tag{9}
$$

together with the instrument grouping, stage types, and allowed protocol composition. These data retain branch weights and conditional updates, rather than just an unlabeled reachable set. The reachable part is generated from the distinguished initial state by the admitted compositions.

The complete finite model also retains its underlying component structure, physical operations, and the diagram of scope restrictions or verified transports. A single interface quotient is not substituted for all of that information. Distinct internal implementations may have the same behavior through one interface.

Equation (9) is a process object. Its labels $a,r$ do not carry utilities. Two actual occurrences represented by the same residual state remain occurrences in their respective histories; the quotient identifies their future predictive content under the declared scope, not their numerical identity or the reality of their pasts.

This formalizes one precise sense of a choice's residual mark: applying a physical operation changes the distinguished residual state and possibly the internal mode that governs subsequent responses. In an operation-level process representation it plugs a physical map into an exposed interaction point, leaving a residual process at the remaining points. Neither description requires a scalar magnitude of consequence.

## 10. Connection to quantum process tensors and combs

The state construction assumes that enough environmental memory is retained. When an interface is described without exposing that memory, a multi-time process tensor provides its response to intervention sequences. This is borrowed quantum mathematics, not an Omega theorem. [Pollock and colleagues, 2018](https://arxiv.org/abs/1512.00589).

For one intervention $\mathcal A$ on a qubit $S$, use the Choi convention

$$
J(\mathcal A)=\sum_{i,j}\mathcal A(|i\rangle\langle j|)\otimes|i\rangle\langle j|.
$$

Let $R$ have ordered factors $(O,S_{\rm out},S_{\rm in})$. The output is

$$
\rho_O(\mathcal A)
=\operatorname{Tr}_{\rm slot}\!\left[R\bigl(I_O\otimes J(\mathcal A)^T\bigr)\right].
\tag{10}
$$

The transpose is in the declared product basis. A physical deterministic process satisfies

$$
R\geq0,
\qquad
\operatorname{Tr}_O R=I_{S_{\rm out}}\otimes\rho_{S_{\rm in}}.
\tag{11}
$$

Equations (10)–(11), their multi-slot versions, and network composition use the established quantum-comb framework. Its completeness is relative to exposed ports, rather than a statement that all internal implementations coincide. [Chiribella, D'Ariano, and Perinotti, 2009](https://arxiv.org/html/0904.4483v2).

For a permitted tester outcome represented in the compatible dual convention by $E$, its probability is $\operatorname{Tr}(RE)$. Therefore restricted process equivalence is orthogonality of $R-R'$ to the span of permitted tester effects. Informationally complete testers identify the whole process operator on those ports. This is the process-level counterpart of (2), with admissible process operators replacing initial density matrices.

## 11. Worked model: a physical record controls a later interaction

Use three qubits in order $(S,M,A)$: source, memory, and actuator. The names identify roles in this fixture, not categories of valuerhood.

Initialize the actuator in $|0\rangle_A$. A record is acquired by

$$
|+\rangle_S|0\rangle_M
\xrightarrow{\mathrm{CNOT}_{S\to M}}
|\Phi^+\rangle_{SM}
=\frac{|00\rangle+|11\rangle}{\sqrt2}.
$$

The feedback unitary is the Toffoli gate

$$
U|s,m,a\rangle=|s,m,a\oplus sm\rangle.
\tag{12}
$$

The physical memory controls whether the source can affect the actuator. At $a=0$,

$$
p(A=1\mid s,m)=sm.
$$

Changing $s$ from zero to one changes the actuator when $m=1$ and does not when $m=0$. This dependence is generated by the same fixed interaction law. The memory is not an externally assigned score or a declared good state.

Two admissible operations on an acquired record are keeping it and flipping $M$. From the Bell preparation, the subsequent actuator-1 probabilities are respectively $1/2$ and $0$. Both operations preserve normalization. This is a consequence difference; no preference between these outcomes is asserted.

### 11.1 A matched pair with hidden coherence

Consider the two boundary preparations

$$
\rho_c=|\Phi^+\rangle\langle\Phi^+|,
\qquad
\rho_d=\frac12\bigl(|00\rangle\langle00|+|11\rangle\langle11|\bigr).
\tag{13}
$$

Their individual source and memory marginals agree. The dephased preparation can be modeled using an additional environment; this fixture treats $\rho_c$ and $\rho_d$ as specified boundary states. No claim is made that an omitted purification has ceased to exist.

Expose one intervention on $S$, then apply $U$, and initially expose only output $A$. For an arbitrary completely positive branch $\mathcal A$,

$$
\tau_c(\mathcal A)
=\operatorname{Tr}_{SM}\!\left[
U\bigl((\mathcal A\otimes\mathrm{id}_M)(\rho_c)\otimes|0\rangle\langle0|_A\bigr)U^\dagger
\right],
$$

and analogously $\tau_d$.

### Proposition 6 — full equality at the restricted interface

For every intervention $\mathcal A$ on $S$, $\tau_c(\mathcal A)=\tau_d(\mathcal A)$.

**Proof.** Their input difference consists of terms off-diagonal in $M$:

$$
\rho_c-\rho_d
=\frac12\left(|0\rangle\langle1|_S\otimes|0\rangle\langle1|_M
+|1\rangle\langle0|_S\otimes|1\rangle\langle0|_M\right).
$$

An operation on $S$ preserves the off-diagonal memory indices. The gate (12) is block-diagonal in $M$ and also preserves those indices. Tracing out $M$ annihilates each difference term. This proves equality even for a general linear $S$ operation, hence for every physical branch. $\square$

The corresponding $8\times8$ process operators $R_c,R_d$ on $(A,S_{\rm out},S_{\rm in})$ are exactly equal. In computational order they are explicitly

$$
R_c=R_d=\frac12\operatorname{diag}(1,1,1,0,0,0,0,1).
$$

This is stronger than agreement under one selected measurement or one chosen policy.

### 11.2 Reopening the joint system breaks that equivalence

Instead expose the full output $SMA$, or permit a later interaction that accesses it. Apply

$$
W=(\mathrm{CNOT}_{S\to M}\otimes I_A)U^\dagger
$$

to the output of $U$, and measure $|+\rangle\langle+|$ on $S$. Undoing the feedback and then the record-acquisition interaction gives

$$
p(+\mid\rho_c)=1,
\qquad
p(+\mid\rho_d)=\frac12.
\tag{14}
$$

The process matrices with output $SMA$ can also be written explicitly. Let

$$
|w_m\rangle=\sum_{o=0}^{1}|o,m,om\rangle_{SMA}\otimes|o,m\rangle_{S_{\rm out}S_{\rm in}}.
$$

Then

$$
R_c^{\rm full}=\frac12(|w_0\rangle+|w_1\rangle)(\langle w_0|+\langle w_1|),
\qquad
R_d^{\rm full}=\frac12\sum_{m=0}^{1}|w_m\rangle\langle w_m|.
$$

These are process operators with trace two, as required by (11), not normalized density matrices. Their cross terms differ. The later coherent interaction is outside the restricted interface used in Proposition 6. There is no contradiction: the scope changed, and the old quotient does not preserve the newly exposed distinction.

This uncomputation is a finite diagnostic of retained coherence. It is not a model of awareness causing erasure, an experiment on a quantum-gravity cutoff, or a claim that all macroscopic records can practically be reversed.

### 11.3 The residual spaces can be computed exactly

On the four-dimensional $SM$ boundary space, consider three scopes:

| Scope | Allowed process access | Effect-space dimension |
| --- | --- | ---: |
| $p_0$ | No intervention; arbitrary final measurement on $A$ | 2 |
| $p_1$ | Arbitrary one-slot instruments on $S$; arbitrary final measurement on $A$ | 8 |
| $p_2$ | Full joint output after the supplied isometry and unitary | 16 |

These spaces satisfy $\mathcal E_{p_0}\subset\mathcal E_{p_1}\subset\mathcal E_{p_2}$. The dimensions include the normalization coordinate. They count independent predictive coordinates in this example, not branches, identities, possible experiences, or units of lushness.

The first space is $\operatorname{span}_{\mathbb R}\{I,|11\rangle\langle11|\}$. For the second, all tests remain block-diagonal in $M$, so the space is contained in

$$
\operatorname{Herm}(\mathbb C^2_S)\otimes
\operatorname{span}_{\mathbb R}\{I_M,Z_M\}.
$$

Measure/prepare operations on $S$ span this eight-dimensional space: preparation of $S=1$ permits the actuator to reveal the $M=1$ block, while branch traces retain the sum of the memory blocks. Full joint output preserves the whole sixteen-dimensional input operator space because the supplied evolution from $SM$ is an isometry.

The witness (14), pulled back to the input, lies outside $\mathcal E_{p_1}$ and inside $\mathcal E_{p_2}$. This is an explicit obstruction to transporting the restricted quotient into the expanded scope.

## 12. Exact computational verification

The companion script uses only the Python standard library. Matrix entries are exact Gaussian rationals $a+bi$, $a,b\in\mathbb Q$. Span calculations use exact rational elimination. There are no floating-point rank thresholds.

For the intervention basis, take the four projectors onto $|0\rangle$, $|1\rangle$, $|+\rangle$, and $|{+i}\rangle=(|0\rangle+i|1\rangle)/\sqrt2$. The sixteen maps

$$
\mathcal A_{v,u}(X)=\operatorname{Tr}(P_uX)P_v,
\qquad
J(\mathcal A_{v,u})=P_v\otimes P_u^T
$$

span the Hermitian Choi operator space. Each is a physical instrument branch, completed by replacing $P_u$ with $I-P_u$ in the second branch. This makes the finite basis an adequate spanning set of physical operations, rather than a sample of convenient unitary gates.

The retained run completes **233 named checks**. It verifies:

- Forward circuit probabilities and backward-propagated effects agree.
- Sixteen physical measure/prepare Choi operators span the intervention operator space.
- Direct circuit and process-matrix outputs agree on all sixteen operations for both preparations.
- Every tested complete instrument has unit total probability.
- The restricted process matrices coincide and the expanded ones differ.
- Both process representations satisfy their causal partial-trace constraints.
- Independently constructed positive weighted Gram decompositions reproduce the process matrices exactly.
- The effect-space dimensions are $2,8,16$, with the stated inclusions and missing witness.
- Physical record acquisition and the memory-conditioned response obey (12)–(14).
- The nonpositive orthogonal-projection example has determinant $-1/27$.

For a separate stationary two-qubit control family generated by source Hadamard and phase gates, CNOT, and SWAP, the effect closure from $\operatorname{span}\{I,Z_S\}$ has dimensions

$$
2\longrightarrow4\longrightarrow8\longrightarrow12\longrightarrow16\longrightarrow16.
$$

The final space is checked invariant under every declared generator. This is a positive control for the saturation construction, not evidence of a privileged universal gate set or a physical minimum scale. A Hadamard conjugation is evaluated as $H_0EH_0/2$ with integer $H_0$, retaining exact rational arithmetic.

The script verifies worked instances. It does not replace the general proofs above, derive physical assumptions, or rerun the existing Omega repository suite.

## 13. The Planck/Logos conjecture and what would establish it

The complete finite perspective is the full collection of distinctions supported by the declared finite realization and its admissible contexts. Bounded descriptions restrict that collection. This is a precise model-relative realization of the originator's proposed definition of a godly perspective.

The stronger cosmophysical conjecture is that our universe has an intrinsic distinguishability structure governed in part by quantum gravity and Planck-scale constraints. Such constraints could determine which proposed refinements add physical content. This is motivated by the minimal-length literature, but that literature does not supply the complete future-equivalence relation required here. [Mead, 1964](https://doi.org/10.1103/PhysRev.135.B849); [Hossenfelder, 2013](https://arxiv.org/abs/1203.6191).

The present construction does not introduce a cutoff at $\ell_P$. In a Hamiltonian realization, $\hbar$ enters the specified unitary through $U(t)=\exp(-i\widehat Ht/\hbar)$. Neither the dimension bound in Proposition 4 nor the chosen qubit factorization follows from that formula. If every global measurement is already permitted at the current stage, the effect space is all of $\operatorname{Herm}(\mathcal H)$ and the quotient identifies only equal density matrices. Quantum theory alone does not force a nontrivial compression of that complete state description.

To establish the proposed physical limit, one would need a justified underlying theory, its lawful comparison contexts, and an argument that its residual representation identifies exactly physically equivalent descriptions. A minimum localization length alone would not establish equivalence of all correlations, temporal processes, or amplitudes below a spatial grid.

Our saturation is a closure under a specified dynamics and observation family. It is not a universal minimum distance in state space. Arbitrarily small statistical differences can survive in it. Approximate distinguishability at finite resources requires a separate error model; a pairwise tolerance relation is generally not transitive and is not automatically an exact quotient.

## 14. Where valuerhood and value-space can enter

The object now contains more than a list of outcomes: situated records, causal participation, dependence on internal organization, and changes to subsequent response. These supply places to investigate how distinctions become stakes for a locus within the process.

The worked model demonstrates record acquisition and memory-conditioned causal influence. It does not identify the source-memory pair, the actuator, or their union as a valuer. No success condition, pleasure signal, persistence requirement, or preference ordering selects a privileged subsystem.

This matters because the repository already shows that even complete finite intervention evidence can leave several candidate process boundaries, depending on the feature query. An operationally identified boundary is not automatically an identity or a valuer. [Omega process-interface identifiability report](repository://Omega/blob/506ef363a3f27ec4713617089f4f7f3caf8a7d9c/docs/research_notes/omega_v2/process_interface_identifiability_report_v0.md).

Further work can ask which organizations develop self-relevant differentiation and how those differentiations affect their continuation. Their capacities to distinguish and respond may themselves change. A candidate value-space would have to be grounded in those relationships, with the phenomenal correspondence still open. The mathematical object does not guarantee that causal responsiveness suffices for valuation.

The persistence filter can later be studied as part of a specified dynamics and ecology. This finite fixture supplies neither replication nor an open-ended evolutionary environment; it cannot establish cosmic Darwinian emergence. Generativity and persistence remain proposed emergent features. Lushness remains a candidate structural property to investigate after the object and valuer correspondence are understood.

## 15. What is established, borrowed, and still open

| Item | Status in this note |
| --- | --- |
| Finite quantum instruments, Choi representation, process tensors, and network composition | Borrowed mathematical foundations |
| Backward effect recursion and exact equivalence | Defined and proved for the stated model class |
| Minimal sufficient identification | Proved relative to the declared protocols |
| Necessary and sufficient pullback condition for quotient dynamics | Proved |
| Stationary all-finite-horizon closure | Proved under stationary finite-dimensional assumptions |
| Exact restriction and obstruction between scopes | Proved |
| Three-qubit record/feedback process and its scope-dependent equivalence | Analytic proof and exact executable checks |
| Arbitrary physical realization of the quotient as a quantum channel | Not established; an explicit projection counterexample is given |
| Canonical components, intervention family, or embodied perspective | Not derived |
| Universe-wide composition, arbitrary causal structure, or quantum gravity | Not formalized here |
| Planck-derived terminal comparison resolution | Open physical conjecture |
| Awareness, universal habitation, or soul invariant | Open correspondence or metaphysical conjecture |
| Valuerhood and value-space | Not yet identified by this construction |
| Lushness, ethical ordering, or emergent generativity | Deliberately unassigned |

The advance is a constructive replacement for an abstract equivalence specification in a stated finite class. It gives a process object, exact quotient dynamics, explicit transport conditions, and a worked example in which the model answers structural questions. It is not presented as a new theorem of quantum theory or proof of the cosmological interpretation.

## 16. References and relation to previous work

1. **Chiribella, G.; D'Ariano, G. M.; Perinotti, P. (2009).** [Theoretical framework for quantum networks](https://arxiv.org/abs/0904.4483), *Physical Review A* 80, 022339. Source for quantum combs, tester semantics, and composition. Omega adds the proposed cosmological interpretation and uses the framework for its continuation question; it does not claim the underlying formalism.
2. **Pollock, F. A.; Rodríguez-Rosario, C.; Frauenheim, T.; Paternostro, M.; Modi, K. (2018).** [Non-Markovian quantum processes: complete framework and efficient characterisation](https://arxiv.org/abs/1512.00589), *Physical Review A* 97, 012127. Source for multitime process descriptions retaining environmental memory.
3. **Pollock and colleagues (2018).** [Operational Markov condition for quantum processes](https://arxiv.org/abs/1801.09811), *Physical Review Letters* 120, 040405. Previously cited in the Omega packet; relevant to the inadequacy of local state snapshots.
4. **Hartle, J. B. (2016).** [Decoherent Histories Quantum Mechanics Starting with Records of What Happens](https://arxiv.org/abs/1608.04145). Histories and records background. Our instrument calculation does not select a uniquely real classical history family.
5. **Mead, C. A. (1964).** [Possible Connection Between Gravitation and Fundamental Length](https://doi.org/10.1103/PhysRev.135.B849). Historical physical motivation for gravitational limits on measurement, not a proof of our quotient or metaphysical interpretation.
6. **Hossenfelder, S. (2013).** [Minimal Length Scale Scenarios for Quantum Gravity](https://arxiv.org/abs/1203.6191), *Living Reviews in Relativity* 16, 2. Reviews the assumptions and models behind minimum-resolution proposals.
7. **Omega repository (2026).** [Process Interface Identifiability Report v0](repository://Omega/blob/506ef363a3f27ec4713617089f4f7f3caf8a7d9c/docs/research_notes/omega_v2/process_interface_identifiability_report_v0.md) and [Process Interface Transport Report v0](repository://Omega/blob/506ef363a3f27ec4713617089f4f7f3caf8a7d9c/docs/research_notes/omega_v2/process_interface_transport_report_v0.md). Existing finite classical results retained as constraints on interface identification and transport. They are not rerun or promoted into quantum results by citation.
8. **Omega Cosmology v2 (2026), chapter 07.** [Formal Appendices](source://source-19779f1adc0543f5e6dd). Existing histories construction and protocol-relative equivalence. This note constructs explicit dynamic quotients and the worked process connection left open there.

The originator's current statements govern the intended hypothesis. The stated assumptions, proofs, and executable results govern what this formalization establishes. The two must remain distinguishable as the framework develops.
