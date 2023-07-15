import dataclasses
import itertools
import math
import random
import time
import warnings

from ortools.linear_solver import pywraplp


@dataclasses.dataclass
class Arc:
    "An undirected arc between nodes `a` and `b` with weight `w`."
    a: int
    b: int

    def __repr__(self) -> str:
        return f"Arc between nodes {self.a} and {self.b}"

    # Hashable
    @property
    def index(self) -> tuple[int, int]:
        return (self.a, self.b)


class MinimumVertexCoverProblem:
    "An instance of the minimum-weight vertex cover problem."

    # Which backend to use, e.g. "SCIP" or "Cbc"
    SOLVER_NAME = "SCIP"
    # Whether to show the solver's native output
    SOLVER_SHOW_OUTPUT = False
    # Time limit on solution time in seconds
    SOLVER_TIME_LIMIT = 300

    def __init__(self, arcs: list[Arc]) -> None:
        self.arcs = arcs
        self.arcs.sort(key=lambda arc: arc.index)

        self.collect_nodes()
        self.initialize_solver()
        self.generate_decision_variables()
        self.generate_constraints()
        self.generate_objective_function()

        # Let the user call this (potentially expensive function)
        # self.solve_problem()

    def collect_nodes(self) -> None:
        self.nodes: set[int] = set()
        for arc in self.arcs:
            self.nodes.add(arc.a)
            self.nodes.add(arc.b)

    def initialize_solver(self) -> None:
        "Initialize the MILP solver."
        self.milp_solver: pywraplp.Solver = pywraplp.Solver.CreateSolver(self.SOLVER_NAME)
        # .SetTimeLimit appears to use milliseconds
        self.milp_solver.SetTimeLimit(self.SOLVER_TIME_LIMIT * 1000)

    def generate_decision_variables(self) -> None:
        """
        Generate boolean variables representing whether each node is included 
        in the optimal solution.
        """
        self.x: dict[int, pywraplp.BoolVar] = dict()
        for node in self.nodes:
            self.x[node] = self.milp_solver.BoolVar(f"x[{node}]")

    def generate_constraints(self) -> None:
        "Generate the vertex cover constraints for each node."
        for arc in self.arcs:
            self.milp_solver.Add(
                self.x[arc.a] + self.x[arc.b] >= 1,
                f"Must select at least one endpoint of {arc}"
            )

    def generate_objective_function(self) -> None:
        """
        Construct the objective function, namely to minimize the sum of the weights
        of the selected nodes.
        """
        self.milp_solver.Minimize(sum(self.x.values()))

    def solve_problem(self) -> None:
        "Solve the MILP using the backend defined in `self.SOLVER_NAME`."
        if self.SOLVER_SHOW_OUTPUT:
            self.milp_solver.EnableOutput()
        else:
            self.milp_solver.SuppressOutput()

        status = self.milp_solver.Solve()
        match status:
            case pywraplp.Solver.OPTIMAL:
                self.validate_solution()
                self.display_solution()
            case pywraplp.Solver.FEASIBLE:
                warnings.warn("Solver timed out on a feasible, but potentially suboptimal solution")
                self.validate_solution()
                self.display_solution()
            case pywraplp.Solver.INFEASIBLE:
                # How did we get here? Since we pulled the nodes from the arcs,
                # a vertex cover should always exist
                print("Problem is infeasible: No vertex covers exist")
            case pywraplp.Solver.UNBOUNDED:
                # How did we get here? All decision variables are bounded,
                # so the objective value should be finite as long as the vertex
                # weights are
                print("Problem is unbounded; are all vertex weights finite?")
            case _:
                print(f"Solver failed to converge within {self.SOLVER_TIME_LIMIT = }")

    def is_node_included(self, node: int) -> bool:
        """
        Return `True` if the decision variable corresponding to this node has 
        an  objective value of 1, `False` if 0.
        """
        # Compare to 0.5 since solver will report convergence even if
        # x[a, b] == 0.999
        return self.x[node].SolutionValue() > 0.5

    def is_arc_covered(self, arc: Arc) -> bool:
        "Return True if one of both of the endpoints of this arc is covered."
        match (self.is_node_included(arc.a), self.is_node_included(arc.b)):
            case (True, False):
                print(f"  {arc} is covered (left endpoint)")
                return True
            case (False, True):
                print(f"  {arc} is covered (right endpoint)")
                return True
            case (True, True):
                print(f"  {arc} is covered (both endpoints)")
                return True
            case (True, True):
                print(f"  {arc} is not covered!")
                return False

    def validate_solution(self) -> None:
        "Double check that the current solution is a vertex cover."
        assert all(map(self.is_arc_covered, self.arcs))

    def display_solution(self) -> None:
        "Summarize the current solution."
        nodes = list(filter(self.is_node_included, self.nodes))
        print(f"Solution consists of the following {len(nodes)} nodes:")
        print(nodes)


def randexp():
    "A random draw from the standard exponential distribution."
    return -math.log(random.random())


if __name__ == "__main__":
    import sys

    density = 0.80
    if len(sys.argv) > 1:
        density = float(sys.argv[1])

    n_nodes = 20
    if len(sys.argv) > 2:
        n_nodes = int(sys.argv[2])

    nodes = range(n_nodes)

    arcs = [
        Arc(a, b)
        for a, b in itertools.product(nodes, repeat=2)
        if random.random() < density
    ]

    then = time.time()
    problem = MinimumVertexCoverProblem(arcs)
    compilation_time = time.time() - then

    problem.solve_problem()
    solver_time = problem.milp_solver.WallTime() / 1000.0

    print(f"Problem size:               {len(problem.nodes)} nodes, {len(problem.arcs)} arcs")
    print(f"Problem compilation time:   {'%.3f' % compilation_time} seconds")
    print(f"Problem solution time:      {'%.3f' % solver_time} seconds")
