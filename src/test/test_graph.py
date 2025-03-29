import os
import unittest
from collections import defaultdict

import codyssi.graph as graph


class CycleTest(unittest.TestCase):
    nodes: set[str]
    edges: dict[str, set[tuple[str, int]]]

    def setUp(self) -> None:
        nodes = set[str]()
        edges = defaultdict[str, set[tuple[str, int]]](set)
        with open(
            os.path.join(".", "src", "test", "resources", "graph.txt"), "r"
        ) as f:
            for line in f.readlines():
                start, end, weight = line.split(",")
                nodes |= {start, end}
                edges[start].add((end, int(weight)))
        self.nodes = nodes
        self.edges = edges

    def test_find_cycles_nx(self) -> None:
        lgst = max(graph.find_cycles(self.edges, self.nodes), key=len)
        self.assertEqual(
            set(lgst),
            {
                "UWW",
                "EJY",
                "PPC",
                "GYD",
                "HZI",
                "PRZ",
                "UGO",
                "ONC",
                "FQB",
                "CGW",
                "SLC",
                "KJB",
                "YIC",
                "JOT",
                "RXK",
                "PWA",
                "GKK",
                "PRO",
                "FUE",
                "MTX",
                "EIT",
                "FIF",
                "WFA",
            },
        )
