# Warning/response physical diagnostics

All values below are response-on minus response-off within the same environment.
Whole bits are complete sampled histories; body intervals use non-Markov projected bounds.

| Environment | T | Whole bits | Body interval | Working time | Sheltered time | Endpoint bank energy |
|---|---:|---:|---|---:|---:|---:|
| fast | 16 | 1.200505 | [0.337315, 1.925962] | 0.073251 | 0.209051 | -0.017265 |
| fast | 64 | 2.788836 | [-1.281273, 5.697741] | 0.647672 | 2.140170 | 0.016518 |
| fast | 256 | 8.408367 | [-7.310950, 18.300357] | 4.103155 | 17.223088 | 0.025802 |
| fast | 1024 | 28.908576 | [-32.717035, 59.146492] | 20.399337 | 134.040286 | 0.033631 |
| slow | 16 | 1.171493 | [0.355336, 1.886699] | 0.011598 | 0.026584 | -0.019483 |
| slow | 64 | 2.292874 | [-1.416852, 5.624714] | 0.053236 | 0.392169 | 0.000369 |
| slow | 256 | 6.600288 | [-7.980244, 18.561580] | 1.460797 | 6.501152 | 0.013574 |
| slow | 1024 | 26.082982 | [-33.404743, 62.842042] | 14.304695 | 92.989433 | 0.029288 |
| blocked | 16 | 1.168185 | [0.361334, 1.862996] | 0.002837 | 0.000000 | -0.019735 |
| blocked | 64 | 2.196590 | [-1.411999, 5.556425] | -0.071989 | 0.000000 | -0.003416 |
| blocked | 256 | 5.451339 | [-8.271586, 18.570104] | -0.176661 | 0.000000 | -0.001420 |
| blocked | 1024 | 18.454009 | [-35.536122, 70.434960] | -0.484951 | 0.000000 | -0.001419 |
| open | 16 | 1.575325 | [0.401744, 1.845356] | 0.454011 | 1.241045 | 0.003313 |
| open | 64 | 4.694757 | [-0.383905, 5.971903] | 2.455632 | 7.272227 | 0.049904 |
| open | 256 | 11.915995 | [-5.483558, 17.740965] | 7.922164 | 35.954059 | 0.032609 |
| open | 1024 | 31.555919 | [-30.155171, 52.615412] | 23.319106 | 177.500276 | 0.028833 |

## Stationary tracking diagnostic

Mutual information of the bit and contemporaneous exposed hazard; bits. This does not establish the formal future-breadth T test.

| Law | Signal/exposure MI |
|---|---:|
| blocked_R0 | 0.000000018 |
| blocked_RX | 0.000000011 |
| blocked_T0 | 0.000054584 |
| blocked_TX | 0.000043455 |
| fast_R0 | 0.000125326 |
| fast_RX | 0.000134494 |
| fast_T0 | 0.000427022 |
| fast_TX | 0.000506912 |
| slow_R0 | 0.000135957 |
| slow_RX | 0.000147052 |
| slow_T0 | 0.000431252 |
| slow_TX | 0.000513847 |
| open_R0 | 0.000085133 |
| open_RX | 0.000090925 |
| open_T0 | 0.000415007 |
| open_TX | 0.000410706 |

## Signal-response interaction

(TX-T0)-(RX-R0): change in response value with exposure-linked rather than independent writing/resetting. Two physical moments are matched, not full paths or realized costs.

| Environment | T | dt0.125 | dt0.25 | dt0.5 |
|---|---:|---:|---:|---:|
| blocked | 16 | -0.071573 | -0.057662 | -0.041769 |
| blocked | 64 | -0.314836 | -0.268436 | -0.216813 |
| blocked | 256 | -0.631851 | -0.540388 | -0.435437 |
| blocked | 1024 | -1.834089 | -1.566102 | -1.251330 |
| fast | 16 | -0.055053 | -0.047377 | -0.038042 |
| fast | 64 | -0.569173 | -0.500632 | -0.428651 |
| fast | 256 | -0.578052 | -0.572776 | -0.571691 |
| fast | 1024 | 3.848881 | 2.710628 | 1.466847 |
| open | 16 | -0.062111 | -0.068686 | -0.073682 |
| open | 64 | -0.983328 | -0.894309 | -0.804841 |
| open | 256 | 0.716938 | 0.434672 | 0.129051 |
| open | 1024 | 7.696407 | 5.704888 | 3.570736 |
| slow | 16 | -0.067941 | -0.055108 | -0.040345 |
| slow | 64 | -0.349326 | -0.300809 | -0.247368 |
| slow | 256 | -0.697048 | -0.629274 | -0.554161 |
| slow | 1024 | 2.020169 | 1.299235 | 0.525052 |

Whole-history cadence flips on the sampled grid: 11; horizon-flip groups: 23.
No claim of no crossing between sampled points, physical faithfulness or subjective suffering follows.
Same-root mechanism contrasts can differ in limiting rate. A stationary rate is not a finite-horizon verdict.
The body can recover through native routes; no permanent death or structural channel closure is present.
