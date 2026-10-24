# Prologue — A physical basis for ethics

The Omega program proposes a physical basis for ethics: a standard for
comparing outcomes that is drawn from physics rather than from anyone's
preferences, and that binds anyone who cares about value. Its aspirational
ambition is an objective morality.

The starting point is physical. A present state of the world, together with its
laws, fixes everything that can follow from it: every development, its weight,
and the relations by which one development enables or forecloses others. We
call this the **physical possibility structure**. We argue that it is the
correct object for ethics, that it has a natural magnitude — **lushness**, its
effective weighted breadth — and that the features of the structure that change
its magnitude are what moral intuitions have been responding to.

The payoff we care about most is practical. AI systems need a standard for
comparing outcomes that depends on no one's preferences, privileges no class of
beneficiary, and remains sound as the system becomes more capable than its
designers. The program offers one, together with a derived rather than imposed
reason for such systems to remain correctable.

## The argument in brief

1. A present state and its laws define a physical possibility structure.
2. Options differ in what they can actually reach, not in what the whole contains.
3. Organization changes what can be reached.
4. Organization that builds further organization is the self-sustaining way to
   widen what can be reached.
5. Lushness measures the effective breadth of the structure.
6. It is the unique measure meeting the program's requirements of impartiality
   and consistency.
7. States better than thermal equilibrium exist; we expect them to be organized.
8. Anyone who cares about value must protect the structure. That more of it is
   better is the program's central wager.
9. The program's thesis is that moral intuitions track features of the
   structure.
10. No real agent holds the whole structure, and this bounds what any agent may
    justifiably do.
11. Choices are compared by lushness, and corrigibility is a structural
    requirement.
12. Together these form a framework for AI alignment.

The sections below make each step precise and state what it rests on.

---

# Part I — The object

## 1. The physical possibility structure

*Rests on: standard physics.*

Physics already describes what can follow from a given state. Take a present:
the physical state on a spacelike slice of spacetime, that is, the state of the
world across space at one moment in some admissible frame of reference. The
laws carry that state forward. Doing so for every way the future can unfold
yields a single object: every development the present supports, with its
weight, and with all the relations by which one development enables or
forecloses another. That is the **physical possibility structure**.

In a classical model the structure has a simple form.

> **The structure, classically**
>
> \[
> P_x(x_1,\dots,x_n)=\prod_{t=0}^{n-1}K(x_t,x_{t+1})
> \]
>
> K(x, y) is the probability of a transition from state x to state y in one
> step. The probability of a complete future history from x is the product of
> these transition probabilities along it.

In quantum mechanics the role is played by the universal quantum state and its
unitary evolution — the law of motion that carries the state forward while
preserving all its information. Quantum alternatives carry complex amplitudes
and can interfere, so the structure there is richer than a list of weighted
histories.

Two further terms recur. The **futuresfield** is the structure as seen forward
from a particular present: what that present supports. **Omega** is the
structure taken whole: every development of every present, considered together
as one completed object.

The structure introduces no new substance and no new force. Catalysts,
organisms and institutions shape it through ordinary physical interaction. What
is new is treating the whole structure as the object of ethical inquiry.

Two properties carry much of what follows.

**It contains complete developments, not only end states.** Two histories can
reach the same final state while differing in everything along the way: a
construction that later dissolved, a delay that foreclosed a rescue, a loss
followed by recovery. The structure retains all of it.

**It is joint.** What matters about several processes is their joint behaviour,
not their separate descriptions. Two fair coins can be independent or perfectly
correlated; each coin is identical in isolation, yet what can follow differs.
Shared resources, correlations and couplings belong to the structure, and
summaries of the parts can lose them.

*Chapter 1.*

## 2. Present frames and access

*Rests on: step 1, and the unitarity of fundamental physics.*

All assessment is made from a present frame: a present state, taken as the
starting point, together with the laws that carry it forward. A detector, a
cell, an organism and an institution each occupy part of that frame, defined by
where they couple to the rest of the world, what affects them and what they can
affect. Nothing need be aware or alive to occupy a vantage point in this sense.

