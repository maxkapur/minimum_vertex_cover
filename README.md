# Minimum-weight vertex cover

A minimum-weight vertex cover solver using the [SCIP Optimization Suite](https://www.scipopt.org/) for integer linear programming.

Integer programming is *not* the most efficient way to solve the minimum-weight vertex cover problem. Instead, the purpose of this repository is to demonstrate a “Hello, World!”-type program using SCIP’s toolset, and to explore using GitHub actions to compare problem compilation times for problem sizes.

## Requirements and installation

Requires Python v3.10 or better because I used a `match` statement (sorry). Also requires a conda environment ([Miniconda](https://docs.conda.io/en/latest/miniconda.html) is sufficient) in order to `conda install` pyscipopt along with its binary dependencies.

Assuming you have conda and git installed, you might install and set up a virtual environment for this script as follows (example uses Debian and the bash shell):

```bash
# Clone this repo
$ git clone "https://github.com/maxkapur/minimum_vertex_cover.git"
# Change into the cloned directory
$ cd ./minimum_vertex_cover
# Create a virtual environment for this script
$ conda create -p ./venv
# Activate it
$ conda activate "$(pwd)/venv"
# Make sure it activated correctly
$ conda info         
    active environment : THIS_DIRECTORY/venv
# Add conda-forge channel (required to install pyscipopt)
$ conda config --add channels conda-forge
# Install dependencies
$ conda install --file ./requirements.txt
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
