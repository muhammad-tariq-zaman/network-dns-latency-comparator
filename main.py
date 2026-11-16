"""Compare DNS resolver latency from a samples CSV.

Usage: python3 main.py samples.csv
CSV columns: resolver,query,latency_ms.
Latency samples are grouped by resolver; each resolver gets its
sample count, average latency and p95 latency (the value at the
95th percentile of its sorted samples). Resolvers are listed
fastest first by average latency, and the fastest one is named.
"""
import argparse, csv, math, sys

def compare(rows):
    grouped = {}
    for row in rows:
        resolver = row["resolver"].strip()
        grouped.setdefault(resolver, []).append(float(row["latency_ms"]))
    out = []
    for resolver, samples in grouped.items():
        samples = sorted(samples)
        average = round(sum(samples) / len(samples), 1)
        index = max(0, math.ceil(0.95 * len(samples)) - 1)
        p95 = samples[index]
        out.append((resolver, len(samples), average, p95))
    return sorted(out, key=lambda r: (r[2], r[0]))

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path")
    args = parser.parse_args(argv)
    with open(args.path, newline="", encoding="utf-8") as f:
        results = compare(list(csv.DictReader(f)))
    for resolver, count, average, p95 in results:
        print(f"{resolver}: {count} sample(s), average {average:.1f} ms, p95 {p95:g} ms")
    if results:
        print(f"Fastest resolver: {results[0][0]} ({results[0][2]:.1f} ms average).")
    return 0

if __name__ == "__main__":
    sys.exit(main())
