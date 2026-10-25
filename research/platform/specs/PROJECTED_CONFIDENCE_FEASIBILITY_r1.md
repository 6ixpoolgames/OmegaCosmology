# Projected-history confidence: bounded S1 feasibility

25 October 2026. E1 physics and observed quantity stay unchanged. The target is
the unassembled donor A, AtoB minus local, low supply/bill/turnover, at T16/64/256.
Two cadences .25/.5;8192 independent paired filter paths each, fixed seeds
2026102504/2026102505, batches256. No sign-dependent extension of sampling.
Caps:600s/4GiB per case; two serial cases. Existing full-history comparisons
are independently checked against the matching retained cadence's case.

Use [Maurer and Pontil2009, Theorem4](https://www.cs.mcgill.ca/~colt2009/papers/012.pdf)
on each paired path score. With unbiased sample variance V, fixed sample count
N, proven support width R and error allocation alpha, the two-sided radius is
`sqrt(2 V log(4/alpha)/N) + 7 R log(4/alpha)/(3(N-1))`.
Apply the one-sided theorem to X and -X with alpha/2 each. Allocate .05/6 to each
of the six cadence/horizon comparisons. This family is specified before this
feasibility run; earlier studies are exploratory context, not part of its
simultaneous coverage.

With n steps and M observed states, the raw path entropy reward lies in
[0,n log2 M]. Subtracting a memory1 control with its exact mean gives a paired
score of support width4n log2 M (the deterministic mean shifts the interval but
not its width). Use this theoretical width, never the observed sample range.
The control preserves the target mean; it does not delete physical randomness.

This improves the finite-sample statistical treatment but leaves float64
evaluation and pseudorandom sampling assumptions explicit. It is NOT a rigorous
numerical entropy certificate. If bounds remain too broad, report their width
and the support-term sample requirement; do not keep sampling until a sign
appears. Approximate t and older Hoeffding intervals remain separately typed.
Observation-tree expansion and interval-arithmetic filtering are alternative
future methods, not asserted implementations in this sprint.