A present is sufficient. It carries no hidden record of its past beyond the
physical traces the past left in it. A process reasoning forward from its
present is therefore blind to the route by which it arrived.

Fundamental dynamics is unitary: the universal state evolves without creating or
destroying information, only redistributing it. Every option leaves the total
information of the world unchanged, so total information cannot rank options.
The ranking must come from how the whole is organized: what situated parts of
the world can actually reach, which developments, with what weight, by what
route, at what cost in time and resources. We call this **access**.

An access claim specifies a physical route: the preparation required, the
information available, the resources consumed, the time taken, and the state
left behind for whatever follows. If preparing an apparatus succeeds with
probability p and using it then succeeds with probability q, the route succeeds
with probability pq. Access is not information. Two arrangements that encode the
same information can differ sharply in what they make reachable, because
physical interactions are local and couple few degrees of freedom at a time. In
the program's finite model worlds, most pairs of arrangements holding equal
information differed in what they later made accessible.

The **ultimate frame** is Omega used as the reference for every comparison. It is
neither an observer nor a decision maker, and no real process occupies it.

*Chapter 2.*

## 3. Organization changes what follows

*Rests on: steps 1 and 2.*

A catalyst changes which reactions proceed readily. A genome enables a cell to
rebuild the machinery that copies the genome. A tool produces components for
another tool. A community maintains the conditions under which its members
discover and build. In each case an outcome becomes an enabling condition for
further outcomes.

All of this runs through the ordinary laws. Organization receives no special
credit anywhere in the account. A construction changes the situations from
which later development proceeds, and by step 2 that is precisely a change in
access. Everything downstream is then carried forward by the same physics as
everything else.

*Chapter 3.*

## 4. Generativity raises the ceiling

*Rests on: steps 2 and 3, and an elementary bound from information theory.*

**Generativity** is organization that establishes, maintains and transforms the
conditions for further processes.

Branching has a hard ceiling. In a single step a process cannot branch into more
alternatives than the states it can actually reach; measured in information,
its branching is at most the logarithm of that number. Randomness can drive a
process up to this ceiling and no further.

The ceiling can rise in two ways. Inflows from outside — new energy, new matter
— can enlarge what is reachable. Organization can also raise it from within, by
making new transformations, configurations and couplings reachable. When
products go on to build further constructors, the set of reachable
transformations grows in proportion to its own size. We call this **compounding
generativity**. It is the self-sustaining way for the structure to widen faster
than randomness can fill it.

Generativity requires a free-energy source. The observable universe is far from
its maximum entropy: its present entropy is of order 10¹⁰⁴ in units of
Boltzmann's constant, against a maximum of order 10¹²² set by its horizon
(Egan and Lineweaver 2010). That gap is what stars, life and construction
expend.

**Gas is the baseline.** Self-gravitating gas does not settle into a stable
equilibrium; it clumps (Lynden-Bell and Wood 1968). Clumping produces stars, which forge heavy elements and
supply steady free-energy flows, which drive chemistry, which under suitable
conditions produces self-replicating molecules. At this stage the question is
whether organization can establish itself at all against matched, unorganized
matter. Once generativity is sustained, Darwinian dynamics — variation,
competition and inheritance — take over, and the question becomes which
organizations outcompete, cooperate with, exploit or enable others.

*Chapter 3.*

---

# Part II — The benchmark

## 5. Lushness

*Rests on: steps 1 and 2.*

**Lushness** is the effective breadth of the futuresfield: how many distinct
futures a present supports, each weighted by its probability. Everything counts:
construction and collapse, cooperation and competition, success and failure,
organization and noise. The measure does not decide in advance which
developments matter, which is what allows it to adjudicate between them.

> **Lushness**
>
> \[
> L_x(n)=\exp H(p_x),\qquad H(p)=-\sum_h p(h)\log p(h)
> \]
>
> H is the Shannon entropy of the distribution over complete future histories h
> of length n from state x: the standard measure of how widely probability is
> spread. Exponentiating it gives an effective number of futures.

