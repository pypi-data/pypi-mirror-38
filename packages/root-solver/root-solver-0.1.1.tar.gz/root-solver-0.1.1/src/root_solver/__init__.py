"""
root-solver provides solvers for polynomials of orders 2 and 3, using the
algorithms of Kahan and others. See
http://www.cs.berkeley.edu/~wkahan/Math128/Cubic.pdf for more information about
the algorithms included.

Additionally root-solver includes support for tracking a single root as the
coefficients of the polynomial changes.
"""

from ._cubic import solve_cubic, CubicTracker
from ._quadratic import solve_quadratic

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions

__all__ = [
    "__version__",
    "solve_cubic",
    "solve_quadratic",
    "CubicTracker",
]
