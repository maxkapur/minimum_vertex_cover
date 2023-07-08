# Minimum-weight vertex cover

A minimum-weight vertex cover solver using the [OR-Tools modeling language](https://developers.google.com/optimization) and [SCIP backend](https://www.scipopt.org/) for integer linear programming.

Integer programming is *not* the most efficient way to solve the minimum-weight vertex cover problem. Instead, the purpose of this repository is to demonstrate a “Hello, World!”-type program in the OR-Tools language, and to explore using GitHub actions to compare problem compilation times for problem sizes.

If OR-Tools ever [supports PyPy](https://github.com/google/or-tools/issues/1346), I would also like to compare the performance PyPy and Cython for this script. Since the SCIP solver is written in C, using PyPy will not improve the *solution* times, but for graphical problems like vertex cover, the time to *compile* linear programs is often nontrivial, and PyPy could be helpful for large instances.

## Requirements and installation

Requires Python v3.11 or better because I used a `match` statement (sorry).

You might install and set up a virtual environment for this script as follows (Debian):

```bash
# Clone this repo
$ git clone "https://github.com/maxkapur/minimum_vertex_cover.git"
# Change into the cloned directory
$ cd minimum_vertex_cover
# Create a virtual environment in your home directory
$ python3 -m venv ~/python-venvs/minimum-vertex-cover
# Activate it
$ source ~/python-venvs/minimum-vertex-cover/bin/activate
# Make sure it activated correctly
$ which python
YOUR_HOME_DIRECTORY/python-venvs/minimum-vertex-cover/bin/python
# Install dependencies
$ python -m pip install -r requirements.txt
```

## Usage

The file `main.py` accepts command-line arguments to define the density and size of the graph. For example, in the following run, the graph contains `10` nodes, and each arc is constructed with probability `0.3`. The arc weights are drawn from a standard exponential distribution; we can see that those that appear in the optimal solution have small weights:

```bash
$ python main.py 0.3 10
Solution consists of the following 6 arcs:
  Arc between nodes 1 and 2 with weight 0.0773
  Arc between nodes 3 and 0 with weight 0.3714
  Arc between nodes 4 and 7 with weight 0.0021
  Arc between nodes 5 and 7 with weight 0.3101
  Arc between nodes 6 and 3 with weight 0.0771
  Arc between nodes 8 and 9 with weight 0.0058
Problem size:               10 nodes, 35 arcs
Problem compilation time:   0.004 seconds
Problem solution time:      0.005 seconds
```

## Author

By [Max Kapur](https://maxkapur.com).
