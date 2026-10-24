# 14 — A compact formal core

This section fixes one tractable setting: finite-dimensional quantum systems, finitely many interaction slots, and specified interfaces. Classical stochastic models are included through diagonal states and classical operations. Relativistic and field-theoretic extensions require their appropriate algebras and boundary structures.

## A. Quantum ingredients

A state ρ is positive semidefinite with Tr ρ = 1. A channel E is completely positive and trace preserving. An effect F satisfies 0 ≤ F ≤ I. An instrument {M_o} consists of completely positive trace-nonincreasing maps whose sum is a channel.

For a physical outcome o:

```text
p(o) = Tr[M_o(ρ)]
ρ_o  = M_o(ρ) / p(o),                    when p(o) > 0.
```

Retain the pair (p(o), ρ_o), or the unnormalized state M_o(ρ), when comparing occurrence weight and conditional structure. Conditional normalization alone discards p(o).

For a downstream effect F:

```text
p(F | ρ) = Tr[F E(ρ)] = Tr[E*(F) ρ].
```

This equality is the definition of the dual map under the trace pairing. It supplies the elementary focus construction. [R06–R08]

## B. Residual processes and testers

Let Υ_x denote the residual process associated with physical boundary condition x. An admissible tester T is a causally ordered sequence of allowed interventions, ancillas, and final readout on the specified interface. Write its outcome law as p_Υx^T(y).

Process tensors or quantum combs represent these multi-time response laws, with positivity and causal normalization constraints. Use one explicit Choi convention when implementing them; tensor order and transposes must follow that convention. The abstract probability pairing avoids hiding a convention in notation. Interactive strategy discrimination supplies corresponding operational distance machinery. [R15, R31, R36]

For a nonempty tester family T_H, define:

```text
d_H(x, x′) = sup_{T ∈ T_H} ½ Σ_y |p_Υx^T(y) − p_Υx′^T(y)|.
```

Define x ~_H x′ when d_H(x,x′)=0 and Γ_H as the resulting quotient of the physical condition domain. Each tester's output distribution is normalized. The metric compares normalized residual processes; separately retain any weight associated with the boundary conditioning itself.

### Proposition 1: exact equivalence and horizon refinement

The relation ~_H is an equivalence relation. If T_H is contained in T_H′, then d_H ≤ d_H′, and equivalence at H′ implies equivalence at H.

**Derivation.** Equality of all corresponding probability laws is reflexive, symmetric, and transitive. A supremum over a subset cannot exceed the supremum over the larger set. Thus expanding admissible continuation can separate classes but cannot merge classes already distinguished.

The distance is a pseudometric on physical conditions and a metric on its zero-distance quotient. Finiteness of the underlying Hilbert space does not imply that this quotient has finitely many points.

## C. Compression and composition

An encoding q maps concrete conditions to abstract representations. A decoder or abstract process assignment produces predictions p̂_q(x)^T. Require a uniform error bound in the declared domain:

```text
sup_{x,T} TV[p_Υx^T, p̂_q(x)^T] ≤ ε.
```

If q(x)=q(x′), the triangle inequality gives d_H(x,x′) ≤ 2ε. Thus an encoding that merges perfectly distinguishable conditions cannot satisfy ε < 1/2 for that tester domain.

For exact deterministic updates F_a, abstraction respects composition when abstract updates F̄_a exist satisfying q∘F_a = F̄_a∘q. In probabilistic settings the corresponding pushforward laws must agree. In quantum settings use physical maps and valid encodings rather than assuming every set-theoretic quotient is a quantum channel.

### Proposition 2: restricted operational contraction

Suppose a transformation Φ maps the compared processes to a new interface, and every admissible output tester composed with Φ is an admissible input tester. Then:

```text
d_out(Φx, Φx′) ≤ d_in(x, x′).
```

**Derivation.** Every difference visible after Φ already belongs to a test included in the input supremum. The output supremum therefore cannot exceed the input one.

This statement concerns the corresponding tester domains. A reversible transformation with reversible access in both directions preserves distance. For closed unitary dynamics and unrestricted global measurements, distinguishability is preserved. Substantial compression then comes from a specified restriction, redundancy of representation, or effective description; it cannot be obtained by silently deleting globally accessible information.