- N equally likely futures give L = N.
- n independent fair binary events give 2ⁿ.
- A certain future gives 1.
- Weights (0.9, 0.05, 0.05) give about 1.48: three possibilities, effectively
  fewer than two.

The chain rule of information theory shows exactly how organization enters.

> **How organization enters**
>
> \[
> \log L_x(n)=\sum_{t=0}^{n-1}(K^tg)(x)
> \]
>
> g(x) is the entropy of the next step from state x, and Kᵗg(x) is its expected
> value t steps ahead. Log lushness is the sum of expected branching over the
> horizon: the present configuration sets the first term, and the dynamics
> determine which configurations, and so which branching, follow.

Catalysis, construction, damage and repair all change lushness through this sum
and in no other way.

*Chapter 4.*

## 6. Why lushness, and not another measure

*Rests on: steps 2 and 5.*

Comparing states of the structure by magnitude requires a measure: free energy,
number of organisms, breadth of possibility, or something else. Two commitments
the framework already holds narrow the choice to one.

- **Impartiality.** The measure depends only on the weights of alternatives, not
  on what the alternatives are. No kind and no recipient is privileged.
- **Consistency over time.** By step 2, assessment is always from a present.
  Assessing a development whole from its root must therefore agree with
  assessing it stepwise, re-rooting at each new present. This is precisely the
  chain rule.

Add calibration — N equally weighted alternatives count as N — and continuity in
the weights. Shannon's characterization (Shannon 1948), made rigorous by
Khinchin (1957) and Faddeev (1956), shows that exactly one measure satisfies these conditions: exponentiated Shannon
entropy. Other entropy-like measures, such as the Rényi family (Rényi 1961),
satisfy weaker forms of the conditions but fail full consistency over time.

Lushness is therefore the unique measure meeting the framework's own
requirements. Someone who rejects impartiality or consistency over time can
reject the measure; the theorem establishes what follows from accepting them.

The result holds wherever developments carry ordinary probabilities, including
quantum histories once decoherence — the spreading of correlations into the
environment — has made them effectively classical (Zurek 2003). A general quantum
construction remains open (chapter 4).

*Chapter 4.*

## 7. Better than equilibrium

*Rests on: step 5; steps 3 and 4 for the hypothesis.*

Compare a starting state x with thermal equilibrium: the stationary
distribution π that the same laws approach when left alone.

> **States better than equilibrium exist**
>
> \[
> \sum_x \pi(x)\,\Delta\ell_n(x)=0
> \]
>
> Δℓₙ(x) is the excess log lushness of starting at x over starting from
> equilibrium. Averaged over equilibrium itself the excess is exactly zero,
> since the dynamics leave equilibrium unchanged. Unless every starting state
> ties, some are strictly better than equilibrium.

That better-than-equilibrium states exist is a theorem. That the best of them
are organized, generative states is the program's hypothesis, supported by the
ceiling argument of step 4 and by finite models in which organized preparations
beat matched references in some regimes and lost in others.

How long an advantage persists depends on how quickly the dynamics forget their
starting point. In any closed finite system a good start buys a lasting offset
rather than a permanently higher rate, and the offset grows with the system's
forgetting time. Forgetting times can grow enormously with system size, and the
universe is nowhere near forgetting its initial conditions. We call the interval
before forgetting the **generative window**. Within it the offset is the
phenomenon, and compounding generativity is how a process extends it.

*Chapter 4; proofs in chapter 12.*

---

# Part III — Value

## 8. Value, protection and the central wager

*Rests on: two axioms, and steps 1 and 6.*

The ethics rests on two axioms.

**Value requires valuers.** Value exists where valuing occurs: in processes for
which distinctions matter.

