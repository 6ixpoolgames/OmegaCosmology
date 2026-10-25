# Warning/response physical diagnostics

All values below are response-on minus response-off within the same environment.
Whole bits are complete sampled histories; body intervals use non-Markov projected bounds.

| Environment | T | Whole bits | Body interval | Working time | Sheltered time | Endpoint bank energy |
|---|---:|---:|---|---:|---:|---:|
| fast | 16 | 0.880157 | [0.299333, 1.380915] | 0.050805 | 0.149680 | -0.018601 |
| fast | 64 | 1.708072 | [-0.978099, 3.651623] | 0.500027 | 1.577242 | 0.012733 |
| fast | 256 | 4.105255 | [-5.192121, 10.352861] | 3.244742 | 10.237577 | 0.019935 |
| fast | 1024 | 9.701432 | [-24.466923, 31.017093] | 13.823442 | 62.236036 | 0.021112 |
| slow | 16 | 0.896981 | [0.350504, 1.381880] | 0.007827 | 0.019249 | -0.021926 |
| slow | 64 | 1.571266 | [-0.870581, 3.770546] | -0.001627 | 0.285450 | -0.003597 |
| slow | 256 | 3.392648 | [-5.185656, 10.766469] | 0.848672 | 3.310293 | 0.008561 |
| slow | 1024 | 9.862240 | [-23.084749, 34.249657] | 8.647917 | 38.891390 | 0.017790 |
| blocked | 16 | 0.899884 | [0.361683, 1.366477] | 0.001680 | 0.000000 | -0.022383 |
| blocked | 64 | 1.548818 | [-0.815411, 3.742703] | -0.105436 | 0.000000 | -0.007443 |
| blocked | 256 | 3.098673 | [-5.042840, 10.893428] | -0.272807 | 0.000000 | -0.001690 |
| blocked | 1024 | 9.492281 | [-21.240343, 39.209448] | -0.611362 | 0.000000 | -0.001666 |
| open | 16 | 0.936040 | [0.161641, 1.137399] | 0.305558 | 0.838936 | 0.003133 |
| open | 64 | 2.572554 | [-0.734524, 3.479795] | 1.920042 | 5.005999 | 0.045777 |
| open | 256 | 5.938334 | [-4.347726, 9.957416] | 6.469701 | 21.110275 | 0.024935 |
| open | 1024 | 10.163679 | [-24.160414, 26.977195] | 16.293699 | 84.441124 | 0.018190 |

## Stationary tracking diagnostic

Mutual information of the bit and contemporaneous exposed hazard; bits. This does not establish the formal future-breadth T test.

| Law | Signal/exposure MI |
|---|---:|
| blocked_R0 | 0.000000447 |
| blocked_RX | 0.000000300 |
| blocked_T0 | 0.000016246 |
| blocked_TX | 0.000014755 |
| fast_R0 | 0.000837984 |
| fast_RX | 0.000806131 |
| fast_T0 | 0.000020374 |
| fast_TX | 0.000056976 |
| slow_R0 | 0.000876676 |
| slow_RX | 0.000866620 |
| slow_T0 | 0.000021714 |
| slow_TX | 0.000059100 |
| open_R0 | 0.000657282 |
| open_RX | 0.000607303 |
| open_T0 | 0.000010591 |
| open_TX | 0.000048377 |

## Signal-response interaction

(TX-T0)-(RX-R0): change in response value with exposure-linked rather than independent writing/resetting. Two physical moments are matched, not full paths or realized costs.

| Environment | T | dt0.125 | dt0.25 | dt0.5 |
|---|---:|---:|---:|---:|
| blocked | 16 | 0.054336 | 0.045487 | 0.036913 |
| blocked | 64 | -0.023928 | -0.018919 | -0.012554 |
| blocked | 256 | -0.124733 | -0.104090 | -0.080700 |
| blocked | 1024 | -0.500677 | -0.417553 | -0.325914 |
| fast | 16 | 0.026007 | 0.021504 | 0.017683 |
| fast | 64 | -0.579156 | -0.493304 | -0.404297 |
| fast | 256 | -2.440634 | -2.083733 | -1.716384 |
| fast | 1024 | -9.086210 | -7.774919 | -6.416832 |
| open | 16 | -0.094300 | -0.078223 | -0.058690 |
| open | 64 | -1.529148 | -1.305712 | -1.072873 |
| open | 256 | -3.604382 | -3.081997 | -2.538480 |
| open | 1024 | -10.371037 | -8.926551 | -7.410144 |
| slow | 16 | 0.051536 | 0.043090 | 0.034958 |
| slow | 64 | -0.122021 | -0.102882 | -0.082116 |
| slow | 256 | -0.921590 | -0.787142 | -0.647279 |
| slow | 1024 | -5.930844 | -5.081791 | -4.198373 |

Whole-history cadence flips on the sampled grid: 0; horizon-flip groups: 24.
No claim of no crossing between sampled points, physical faithfulness or subjective suffering follows.
Same-root mechanism contrasts can differ in limiting rate. A stationary rate is not a finite-horizon verdict.
The body can recover through native routes; no permanent death or structural channel closure is present.