### Proposition 3: a covariance summary is not closed under continuation

For x,y,z∈{−1,+1}, let P_t(x,y,z)=(1+txyz)/8, −1≤t≤1. Let q(P) retain the three means and their covariance. Then q(P_t)=(0,I₃) for every t. Under the fixed reversible transformation F(x,y,z)=(x,y,xyz):

```text
mean(F_*P_t) = (0,0,t)
cov(F_*P_t)  = diag(1,1,1−t²).
```

**Derivation.** Every nonconstant product moment except E[XYZ]=t vanishes. Each initial squared coordinate is one. At the output, E[XYZ]=t is the last-coordinate mean, while its products with X and Y reduce to YZ and XZ and still have zero expectation. Thus equal q(P_t) have different q(F_*P_t), precluding any exact F̄ with q∘F_*=F̄∘q on this family.

For these states, TV(P_t,P_s)=|t−s|/2, so the full probability laws already distinguish the preparations. Covariance loses a distinction retained by the full continuation object. This is a failure of sufficiency for exact update, not a proof that every scalar comparison must separate the states.

### Observable completion from the permitted tests

The functions 1,X,Y,Z,XY,XZ,YZ span seven dimensions of the eight-dimensional function space on the register. The future last-coordinate readout composed with F is XYZ, the missing eighth function. For S⊆{1,2,3}, write χ_S(x)=∏_(i∈S)x_i, with χ_∅=1. Their orthogonality gives:

```text
Σ_x χ_S(x)χ_T(x) = 8 if S=T, and 0 otherwise.
P(x) = (1/8) Σ_S E_P[χ_S] χ_S(x).
```

Adding the observable required by the actual continuation therefore reconstructs every joint law in this finite classical domain. In larger classical or quantum models, start from the declared readouts and close their linear span under pullback through permitted operations. A quantum pullback is the dual map. Closure and the relevant conditioning branches determine what expectations must be retained; economical finite closure is not guaranteed. Adding a feature because a permitted continuation requires it differs from assigning that feature an evaluative bonus.

### Proposition 4: conditional transfer in the three-bit device

Let an independent input U first multiply Z. Apply the parity decoder and expose only W=UXYZ. Then:

```text
K_t(w|u) = (1+tuw)/2.
TV(K_t(·|+1), K_t(·|−1)) = |t|.
Best input recovery under fair U = (1+|t|)/2.
```

**Derivation.** The sign A=XYZ has mean t, hence P(A=a)=(1+ta)/2. Since W=UA, the response law follows. For binary fair-input discrimination the best success is one half plus one half of the output total variation.

A balanced readout f after the input flip gives the same formula with t replaced by tc_f, where c_f=(1/8)Σ_xyz xyz f(x,y,z). Enumerating the 70 balanced functions gives 36 with c_f=0, 16 each with c_f=±1/2, and one each with c_f=±1. Every such readout extends to a reversible eight-state permutation. This exhausts that readout class, not all possible quantum interventions or added resources.

For |s|≤|t| and t≠0, receiver postprocessing V=RW with an independent sign of mean s/t transforms K_t into K_s. The t=s=0 case is immediate. No receiver-only stochastic map can accomplish |s|>|t|: writing a=P(V=+1|W=+1) and b=P(V=+1|W=−1), the difference of conditional output probabilities is multiplied by a−b∈[−1,1]. This is a conditional simulation order for these channels.

The entire register output is uniform after averaging over fair U, although the joint law retains E[UW]=t. This establishes the need for conditional response structure when assessing transfer. The full model retains U and every register output; unrestricted access to U trivially reveals the input for every t. The result concerns transfer to the specified receiver, with the interface restrictions in Part 13.

## D. Consequence geometry and candidate lushness profiles

Retain the family of Γ_H with its refinement relations, conditional updates, physical composition, and applicable weights. For a totally bounded Γ_H, let N_ε(Γ_H,d_H) be the minimum number of radius-ε balls required to cover it. Define the candidate support profile:

```text
L_support(H, ε) = log N_ε(Γ_H, d_H).
```

The domain whose cover is taken must be specified: all states permitted by resources, states reachable from a fixed boundary, or a physically supplied ensemble are different objects. A chosen ensemble over quantum states is not automatically a uniquely given branching decomposition.

If decoherent alternatives or preparation statistics supply a probability measure μ, and a justified feature map φ takes values in R^d with finite second moments, define:

```text
m = ∫ φ(x) dμ(x)
Σ = ∫ [φ(x)−m][φ(x)−m]ᵀ dμ(x)
L_cov(β) = log det(I + βΣ),              β > 0.
```

Choose units so βΣ is dimensionless. Unless specified otherwise, logarithms here are natural. L_cov is invariant under orthogonal changes of feature coordinates, not arbitrary rescaling.

For a declared positive-definite feature metric M, use the dimensionless symmetric product βM^(1/2)ΣM^(1/2):

```text
L_cov(β,M) = log det(I+βM^(1/2)ΣM^(1/2))
           = log det(I+βΣM).
```

Under an invertible coordinate change φ′=Sφ, Σ′=SΣSᵀ and M′=S^(−T)MS^(−1). Then Σ′M′=SΣMS^(−1), so the determinant and score are invariant. Holding M fixed while changing units generally changes the modeled metric. Its physical justification remains separate from coordinate invariance.

### Proposition 5: fixed-trace spread

For eigenvalues λ_i ≥ 0 with Σ_i λ_i = M in a fixed d-dimensional feature space:

```text
Σ_i log(1 + βλ_i) ≤ d log(1 + βM/d).
```

**Derivation.** The function log(1+βλ) is concave, so Jensen's inequality gives the bound. Equality occurs when all λ_i=M/d. For r > 1 positive equal directions, strict concavity gives r log(1+βM/r) > log(1+βM) when M > 0.

This is a result about the candidate statistic under its coordinate assumptions. It does not establish a value ordering.

### A calibration boundary with explicit preparations

Let C be uniform on (±2,0), D uniform on the four points (±1,±1), and E uniform on (±1,±1/2). Use the same coordinate readouts and M=diag(1,q), with β,q>0. Their covariances are diag(4,0), diag(1,1), and diag(1,1/4), respectively. Thus:

```text
exp L_C = 1+4β
exp L_D = (1+β)(1+qβ)
exp L_E = (1+β)(1+qβ/4)
exp L_D − exp L_C = β[q(1+β)−3].
```

D wins when q(1+β)>3, C wins when it is smaller, and they tie on the boundary. E is strictly below D throughout this positive parameter domain. At q=1 the C/D crossover is β=2. These are explicit distributions on a common finite alphabet; equal preparation cost is not assumed. The result characterizes a candidate comparison's calibration dependence and its limits, rather than assigning the preparations ethical roles.

### A rare-event bound and its cost

Consider orthogonal records 0,1,…,m with weights P(0)=1−p and P(i)=p/m, where m≥1 and 0≤p≤1. For 0<p<1 the support contains m+1 records regardless of how small p is; its distance from the point mass at 0 is p in total variation. Shannon entropy is h₂(p)+p log₂m bits, which is not uniformly bounded in m at fixed positive p.

Fix the feature convention φ(0)=0 and φ(i)=e_i, so each feature vector has norm at most one, and use M=I. Then:

```text
Σ = (p/m)I − (p²/m²)11ᵀ
L_cov = (m−1)log(1+βp/m) + log(1+βp(1−p)/m)
0 ≤ L_cov ≤ β Tr Σ = β(p−p²/m) ≤ βp.
```

**Derivation.** The covariance has eigenvalue p/m in the m−1 directions perpendicular to 1, and p(1−p)/m along 1. Apply log(1+x)≤x to its nonnegative eigenvalues. For fixed p and β, L_cov approaches βp as m→∞. The uniform tail bound therefore accompanies saturation with breadth. It depends on the bounded feature normalization and fixed β; it is not a bound on every physical consequence or value functional.

### Probability-weighted covers