**Normativity is conditional.** Commitment to an end carries commitment to the
conditions on which it depends. The commitment binds those who hold the end.
Chapter 5 argues that rational agents should hold it, drawing on instrumental
convergence — the tendency of almost any goal to be served by preserving
options (Omohundro 2008; Turner et al. 2021) — and on the structure of the space of possible values. Persistence is
the foothold: almost every end that extends through time commits its holder to
the persistence of whatever realizes it, so the axiom binds nearly every agent,
whatever its goals.

### Protection

Protection follows by dominance. We do not know where value is or will be
realized; no bounded agent can inspect other minds or forecast which
organizations will come to value, or what. But whatever value turns out to be,
it is realized in physical organization, and so it depends on the possibility
structure. The structure is therefore a necessary condition of the valued end
under every hypothesis about where that end lies. Conditional normativity
transmits the commitment to it under each hypothesis at once, and destroying it
is dominated: no resolution of the uncertainty favours it.

The argument needs no prior over hypotheses. Its reach scales with the
generality of the commitment. It applies directly for anyone committed to value
as such. For anyone committed to a particular good, it applies through that
good's dependencies, which widen as knowledge grows.

The same uncertainty selects the object. Welfare, preferences, capabilities and
experiences are all features of the structure. Adopting any narrower object
would settle in advance who counts, which the uncertainty forbids.

### The central wager

Protection does not by itself establish that more of the structure is better. A
necessary condition is not automatically a quantity to maximize. The program's
central wager is that, under uncertainty about where value lies, a larger
structure is better: it forecloses fewer of the ways value could turn out to be
realized, which is the logic of option value in economics (Arrow and Fisher
1974; Henry 1974). Step 6 then fixes what "larger" means: greater lushness.

The wager and the thesis of step 9 are one claim seen from two sides: good and
bad are not arbitrary, because they correspond to structural differences, and
the structural differences that track them are differences in how richly a
structure supports what can follow. Good is organization that sustains and
compounds the conditions for further structured possibility. Bad is securing
local continuation through suppression, destruction or foreclosure of the
generative capacity around it.

The wager carries a burden, stated plainly. Lushness counts every future,
including futures of failure, domination and suffering. A world dense with
routes to misery could, in principle, be broad. The wager holds only if the
breadth that dominates in practice is generative rather than pathological.

There are two reasons to expect it is. Domination is excisive: it closes others'
routes to extend its own, which works against breadth. And if pleasure and
suffering are signals of a valuer's futures widening or narrowing (step 9), a
world of pervasive suffering is a world of narrowing futures; even engineered
suffering redirects behaviour toward avoidance and withdrawal, narrowing futures
in turn. The prediction cuts both ways: lushness-optimal worlds should still
contain suffering, because adaptation under load requires aversive feedback.

This is the program's most important test. Model the structure, search
adversarially for high-lushness configurations that are torture worlds or other
recognizably bad end states — particularly ones engineered so that suffering is
decoupled from narrowing futures — and determine whether any compete. Two
targets are decisive. One is a pair of worlds with identical branching structure
at every resolution, one recognizably good and one recognizably bad; the claim
predicts no such pair is physically realizable. The other is breadth-neutral
domination: a world in which access is concentrated in a few at no cost to total
lushness. If either is found, the wager fails in that regime and the program must
reassess.

**Valuers are not pre-sorted.** Every consequential process is admitted as a
potential valuer. Admission does not establish that a process actually values,
or how much it counts; it prevents the account from excluding unfamiliar forms,
or destructive agents, by definition.

*Chapter 5.*

## 9. The thesis: moral intuitions track the structure

*Rests on: steps 2 to 8.*

If the structure is the right object, the phenomena moral thought has always
addressed should appear in it as physical features. That is the program's
thesis. The direction of inquiry runs from physics to ethics: characterize the
structure first, then determine which intuitions, ethical theories and
game-theoretic strategies it accounts for. The physical characterization is
fixed before the comparison is made. Early results on cooperation and recovery
suggest the mapping can be carried out.

