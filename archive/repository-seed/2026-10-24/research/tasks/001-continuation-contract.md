# Task 001 — Make the finite continuation object a shared research contract

**Status:** proposed; not started.  
**Suggested first GitHub issue title:** Specify continuation preservation and
adapt the existing feedback probe.  
**Purpose:** ensure that later experiments test the intended object rather
than silently replace it with whichever representation is easiest to compute.

## Why this comes first

Formal note 10 already defines a finite continuation object. P001 has a working
implementation for one diagonal fixture, but its representation and summaries
are tailored to that fixture. Its equal boundary distances coexist with
unequal later support counts. A second example is useful only if we can state
precisely what it holds fixed and what its description discards.

This task translates the existing mathematics into a common, inspectable
research contract. It is not a new definition of lushness or a claim of
canonical physical factorization.

## Required inputs

- `docs/current-position.md` and the handoff current-position ledger.
- Formal note 10, particularly sections 2–9 and 11–15.
- P001's specification, complete objects, report and tests.
- Relevant legacy reports before claiming a new result about boundaries,
  intervention transport, or predictive sufficiency.

## Deliverables

1. **A concise continuation contract** in `docs/continuation-contract.md`.
   Identify the full finite realization, initial state, components and scope;
   typed stages and controls; branch maps; physically recorded outcomes;
   conditional/subnormalized weights; reachable residuals; and lawful
   composition. Give a source mapping to note 10 for each field.
2. **An explicit map of information loss.** Show the transformations from full
   realization to a declared response interface, reachable residual family,
   distance matrix and packing profile. State what each preserves and omits.
   Define a valid change of presentation separately from a change of access.
3. **A minimal P001 adapter** that uses the contract without changing the
   fixture or result. Retain record occurrences, controller access and the
   policy-indexed laws. Mark the implementation as a classical diagonal
   realization; do not imply it handles general coherent quantum processes.
4. **A preregistered P002 specification, if warranted.** Name the matched
   stage-indexed summaries, the allowed difference, and a possible falsifier.
   Implementing or searching P002 is outside this first task.

## Acceptance criteria

- P001 reproduces its complete object and scientific result under an explicit
  representation correspondence; both the boundary equality and terminal
  support mismatch remain visible.
- A change of coordinate names/order transports all modeled maps and output
  laws. An incompatible stage/control attachment is rejected or reported as
  an unresolved type mismatch, not silently composed.
- Weights remain conditional on an instrument or policy. There is no invented
  prior over control choices, and equivalent future responses do not erase
  distinct recorded occurrences.
- The contract explains where coherence and CP instruments enter in the
  general definition, and which of those requirements the P001 adapter does
  not exercise. Reuse the baseline's exact evidence for the borrowed quantum
  fixture; do not build an unnecessary new quantum simulator.
- Tests address concrete loss/composition risks. No preference for persistence,
  generativity, controllability or moral desirability is inserted.
- End with either a coherent P002 specification or a precise reason that the
  proposed comparison would be redundant or ill-posed.

## Boundaries and stopping rule

Keep this to one contract and one existing adapter. A general-purpose framework,
new dependency stack, open-ended enumeration or a scalar objective is outside
scope. Stop when the adapter and loss map are clear enough to assess the next
question, including if that assessment rejects the proposed P002 direction.

The unresolved bridge from continuation structure to value-capable
differentiation must remain explicit in the result.