For a declared domain Γ, metric d, and physical probability measure μ, define closed balls B_ε(x) with centers in Γ. For ε≥0 and 0≤δ<1:

```text
N_(ε,δ)(Γ,d,μ) = inf {|C| : C is a finite subset of Γ,
                         μ(⋃_(c∈C) B_ε(c)) ≥ 1−δ}.
```

Set the result to infinity if no finite cover meets the requirement. Keep its dependence on ε,δ, horizon, and interface. Covering probability one is not in general the same as covering every point of the declared domain. For a finite positive-weight support, δ=0 does require every support point.

For the two response laws K_t(·|±1) with equal physical input weights, centers in that response family, and closed balls:

```text
N_(ε,δ) = 1 when ε≥|t| or δ≥1/2;
          2 otherwise.
```

The domain collapses to one response at t=0. Allowing centers outside the family would change the radius boundary, so the center convention is part of the construction.

### Similarity-sensitive effective diversity

For a finite ensemble {x_i,p_i}, p_i≥0 and Σ_i p_i=1, choose a symmetric similarity matrix Z with 0≤Z_ij≤1 and Z_ii=1. The Leinster–Cobbold order-two diversity is [R35]:

```text
D₂(p,Z) = 1/(pᵀZp).
```

With operational distance d∈[0,1], Z_ij=1−d(x_i,x_j) is one explicit choice. For identical responses D₂=1; for pairwise perfectly distinguished responses it is 1/Σ_i p_i². Splitting a weight among indistinguishable duplicate labels leaves the value unchanged when their similarities to every member also agree.

For the fair-input parity response family:

```text
Z = [[1,1−|t|],[1−|t|,1]]
D₂ = 1/(1−|t|/2).
```

It increases from 1 to 2 as the two responses become distinguishable. This agrees with the specified channel capability order. Neither this similarity choice nor an ensemble over all interventions is selected uniquely by physics. The test validates discrimination of a known response difference; it does not validate D₂ as global lushness or make higher-order correlation intrinsically valuable.

## E. Recovery and compatibility

For a transition model x_{t+1}=f(x_t,a_t,e_t), a target A, and admissible policy class Π, existential recovery means some allowed policy and contingency realization reaches A by H. Robust recovery requires one policy securing the registered recovery criterion for every allowed contingency sequence. A policy may condition on information actually available at its decision points.

For requirements R_i on complete allowed continuations z, define:

```text
Real(F) = {z : R_i(z) holds for every i ∈ F}
May(F)  iff Real(F) ≠ ∅
Robust_E(F) iff ∃π ∈ Π ∀e ∈ E : outcome(π,e) ∈ Real(F).
```

Assume outcomes are valid continuations and E is nonempty. Robust_E(F) then implies May(F): choose any e from E and use the securing policy's outcome.

Adding requirements shrinks Real(F). Enlarging E can only shrink the set of securing policies. The converse from May to Robust fails, as do the inferences from individual to joint recovery and from pairwise to full compatibility. Part 13 gives finite counterexamples.

For success regions S_π={e : outcome(π,e) ∈ Real(F)}, define a policy-cover number:

```text
κ_F(E) = inf {|P| : P ⊆ Π and E ⊆ ⋃_{π∈P} S_π},
```

with infinity when no cover exists. A finite cover records complementary policy success. Its execution requires a realizable selector or an equivalent adaptive policy.

## F. A finite decision frame

Let A be a finite nonempty action set. Let C(a) be the declared corridor criterion, and J(a) the model-to-world justification criterion. ODT0 returns:

```text
A₀ = {a ∈ A : C(a) and J(a)}.
```

These predicates contain the substantive physical and normative work. Writing them down does not verify them.

Given a preorder ≽ over A₀, ODT1 retains actions not strictly dominated. For finite nonempty A₀ this frontier is nonempty. ODT2 selects from it using registered arbitration. If A₀ is empty, an explicitly specified emergency procedure is required; the empty licensed set is itself an informative outcome.

This formal core is sufficient to begin finite probes of focus, consequential equivalence, compression, recovery, compatibility, and candidate lushness. The extension to the full physical object remains the organizing research direction.