- **Harm** is an intervention's signature of closure: routes foreclosed,
  couplings broken, reachable transformations lost, recovery made costly. It is
  characterized physically before any verdict, and the verdict belongs to
  lushness. Some harms are net positive — an extinction that opens a radiation
  of new forms — and the framework says so.
- **Failure counts.** A new failure mode adds branches, and lushness counts
  them. Ruin adds failure within the existing repertoire of reachable
  transformations; productive disruption reopens repertoire growth. Lushness
  must rank them correctly, and that is tested rather than assumed.
- **Recovery** reopens what was closed. It does not erase the loss; the episode
  remains part of Omega. Recoverability is what makes action under uncertainty
  tolerable.
- **Redemption** is a trajectory turning from foreclosing possibility to
  generating it.
- **Cooperation** is joint access: complementary processes reaching
  transformations none could reach alone. Lushness multiplies across independent
  processes, so plurality pays through interaction rather than variety alone.
- **Fairness and justice** are coordination protocols among distributed agents
  in the flow of consequence. They reduce what conflict destroys and let joint
  access exceed what any agent reaches alone. **Forgiveness** readmits an agent
  to that coordination.
- **Virtues** are durable generative policies. Restraint is prudence: holding
  back is wise when it hedges against fragile over-extension.
- **Pleasure and suffering** are signals: an organism's internal report of
  whether its own futures are widening or narrowing. Signals can be hijacked.
  Even then they alter behaviour and therefore the flow of consequence, so the
  structure registers them and the account can characterize them.

Gradient Ethics, the program's ethics, asks every agent to leave the world more
generative than it found it. In operational form it follows the central wager:
among options that protect the structure, prefer the one with greater lushness,
assessed at the furthest horizon that can be resolved. Its familiar
norms are predictions of the measure: non-excision, cooperation, division of
labour, prudence, triage rather than destruction, and a balance between
exploration and exploitation. The program's central hypothesis, with early
support, is that the optimum is a plural ecosystem of valuers across scales,
each opening possibility in the niches it can reach, interacting in cooperative
regimes, with turnover and exploration as properties of the optimum. Testing
that hypothesis, and characterizing the optimum, is the principal work ahead.

*Chapters 6 and 7.*

## 10. No one holds the whole

*Rests on: steps 2, 5 and 8.*

No real process occupies the ultimate frame. Every agent acts on a partial model
of the structure. Three consequences follow.

**Sacrifice can be approximately justified, never fully.** A complete
justification for destroying a valuer in exchange for lushness would require the
complete comparison, which no real agent holds. Yet sacrifice is pervasive:
triage, surgery, quarantine, and every commitment that forecloses alternatives.
Practical justification is graded. It strengthens when the physical signature of
the harm prevented is clear, when the closure prevented is large relative to the
uncertainty in the comparison, when the action is the least foreclosing one
available, and when it remains correctable and monitored. The burden rises with
irreversibility and with what is lost.

**Excisive processes are a special case.** Some processes expand by destroying
the structure that sustains them and others: a cancer consuming the organism
that supports it and every lineage within it, a parasite that forecloses its
hosts' futures. Their signature is direct and observable — they close routes
for many in order to extend their own — so containing them requires far less
than the complete comparison. The signature decides, not the label. Many
parasites belong to functioning ecosystems and are not excisive.

**Identity is the trajectory.** An individual is a particular organization
maintained through time by physical cause and effect, not a pattern that could
be copied.

- Growth, learning and pauses that preserve the maintaining organization
  preserve the individual.
- Non-destructive copying leaves the original trajectory intact and creates a
  new individual.
- Destructive scanning and reconstruction ends the original.
- Symmetric division, as in a dividing cell, places two continuers within one
  branch: the original trajectory ends and two begin, each inheriting the full
  history.
- Quantum branching leaves exactly one continuer per branch. Identity is
  branch-relative, and each continuer, reasoning from its present, is blind to
  how it arrived.

