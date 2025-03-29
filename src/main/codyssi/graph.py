import sys
from collections import defaultdict
from queue import PriorityQueue
from typing import Callable
from typing import Iterator
from typing import TypeVar

T = TypeVar("T")


def dijkstra(
    start: T,
    is_end: Callable[[T], bool],
    adjacent: Callable[[T], Iterator[T]],
    get_cost: Callable[[T, T], int],
) -> tuple[int, dict[T, int], list[T]]:
    q: PriorityQueue[tuple[int, T]] = PriorityQueue()
    q.put((0, start))
    best: defaultdict[T, int] = defaultdict(lambda: sys.maxsize)
    best[start] = 0
    parent: dict[T, T] = {}
    path = []
    while not q.empty():
        cost, node = q.get()
        if is_end(node):
            path = [node]
            curr = node
            while curr in parent:
                curr = parent[curr]
                path.append(curr)
            break
        best_cost = best[node]
        for n in adjacent(node):
            new_cost = best_cost + get_cost(node, n)
            if new_cost < best[n]:
                best[n] = new_cost
                parent[n] = node
                q.put((new_cost, n))
    return cost, best, path


def find_cycles(
    edges: dict[str, set[tuple[str, int]]], nodes: set[str]
) -> Iterator[list[str]]:
    def dfs(path: list[str]) -> Iterator[list[str]]:
        nn: set[tuple[str, int]] = edges.get(path[-1], set())
        for n, _ in nn:
            try:
                i = path.index(n)
                yield path[i:]
            except ValueError:
                yield from dfs(path[:] + [n])

    seen = set[tuple[str]]()
    for node in nodes:
        for c in dfs([node]):
            s = tuple(_ for _ in sorted(c))
            if s not in seen:
                seen.add(s)
                yield c
