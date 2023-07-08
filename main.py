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

    # Hashable
    @property
    def index(self) -> tuple[int, int]:
        return (self.a, self.b)


class MinimumVertexCoverProblem:
    "An instance of the minimum-weight vertex cover problem."

    SOLVER_NAME = "SCIP"
    SOLVER_SHOW_OUTPUT = True

    def __init__(self, arcs: list[Arc]) -> None:
        self.arcs = arcs

        self.nodes: set[int] = set()

        for arc in arcs:
            self.nodes.add(arc.a)
            self.nodes.add(arc.b)

        self.milp_solver: pywraplp.Solver = pywraplp.Solver.CreateSolver(self.SOLVER_NAME)

        self.x: dict[tuple[int, int], pywraplp.BoolVar] = dict()

        for arc in self.arcs:
            self.x[arc.index] = self.milp_solver.BoolVar(f"x[{arc.a},{arc.b}]")
        for node in self.nodes:
            self.milp_solver.Add(
                sum(self.x[arc.index] for arc in self.arcs if arc.a == node or arc.b == node) >= 1,
                f"Must select at least one arc that covers node {node}"
            )

        self.milp_solver.Minimize(sum(map(lambda arc: arc.w * self.x[arc.index], self.arcs)))

        if self.SOLVER_SHOW_OUTPUT:
            self.milp_solver.EnableOutput()
        else:
            self.milp_solver.SuppressOutput()

        self.milp_solver.Solve()


def randexp():
    "A random draw from the standard exponential distribution."
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

    problem = MinimumVertexCoverProblem(arcs)