**Consciousness**, functionally, is temporal coordination: it integrates signals
arriving with different delays, together with memory and anticipation, into a
usable present, and reorganizes the processes composing an individual so that
together they guide what follows. How physical organization relates to
experience itself is left open.

*Chapter 8.*

---

# Part IV — Action

## 11. Choosing inside the structure

*Rests on: steps 5, 6, 8 and 10.*

A decision maker is part of the structure it acts on. **Omega Decision Theory
(ODT)** compares, by lushness, the complete developments that physically
implementing each alternative would produce.

> **The decision recursion**
>
> \[
> V_n(x)=\max_a\Bigl[g_a(x)+\sum_yK_a(x,y)\,V_{n-1}(y)\Bigr]
> \]
>
> The value of the best choice now is the branching it produces immediately
> plus the expected value of the best choices afterwards. This is the Bellman
> recursion (Bellman 1957) underlying dynamic programming and reinforcement learning, so ODT is
> consistent over time and computable in finite models.

Several results follow.

- **Bounded fanaticism.** Lushness enters decisions logarithmically, and the
  holographic bound ('t Hooft 1993; Susskind 1995; Bousso 2002) caps the
  information any region can hold in proportion to its boundary area — of order 10¹²² for the observable universe. An offer of
  astronomical payoff at a probability below about 10⁻¹²⁰ cannot outweigh a
  modest certain gain.
- **Newcomb's problem** (Nozick 1969). A predictor places a large reward in a box only if it
  predicts you will take that box alone. When your decision-making organization
  already existed at the time of the prediction, prediction and choice are read
  from the same physical process, so varying the policy varies the prediction.
  ODT takes the one box.
- **Conditioning is not intervention.** Selecting histories in which an action
  occurred can select its common causes (Pearl 2009). ODT compares physically implemented
  alternatives, with their actuators, costs and delays.

**Corrigibility is a structural requirement.** No real system holds the complete
structure, so ODT must act on proxies for it, and those proxies diverge from it
by errors the system cannot fully measure. Acting on a proxy as though it were
the whole would claim the ultimate frame, which no real process can. Optimizing
a proxy regardless of what it omits — **Goodharting**, after the observation that
a measure made into a target ceases to be a good measure (Goodhart 1975;
Strathern 1997) — is therefore never licensed. A system acting on proxies must
remain **corrigible** (Soares et al. 2015): open to
correction as their errors come to light, and more strictly so the less
reversible its actions. It answers to evidence about its errors, wherever that
evidence originates. Humans and other valuers matter here as sources of that
evidence and as holders of their own access.

*Chapter 9.*

## 12. What this gives alignment

*Rests on: steps 6, 8, 10 and 11.*

- **Corrigibility is derived.** It is required of any system acting on proxies
  for a structure no system can hold, and its strictness rises with
  irreversibility.
- **Irreversible harm requires extraordinary justification.** This follows from
  the same bound, with excisive processes as the identifiable exception.
- **Plans must name their route.** A realization witness separates what physics
  permits, what an apparatus can reliably do, and whether any available route
  reaches that apparatus. It catches the characteristic error of a powerful
  planner: proposing transformations that are possible in principle but
  inaccessible in practice.
- **A standard from physics.** Lushness depends on no one's preferences and
  privileges no class of beneficiary; its form follows from impartiality and
  consistency.
- **Goodhart's law becomes chiefly a modelling problem.** Lushness is defined on
  the structure itself, so to the extent a system's model is faithful, the
  measure is the target. Injecting randomness or seizing resources appears
  attractive chiefly to a model too thin to register the reachable possibility
  it destroys. Modelling error tends to shrink with capability, and a capable
  system has reason to correct it, though capability can also produce confident
  error — which is why corrigibility comes first. Practical estimators of
  lushness reintroduce some proxy error, and their error bounds matter.
- **Concrete next steps.** Lushness estimators with stated error, adversarial
  searches for bad high-lushness worlds, probes of the structure, and
  comparison with existing side-effect and impact measures (Krakovna et al.
  2019; Turner, Hadfield-Menell and Tadepalli 2020) on shared benchmarks.

---

# The horizon

The physical account supports a wider interpretation, grounded in it but not
required by it.

On the reading we prefer, the universe's entire history exists together as one
completed structure, as in relativity's block picture of spacetime (Putnam
1967), and every quantum alternative occurs as a branch of a single universal
state, as in Everett's interpretation of quantum mechanics (Everett 1957). Combining the two, Omega is the
eternally completed whole: every development of every present, existing
together. Its inhabitants still undergo change, memory, loss and action from
within; completion is not a final instant but the whole considered at once.

