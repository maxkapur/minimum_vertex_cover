from ortools.linear_solver import pywraplp
import dataclasses
import itertools
import random
import math


@dataclasses.dataclass
class Arc:
    "An undirected arc between nodes `a` and `b` with weight `w`."
    a: int
    b: int
    w: float


class MinimumVertexCoverProblem:
    "An instance of the minimum vertex cover problem."

    def __init__(self, arcs: list[Arc]) -> None:
        self.arcs = arcs


def randexp():
    "Random draw from the standard exponential distribution."
    return -math.log(random.random())


if __name__ == "__main__":
    import sys

    density = 0.50
    if len(sys.argv) > 1:
        density = float(sys.argv[1])

    n_nodes = 20
    if len(sys.argv) > 2:
        n_nodes = int(sys.argv[2])

    nodes = range(n_nodes)

    arcs = [
        Arc(a, b, randexp())
        for a, b in itertools.product(nodes, repeat=2)
        if random.random() < density
    ]

    print(arcs)