# network-dns-latency-comparator

Compare DNS resolver latency from a CSV of latency samples: each resolver gets its sample count, average latency and p95 latency (the value at the 95th percentile of its sorted samples) — fastest first by average latency, with the fastest resolver named.

Sample input is included (sample.csv with nine latency samples).

## How to run

```sh
python3 main.py sample.csv
```

## Example output

```
1.1.1.1: 3 sample(s), average 18.0 ms, p95 19 ms
8.8.8.8: 3 sample(s), average 22.7 ms, p95 25 ms
9.9.9.9: 3 sample(s), average 47.7 ms, p95 50 ms
Fastest resolver: 1.1.1.1 (18.0 ms average).
```

Standard library only. Run the tests with `python3 -m unittest discover`.
