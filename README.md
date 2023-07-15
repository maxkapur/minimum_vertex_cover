# Minimum-weight vertex cover

A minimum-weight vertex cover solver using the [OR-Tools modeling language](https://developers.google.com/optimization) and [SCIP backend](https://www.scipopt.org/) for integer linear programming.

Integer programming is *not* the most efficient way to solve the minimum-weight vertex cover problem. Instead, the purpose of this repository is to demonstrate a “Hello, World!”-type program in the OR-Tools language, and to explore using GitHub actions to compare problem compilation times for problem sizes.

If OR-Tools ever [supports PyPy](https://github.com/google/or-tools/issues/1346), I would also like to compare the performance PyPy and Cython for this script. Since the SCIP solver is written in C, using PyPy will not improve the *solution* times, but for graphical problems like vertex cover, the time to *compile* linear programs is often nontrivial, and PyPy could be helpful for large instances.

## Requirements and installation

Requires Python v3.11 or better because I used a `match` statement (sorry).

You might install and set up a virtual environment for this script as follows (example uses Debian and the fish shell):

```bash
# Clone this repo
$ git clone "https://github.com/maxkapur/minimum_vertex_cover.git"
# Change into the cloned directory
$ cd minimum_vertex_cover
# Create a virtual environment for this script
$ python3 -m venv "./venv"
# Activate it (use tab completion to select the right activate
# script for your platform)
$ source "./venv/bin/activate.fish"
# Make sure it activated correctly
$ which python
THIS_DIRECTORY/venv/bin/python
# Install dependencies
$ python -m pip install -r requirements.txt
```

## Usage

The file `main.py` accepts command-line arguments to define the density and size of the graph. For example, in the following run, the graph contains `10` nodes, and each arc is constructed with probability `0.3`. The arc weights are drawn from a standard exponential distribution; we can see that those that appear in the optimal solution have small weights:

```bash
$ python main.py 0.3 10
Generating decision variables ... done.
Generating vertex cover constraints ... done.
Generating objective function ... done.
Solving problem using backend SCIP.
Optimal solution found.
Double-checking that every arc is covered ... done.
Solution has weight 3.355 and consists of the following 7 nodes:
[0, 1, 2, 4, 5, 6, 7]
Problem size:               10 nodes, 28 arcs
Problem compilation time:   0.004 seconds
Problem solution time:      0.007 seconds
```

## References

For more information about the minimum-weight vertex cover problem, see [Chandra Chekuri’s course notes](https://courses.engr.illinois.edu/cs583/sp2018/Notes/covering.pdf) (especially §4) or [Wikipedia](https://en.wikipedia.org/wiki/Vertex_cover).

## Author

By [Max Kapur](https://maxkapur.com).
