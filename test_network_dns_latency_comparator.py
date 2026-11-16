import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import unittest
from main import compare

def row(resolver, query, latency):
    return {"resolver": resolver, "query": query, "latency_ms": str(latency)}

class TestDnsLatencyComparator(unittest.TestCase):
    def test_average_computed(self):
        r = compare([row("8.8.8.8", "example.com", 22),
                     row("8.8.8.8", "example.org", 25),
                     row("8.8.8.8", "example.net", 21)])
        self.assertEqual(r[0][2], 22.7)

    def test_fastest_first(self):
        r = compare([row("9.9.9.9", "example.com", 45),
                     row("1.1.1.1", "example.com", 18),
                     row("8.8.8.8", "example.com", 22)])
        self.assertEqual([x[0] for x in r], ["1.1.1.1", "8.8.8.8", "9.9.9.9"])

    def test_p95_single_sample(self):
        r = compare([row("1.1.1.1", "example.com", 18)])
        self.assertEqual(r[0][3], 18.0)

    def test_p95_of_twenty_samples(self):
        rows = [row("1.1.1.1", "example.com", n) for n in range(1, 21)]
        self.assertEqual(compare(rows)[0][3], 19.0)

    def test_sample_count(self):
        r = compare([row("1.1.1.1", "a", 18), row("1.1.1.1", "b", 19)])
        self.assertEqual(r[0][1], 2)

    def test_tie_broken_by_resolver_name(self):
        r = compare([row("8.8.8.8", "a", 20), row("1.1.1.1", "a", 20)])
        self.assertEqual(r[0][0], "1.1.1.1")

    def test_decimal_latencies(self):
        r = compare([row("1.1.1.1", "a", 18.5), row("1.1.1.1", "b", 19.5)])
        self.assertEqual(r[0][2], 19.0)

    def test_empty_input(self):
        self.assertEqual(compare([]), [])