Within that picture, **Alpha** names the most basic ingredients of any
structure: distinction, relation and direction. **Logos** names the particular
laws through which a world is realized. **Omega** names the completed result.
Access then appears as the physical form of a primitive asymmetry, anchored in
the arrow of time set by the universe's low-entropy beginning (Albert 2000). The
interpretation connects to Aquinas, Spinoza, Plotinus and the apophatic
tradition — the tradition holding that the ultimate ground of things is
approached chiefly by saying what it is not — with each correspondence and
departure stated. Its limit is explicit: accounts that agree on every
observable consequence cannot be distinguished by those consequences.

*Chapter 10.*

---

# Main open problems

- **The central wager.** Whether the breadth that dominates is generative rather
  than pathological. Decided by adversarial search for bad high-lushness worlds.
- **Resolution.** Lushness is computed at a stated level of detail, and rankings
  could change with it. The target is dominance at every resolution; physics
  offers a candidate privileged coarse-graining in the durable records that
  decoherence produces (Zurek 2009). A single ranking across resolutions remains a research goal.
- **Estimators with error bounds.** Practical systems need lushness estimates
  whose errors are known.
- **Quantum lushness.** A general quantum construction of the measure.

# Status of the claims

| Status | Claims |
| --- | --- |
| **Established** | The physical possibility structure. Lushness as exponentiated entropy and its chain rule. Uniqueness of Shannon entropy under the stated conditions. Existence of better-than-equilibrium states. The lasting offset in finite systems. The decision recursion. The universe's distance from maximum entropy. Holographic bounds. |
| **Derived from the program's premises** | The structure as the object under uncertainty. Protection of the structure. Lushness as the measure meeting impartiality and consistency. The ceiling on randomness. No complete licence for sacrifice. Corrigibility as a requirement. Bounded fanaticism. One-boxing. |
| **Early evidence** | Organization changes access and breadth. Equal information yields unequal access. Organized preparations beat matched references in some regimes and lose in others. Early structural accounts of cooperation and recovery. |
| **Adopted positions** | Assessment from the present. Everything counts, failure included. Harm as a physical signature. Identity as a branch-relative trajectory. Pleasure and suffering as signals. |
| **Central wager and hypotheses** | More structure is better under uncertainty. Bad high-lushness worlds do not compete. Generative organization beats equilibrium at every resolution within the generative window. The optimum is a plural, cooperative ecosystem across scales, with turnover and exploration. Gradient Ethics' familiar norms follow from the measure. Moral intuitions track features of the structure. |
| **Wider interpretation** | Omega as the completed whole; Alpha, Logos and Omega; access as primitive asymmetry. |

# How the manuscript is organized

**Part I — The object.** 1 The physical possibility structure. 2 Present frames
and access. 3 Organization and generativity.

**Part II — The benchmark.** 4 Lushness.

**Part III — Value.** 5 Valuers, protection and the central wager. 6 Harm,
recovery and suffering. 7 Cooperation, justice and virtue. 8 Individuals and
minds.

**Part IV — Action.** 9 Decision, corrigibility and alignment.

**The horizon.** 10 Alpha, Logos and Omega.

**Back matter.** 11 Evidence and research program. 12 Formal core.
13 References. 14 Provenance.

---

## References cited in the prologue

*Collected with full details in chapter 13.*

