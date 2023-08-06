"""
Contains all the logic for solving quadratics
"""

from numpy import (
    array, sqrt, sign, abs as np_abs, power as np_pow, around as np_round,
)

from ._utils import get_nearest_radix


def _disc(a, b, c):
    """
    Python implementation of DISC
    """
    if a * c > 0:
        a = np_abs(a)
        c = np_abs(c)
        loop_cont = True  # loop must run at least once
        while loop_cont:
            loop_cont = False
            if a < c:
                a, c = c, a
            n = np_round(b / c)
            if n != 0:
                α = a - n * b
                if α >= - a:
                    b = b - n * c
                    a = α - n * b
                    if a > 0:
                        loop_cont = True
    return np_pow(b, 2) - a * c


def solve_quadratic(A, B, C):
    """
    Solves the quadratic A x^2 + B x + C.

    Python implementation of QDRTC
    """
    if A != 0 and C != 0:
        σ = get_nearest_radix(sqrt(np_abs(A)) * sqrt(np_abs(C)))
        if np_abs(B) == np_abs(B) + σ:
            return array([- C / B, - B / A])
        A = A / σ
        B = B / σ
        C = C / σ

    b = - B / 2
    q = _disc(A, b, C)

    if q < 0:
        X = b / A
        Y = sqrt(- q) / A
        return array([
            X + 1j * Y,
            X - 1j * Y
        ])

    r = b + sign(b) * sqrt(q)
    if r == 0:
        X = C / A
        return array([X, - X])
    return array([C / r, r / A])
