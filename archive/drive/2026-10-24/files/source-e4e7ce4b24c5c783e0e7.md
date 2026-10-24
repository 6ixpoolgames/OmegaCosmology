# 08 — Quantum Histories and Perspective Addendum

Date: 15 September 2026  
Version: v0 — working addendum  
Status: established quantum inputs; conditional mathematical realization; conjectural awareness correspondence

## Purpose and relation to the existing packet

This addendum develops the deferred quantum correspondence in §§4.1–4.3 and 13.1 of the [September 2026 Update Addendum](source://source-259b0bb46fb46868dd4e). It preserves the earlier packet as a historical record. The new contribution is a specified quantum realization of the block-and-perspective picture, including an explicit delayed-choice eraser calculation.

The model borrows unitary dynamics, Born weighting, and decoherent histories from established physics. It shows how the proposed picture can be expressed consistently within those assumptions. It does not derive quantum mechanics from Alpha, perspective, or awareness.

The change from the previous addendum is precise:

| Earlier position | What this addendum supplies | What remains open |
|---|---|---|
| Born weight is a possible physical correlate of continuation “thickness.” | Explicit branch vectors, interference terms, and weights for a specified quantum history family. | Mapping agent-relative or valuer-relative trajectories to that family. |
| Trajectory correlation may address arbitrary proliferation. | Regrouping invariance within a fixed quantum representation, following from linearity and completeness. | General valuer individuation, effective plurality, and physical duplication. |
| Block-compatible agency does not require phenomenal selection. | A record-relative quantum formulation and an eraser example requiring no privileged moving present. | The physical or phenomenal correspondence that makes a perspective inhabited. |
| Lushness may admit comparative or scalar treatment. | A quantum substrate with explicit weighting and retained correlations. | A measure of generative quantum futures; normalized Born mass alone is insufficient. |

“Established input” below means borrowed quantum mathematics. “Derived within the model” means a consequence of those inputs. The block interpretation is working architecture; universal habitation is a conjecture. The project-specific identification of a physical record interface with awareness remains open, including any distinction between awareness and consciousness.

## Repository relationship and scope

The [Omega closeout](repository://Omega/blob/cc4c89ca6552ce52cc5f7392e3b95f0c24dfdf88/docs/research_notes/omega_theory/omega_closeout_v0.md) and [migration map](repository://Omega/blob/cc4c89ca6552ce52cc5f7392e3b95f0c24dfdf88/docs/research_notes/omega_theory/migration_to_alpha_v0.md) treat the quantum branch as archive-only. This addendum belongs to that exploratory record; it does not promote quantum or phenomenal claims into the checked formal core.

Its requirement to retain future-relevant distinctions is continuous with the repository's [coarse/fine nonreflection note](repository://Omega/blob/cc4c89ca6552ce52cc5f7392e3b95f0c24dfdf88/docs/research_notes/omega_theory/coarse_fine_nonreflection_v0.md) and [marginal-coupling nonfactorization note](repository://Omega/blob/cc4c89ca6552ce52cc5f7392e3b95f0c24dfdf88/docs/research_notes/omega_theory/marginal_coupling_nonfactorization_v0.md). The present construction gives that concern a concrete quantum expression. It does not establish a formal translation of those earlier results into quantum theory.

Gradient Ethics does not depend on adopting this cosmology. No ethical standing, obligation, or ranking follows merely from quantum weight. Alpha remains optional for the construction.

## 1. The physical object

Take a closed quantum model containing the systems, apparatus, and relevant environment:

$$
\mathcal Q=(\mathcal H,|\Psi_0\rangle,U),
\qquad \langle\Psi_0|\Psi_0\rangle=1.
$$

Here $U(t,s)$ is unitary, with

$$
U(t,s)U(s,r)=U(t,r),\qquad
i\hbar\partial_tU(t,s)=\widehat H(t)U(t,s).
\tag{1}
$$

Use a finite-dimensional model or a specified regularization initially. A mixed initial state can replace the pure state by using traces throughout. This is a model on a supplied temporal/background structure; quantum gravity and the origin of that structure are outside this minimal construction.

The **block reading** treats the entire structure specified by $\mathcal Q$ as given. The parameter $t$ locates relations within it; no external advancing present is required. The equations accommodate that reading without establishing its metaphysical truth. They exhaust the quantum alternatives of the chosen model, rather than every conceivable universe.

## 2. Multiway structure without branch counting

A finite multiway representation follows by inserting orthonormal resolutions of the identity between propagators. Writing $U_k=U(t_k,t_{k-1})$,

$$
\langle f|U_N\cdots U_1|i\rangle
=\sum_{z_1,\ldots,z_{N-1}}
\prod_{k=1}^{N}\langle z_k|U_k|z_{k-1}\rangle,
\quad z_0=i,\ z_N=f.
\tag{2}
$$

Vertices are intermediate basis states; edges carry complex transition amplitudes. The same propagator admits different such graphs. Consequently, graph paths are contributions to a representation, and their number is not a physical measure of futures.

Regrouping the finite sum leaves its value unchanged. Inserting another genuine resolution of identity also leaves it unchanged. This supplies the requested consistency under refinement directly from quantum algebra; no additional prohibition on manufacturing branches is needed. Counting a basis vector twice would fail to resolve the identity. Creating an additional physical channel, by contrast, changes the physical model and can change its predictions.

For histories of coarser properties, choose exhaustive orthogonal alternatives $\{P^{(k)}_a\}$ at each selected time. In the Heisenberg picture,

$$
P^{(k)}_a(t_k)=U(t_k,t_0)^\dagger P^{(k)}_aU(t_k,t_0),
\qquad
C_\alpha=P^{(n)}_{\alpha_n}(t_n)\cdots P^{(1)}_{\alpha_1}(t_1).
$$

For a set $B$ of these histories, define

$$
C_B=\sum_{\alpha\in B}C_\alpha,\qquad
|\Psi_B\rangle=C_B|\Psi_0\rangle,\qquad
w(B)=\|\Psi_B\|^2.
\tag{3}
$$

The standard decoherence functional records the interference:

$$
D(\alpha,\beta)=\langle\Psi_\beta|\Psi_\alpha\rangle.
\tag{4}
$$

When the off-diagonal terms vanish, $w(\alpha)$ supplies an additive probability distribution over that family. Approximate decoherence gives approximate additivity, with the required accuracy assessed for the coarse events actually used. These are borrowed class-operator and decoherent-histories constructions; see [Hartle's account](https://arxiv.org/abs/1608.04145).

For disjoint $B,C$, direct expansion of the norm gives

$$
w(B\cup C)=w(B)+w(C)
+2\operatorname{Re}\langle\Psi_B|\Psi_C\rangle.
\tag{5}
$$

Thus a coarse event retains the interference between its constituent histories. Before decoherence, $w$ is not an ordinary probability measure over arbitrary sets of paths. In particular, one cannot consistently treat every unmeasured path in every alternative basis as a simultaneous classical fact.

The project's **branch thickness** intuition has a precise version: coherent alternatives contribute complex amplitudes; a recorded branch receives their resulting squared norm. Relative phase matters. “Nearby” must therefore specify a physical relation, such as nearby action, rather than adjacency in an arbitrarily drawn graph.

## 3. A situated perspective

Represent the accessible, physically encoded record of a perspective by a projector $R_p$ within a specified family of orthogonal record alternatives at time $t$. This idealizes a record interface; it does not define awareness or an enduring personal identity.

With $|\Psi(t)\rangle=U(t,t_0)|\Psi_0\rangle$,

$$
w(p,t)=\|R_p|\Psi(t)\rangle\|^2,
\qquad
|\Psi_{p,t}\rangle=
\frac{R_p|\Psi(t)\rangle}{\sqrt{w(p,t)}}
\quad\text{when }w(p,t)>0.
\tag{6}
$$

This is the state relative to the specified record. It does not replace the global state. In a sequential ideal record measurement, or an appropriate recorded history family, a later record has conditional probability

$$
p(q,t'\mid p,t)=
\bigl\|R_qU(t',t)|\Psi_{p,t}\rangle\bigr\|^2,
\qquad t'>t.
\tag{7}
$$

The conditional state retains the environment and correlations. The record label $p$ alone need not determine future statistics. Memories are physical components of the record; a remembered history need not specify a unique microscopic past.

For the project's requirement that coarse graining preserve every relevant future distinction, the exact operational condition is

$$
\rho\sim_{\mathcal T}\sigma
\quad\Longleftrightarrow\quad
\operatorname{Tr}(\rho E_{\tau r})
=\operatorname{Tr}(\sigma E_{\tau r})
\quad\text{for all }\tau\in\mathcal T,\ r.
\tag{8}
$$

Here $\rho,\sigma$ describe sufficiently complete physical situations; $\mathcal T$ specifies admissible future protocols, and $E_{\tau r}$ is the effect for complete record $r$ under protocol $\tau$. This is a criterion for a proposed compression, not a claim that every present-record projection satisfies it. With all global quantum measurements available, the equivalence reduces to equality of states. Nontrivial compression therefore depends on an actual restriction of accessible distinctions.

The optional **universal habitation conjecture** assigns awareness to every physically admissible situated perspective, without selecting an external present. The formulas neither require that conjecture nor identify awareness with consciousness. They provide a place to state the correspondence separately.

The closest borrowed awareness framework is [Don Page's positive-operator approach](https://arxiv.org/abs/quant-ph/0108039), where experiential measures take the form $\mu(S)=\langle A(S)\rangle$. Our record projectors are more restrictive physical objects; identifying them with awareness operators would be an additional hypothesis. Page's more general awareness measures need not form a normalized probability distribution over all experiences.

## 4. The delayed-choice eraser, explicitly

Use an ideal pair of path qubits, signal $s$ and idler $i$:

$$
|\Psi\rangle=
\frac{|0\rangle_s|0\rangle_i+e^{i\phi}|1\rangle_s|1\rangle_i}{\sqrt2}.
\tag{9}
$$

Let $\psi_j(x)=\langle x|U_s|j\rangle$ be the signal amplitude at a detector position. The two propagated modes are normalized and orthogonal globally, while they can overlap locally at the screen. All outcomes, including losses if present, must be included for normalization. This ideal model isolates the correlations illustrated by the [Kim et al. experiment](https://arxiv.org/abs/quant-ph/9903047); it is not a reconstruction of every optical component.

Ignoring the idler means taking a partial trace. The signal density is

$$
p(x)=\frac12\left(|\psi_0(x)|^2+|\psi_1(x)|^2\right).
\tag{10}
$$

There is no interference cross term. Measuring the idler in its path basis gives

$$
p(x,j)=\frac12|\psi_j(x)|^2,\qquad j=0,1.
$$

For an eraser basis $|\pm\rangle_i=(|0\rangle_i\pm|1\rangle_i)/\sqrt2$, the joint densities instead are

$$
\boxed{p(x,\pm)=\frac14
\left|\psi_0(x)\pm e^{i\phi}\psi_1(x)\right|^2.}
\tag{11}
$$

Since $p(\pm)=1/2$, the conditional densities are twice these joint densities. Their cross terms have opposite signs, and

$$
p(x,+)+p(x,-)=p(x).
\tag{12}
$$

The same detector record participates in different conditional descriptions when additional records are included. The unsorted screen data remain unchanged. This is the specific structural match to the block intuition: one joint arrangement supports both descriptions without rewriting an earlier event. The conditional-statistics interpretation is also developed in [Fankhauser's analysis](https://arxiv.org/abs/1707.07884).

To see why delaying the idler measurement causes no inconsistency, let $M_x$ and $N_b$ denote local measurement operators after the relevant local propagation. In this separated-system setup,

$$
(M_x\otimes I)(I\otimes N_b)
=(I\otimes N_b)(M_x\otimes I).
\tag{13}
$$

Both orderings give the same joint weights. More generally, completeness $\sum_bN_b^\dagger N_b=I$ yields

$$
\sum_b p(x,b)
=\langle\Psi|(M_x^\dagger M_x\otimes I)|\Psi\rangle.
\tag{14}
$$

Changing the local idler instrument cannot change this marginal. Selecting a particular idler outcome changes the conditional ensemble. No awareness-dependent update is required.

There is a useful check on “forgetting.” If an additional environment retains path records $|e_0\rangle,|e_1\rangle$, replace (9) with

$$
\frac{|0,0\rangle|e_0\rangle
+e^{i\phi}|1,1\rangle|e_1\rangle}{\sqrt2}.
$$

Writing $g=\langle e_0|e_1\rangle$, equation (11) becomes

$$
p(x,\pm)=\frac14\left[
|\psi_0|^2+|\psi_1|^2
\pm2\operatorname{Re}\!\left(e^{i\phi}\psi_0^*\psi_1g\right)
\right].
\tag{15}
$$

When $g=0$, those conditional fringes also disappear. Merely omitting a distinction from someone's awareness or description does not erase its physical consequences. A valid perspectival compression must preserve this overlap information whenever later protocols can reveal it.

## 5. What Planck's constant contributes

Where the propagator admits an action path integral, equation (2) has the schematic continuum form

$$
A(B)=\int_B e^{iS[\gamma]/\hbar}\,\mathcal D\gamma,
\qquad
\Delta\phi=\frac{\Delta S}{\hbar}.
\tag{16}
$$

The integration measure and normalization come from the specified propagator and its regularization. They are not supplied by $\hbar$ alone. [Feynman's action discussion](https://www.feynmanlectures.caltech.edu/II_19.html) supplies the relevant physical precedent: contributions with similar phase reinforce, while rapidly varying phases can cancel.

For one nondegenerate fluctuation coordinate near a stationary path,

$$
S(\xi)\simeq S_0+\tfrac12\kappa\xi^2,
\qquad
|\Delta\phi|\lesssim1
\ \Longrightarrow\ 
|\xi|\lesssim\sqrt{\frac{2\hbar}{|\kappa|}}.
\tag{17}
$$

This estimate gives a local scale of phase variation in the quadratic approximation. It is not a hard boundary of distinguishability: contributions outside it still exist, higher-order terms can matter, and other stationary regions can contribute.

The generalized uncertainty algebra and universal minimum-length claim suggested during drafting are not adopted here. The minimal construction needs neither. Coarse graining selects a description of an already quantum system; its discreteness alone does not derive quantum dynamics. Planck's constant controls action-to-phase conversion, while completeness and linearity supply representation consistency.

## 6. What this cleanup establishes

| Proposed feature | Status in this construction |
|---|---|
| Completed structure with no externally moving present | An available block interpretation of the full dynamics. |
| Multiway alternatives and accumulated branch amplitude | Exact finite representation, with complex weights and interference. |
| Past records and future possibilities relative to a perspective | Conditional quantum records, retaining environmental correlations. |
| Delayed-choice eraser | Recovered by equations (9)–(15). |
| Unique microscopic past fixed by present awareness | Not required or generally obtained. |
| Awareness as the cause of decoherence | Not derived; physical record correlations suffice here. |
| Every admissible perspective inhabited | An explicitly optional correspondence conjecture. |
| Awareness-defined universal resolution or Planck cutoff | No derivation in the present model. |
| Lushness of quantum futures | A further task; Born weight alone does not measure generative richness. |

For the last row, an exhaustive decoherent family has $\sum_\alpha p(\alpha)=1$, whether its continuations are sterile or generative. Its weights can inform a later lushness comparison, but their total alone cannot make that comparison. This supplies a candidate physical realization on which a later comparison could be defined; it does not supply the missing valuer-to-history correspondence or a lushness functional.

**Exact diagnostic.** Set $\phi=0$ and measure both signal and idler in the $\{|+\rangle,|-\rangle\}$ basis. Equation (15) gives the following joint probability matrices, with rows and columns ordered $+,-$:

$$
P_{g=1}=\begin{pmatrix}1/2&0\\0&1/2\end{pmatrix},
\qquad
P_{g=0}=\begin{pmatrix}1/4&1/4\\1/4&1/4\end{pmatrix}.
$$

Both have the same signal marginal $(1/2,1/2)$, while their joint records differ. Thus retaining the current signal state alone loses a distinction that a later joint protocol can reveal. This is an elementary quantum instance of the project's existing “same summary, different consequence” concern, not a newly claimed general theorem.

**Validation status.** The displayed identities follow by expansion and operator completeness. During drafting, a finite numerical check across 37 relative phases verified the eraser formula, normalization, signal marginals, and commuting local measurement order within $9\times10^{-16}$; a separate finite path-sum check agreed with direct matrix multiplication within $2\times10^{-16}$. These were drafting checks, not a retained repository validation suite. No new Lean theorem, experimental result, or independently reviewed derivation is claimed.

**Proposed core statement:** A perspective is situated within a complete quantum structure and accesses a physically specified record interface. Compatible quantum histories contribute through amplitudes and correlations; recorded alternatives carry Born weights when the relevant histories decohere. Awareness may be associated with such situated perspectives, without altering the quantum dynamics or privileging a moving present.

## Development provenance

The project author supplied the framework's motivating intuitions and corrections. OpenAI Codex assisted with mathematical reconstruction, source checking, calculation, and drafting. The physical formalism is attributed to its sources in place; the project-specific synthesis and unresolved correspondences are identified separately. This is a working research addendum and has not received independent peer review.