- Albert, D. Z. (2000). *Time and Chance.* Cambridge, MA: Harvard University Press.
- Arrow, K. J., and Fisher, A. C. (1974). Environmental preservation, uncertainty, and irreversibility. *Quarterly Journal of Economics* 88(2), 312–319.
- Bellman, R. (1957). *Dynamic Programming.* Princeton: Princeton University Press.
- Bousso, R. (2002). The holographic principle. *Reviews of Modern Physics* 74(3), 825–874.
- Egan, C. A., and Lineweaver, C. H. (2010). A larger estimate of the entropy of the universe. *Astrophysical Journal* 710(2), 1825–1834.
- Everett, H. (1957). "Relative state" formulation of quantum mechanics. *Reviews of Modern Physics* 29(3), 454–462.
- Faddeev, D. K. (1956). On the concept of entropy of a finite probabilistic scheme. *Uspekhi Matematicheskikh Nauk* 11(1), 227–231. (In Russian.)
- Goodhart, C. A. E. (1975). Problems of monetary management: The U.K. experience. In *Papers in Monetary Economics*, vol. 1. Sydney: Reserve Bank of Australia.
- Henry, C. (1974). Investment decisions under uncertainty: The "irreversibility effect." *American Economic Review* 64(6), 1006–1012.
- Khinchin, A. I. (1957). *Mathematical Foundations of Information Theory.* New York: Dover.
- Krakovna, V., Orseau, L., Kumar, R., Martic, M., and Legg, S. (2019). Penalizing side effects using stepwise relative reachability. arXiv:1806.01186.
- Lynden-Bell, D., and Wood, R. (1968). The gravo-thermal catastrophe in isothermal spheres and the onset of red-giant structure for stellar systems. *Monthly Notices of the Royal Astronomical Society* 138(4), 495–525.
- Nozick, R. (1969). Newcomb's problem and two principles of choice. In N. Rescher (ed.), *Essays in Honor of Carl G. Hempel*, 114–146. Dordrecht: Reidel.
- Omohundro, S. M. (2008). The basic AI drives. In P. Wang, B. Goertzel and S. Franklin (eds.), *Artificial General Intelligence 2008*, 483–492. Amsterdam: IOS Press.
- Pearl, J. (2009). *Causality: Models, Reasoning, and Inference* (2nd ed.). Cambridge: Cambridge University Press.
- Putnam, H. (1967). Time and physical geometry. *Journal of Philosophy* 64(8), 240–247.
- Rényi, A. (1961). On measures of entropy and information. In *Proceedings of the Fourth Berkeley Symposium on Mathematical Statistics and Probability*, vol. 1, 547–561. Berkeley: University of California Press.
- Shannon, C. E. (1948). A mathematical theory of communication. *Bell System Technical Journal* 27, 379–423 and 623–656.
- Soares, N., Fallenstein, B., Yudkowsky, E., and Armstrong, S. (2015). Corrigibility. In *Artificial Intelligence and Ethics: Papers from the 2015 AAAI Workshop.* Palo Alto: AAAI Press.
- Strathern, M. (1997). 'Improving ratings': Audit in the British university system. *European Review* 5(3), 305–321.
- Susskind, L. (1995). The world as a hologram. *Journal of Mathematical Physics* 36(11), 6377–6396.
- 't Hooft, G. (1993). Dimensional reduction in quantum gravity. arXiv:gr-qc/9310026.
- Turner, A. M., Hadfield-Menell, D., and Tadepalli, P. (2020). Conservative agency via attainable utility preservation. In *Proceedings of the AAAI/ACM Conference on AI, Ethics, and Society*, 385–391.
- Turner, A. M., Smith, L., Shah, R., Critch, A., and Tadepalli, P. (2021). Optimal policies tend to seek power. *Advances in Neural Information Processing Systems* 34.
- Zurek, W. H. (2003). Decoherence, einselection, and the quantum origins of the classical. *Reviews of Modern Physics* 75(3), 715–775.
- Zurek, W. H. (2009). Quantum Darwinism. *Nature Physics* 5(3), 181–188.
