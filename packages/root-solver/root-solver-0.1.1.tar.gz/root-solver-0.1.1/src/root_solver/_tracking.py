"""
Contains the framework for tracking roots as the equation changes
"""
from abc import ABC, abstractmethod
from numpy import isreal, argmin, float64


def get_closest_root(target, roots):
    """
    Find the closest root to a specific value. Supports complex numbers.
    """
    diff = target - roots
    norm = diff * diff.conj()
    return roots[argmin(norm)]


class RootTracker(ABC):
    """
    Track a given root of a changing polynomial equation
    """
    def __init__(self, *, start_root, is_real=True, dtype=float64, **kwargs):
        self._start_root = start_root
        self._is_real = is_real
        self._dtype = dtype
        self._finalise(**kwargs)

    def _finalise(self, **kwargs):
        """
        finalise options needed for subclasses
        """
        pass

    def solve_root(self, coef, **kwargs):
        """
        Return the closest root of the polynomial defined by the coefficients
        given in `coef` to `current_root`.
        """
        roots = self._solve_root(coef, **kwargs)
        subset_roots = isreal(roots) if self._is_real else slice(None)
        self._start_root = get_closest_root(
            self._start_root, roots[subset_roots]
        )
        return self._start_root

    @abstractmethod
    def _solve_root(self, coef, **kwargs):
        """
        Hook for subclasses to actually solve roots
        """
        raise NotImplementedError(
            "_solve_root need to be implemented on the subclass"
        )

    @property
    def current_root(self):
        """
        The current root found by the root solver
        """
        return self._start_root
