[![Documentation Status](https://readthedocs.org/projects/root-solver/badge/?version=latest)](https://root-solver.readthedocs.org/en/latest/?badge=latest)
[![Build Status](https://travis-ci.org/root-solver/root-solver.svg?branch=master)](https://travis-ci.org/root-solver/root-solver)
[![Coverage Status](https://codecov.io/github/aragilar/root-solver/coverage.svg?branch=master)](https://codecov.io/github/aragilar/root-solver?branch=master)
[![Version](https://img.shields.io/pypi/v/root-solver.svg)](https://pypi.python.org/pypi/root-solver/)
[![License](https://img.shields.io/pypi/l/root-solver.svg)](https://pypi.python.org/pypi/root-solver/)
[![Wheel](https://img.shields.io/pypi/wheel/root-solver.svg)](https://pypi.python.org/pypi/root-solver/)
[![Format](https://img.shields.io/pypi/format/root-solver.svg)](https://pypi.python.org/pypi/root-solver/)
[![Supported versions](https://img.shields.io/pypi/pyversions/root-solver.svg)](https://pypi.python.org/pypi/root-solver/)
[![Supported implementations](https://img.shields.io/pypi/implementation/root-solver.svg)](https://pypi.python.org/pypi/root-solver/)
[![PyPI](https://img.shields.io/pypi/status/root-solver.svg)](https://pypi.python.org/pypi/root-solver/)

root-solver provides solvers for polynomials of orders 2 and 3 (with plans for 4
and possibly higher), using the algorithms of Kahan and others. See
http://www.cs.berkeley.edu/~wkahan/Math128/Cubic.pdf for more information about
the algorithms included.

Additionally root-solver includes support for tracking a single root as the
coefficients of the polynomial changes.

Bug reports and suggestions should be filed at
[https://github.com/aragilar/root-solver/issues](https://github.com/aragilar/root-solver/issues).

# Installing root-solver
root-solver is distributed via [PyPI](https://pypi.org/project/root-solver/), and
can be [installed via pip](https://packaging.python.org/tutorials/installing-packages/) with:
```
pip install root-solver
```

To install a development version of root-solver, clone this repository and use:
```
pip install -e .
```
