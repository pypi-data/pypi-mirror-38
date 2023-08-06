"""
Contains all the logic for solving cubics (excluding that needed for solving
quadratics)
"""

from numpy import (
    array, sqrt, cbrt, sign, abs as np_abs, float64, power as np_pow, finfo,
    concatenate, inf, around as np_round, isclose, isreal,
)

from ._quadratic import solve_quadratic
from ._tracking import RootTracker
from ._utils import get_shared_figs, check_pairwise

AFTER_1 = 1 + finfo(float64).eps
CUBIC_CONSTANT = 1.324718


def get_quotients_near_triple(A, B, C, D):
    """
    Get the quotients for the case when the roots are almost a triple.
    """
    a = A
    b = - B / 3
    c = C / 3
    d = - D
    if a != 0:
        p = b / a
    else:
        p = inf
    if b != 0:
        q = c / b
    else:
        q = inf
    if c != 0:
        r = d / c
    else:
        r = inf

    return array([p, q, r])


def check_quotients_near_triple(
    A, B, C, D, *, num_calls_triple=0, num_calls_double=0
):
    """
    Handle the case when the roots are almost a triple.
    """
    qs = get_quotients_near_triple(A, B, C, D)
    if not check_pairwise(qs, isclose):
        return False, None
    λ = get_shared_figs(qs)

    a = A
    b = - B / 3
    c = C / 3
    d = - D

    b_dash = b - λ * a
    c_dash = c - λ * b
    d_dash = d - λ * c

    c_ddash = c_dash - λ * b_dash
    d_ddash = d_dash - λ * c_dash

    d_star = d_ddash - λ * c_ddash

    case, roots = solve_cubic(
        a, - 3 * b_dash, 3 * c_ddash, - d_star,
        num_calls_triple=num_calls_triple+1,
        num_calls_double=num_calls_double,
        recurse=(num_calls_triple < 10),
    )
    if case == "0":
        case = "triple"

    return True, (case, roots + λ)


def check_quotients_near_double(
    A, B, C, D, *, num_calls_triple=0, num_calls_double=0
):
    """
    Get the quotients for the case when the roots are almost a double.
    """
    qs = get_quotients_near_double(A, B, C, D)
    pos_case = check_pairwise(qs, isclose)
    neg_case = check_pairwise([qs[0], -qs[1]], isclose)
    if not (pos_case or neg_case):
        return False, None

    if pos_case:
        λ = get_shared_figs(qs)
    elif neg_case:
        λ = get_shared_figs(array([qs[0], -qs[1]]))
    else:
        raise RuntimeError("double quotients check has problem")

    a = A
    b = - B / 3
    c = C / 3
    d = - D

    b_dash = b - λ * a

    c_dash = c - λ * b
    c_ddash = c_dash - λ * b_dash

    if d < a * np_pow(λ, 3):
        D = np_round(d)
        δ = d - D
        d_dash = D - λ * c
        d_ddash = d_dash - λ * c_dash
        d_star = (d_ddash - λ * c_ddash) + δ
    else:
        d_dash = d - λ * c
        d_ddash = d_dash - λ * c_dash
        d_star = d_ddash - λ * c_ddash

    case, roots = solve_cubic(
        a, - 3 * b_dash, 3 * c_ddash, - d_star,
        num_calls_triple=num_calls_triple,
        num_calls_double=num_calls_double+1,
        recurse=(num_calls_double < 10),
    )

    return True, (case, roots + λ)


def get_quotients_near_double(A, B, C, D):
    """
    Handle the case when the roots are almost a double.
    """
    a = A
    b = - B / 3
    c = C / 3
    d = - D

    p = (b * c - a * d) / (np_pow(b, 2) - a * c) / 2
    q = sqrt((np_pow(c, 2) - b * d) / (np_pow(b, 2) - a * c))

    return array([p, q])


def _eval(X, A, B, C, D):
    """
    Python implementation of EVAL
    """
    q0 = A * X
    B1 = q0 + B
    C2 = B1 * X + C
    Q_dash = (q0 + B1) * X + C2
    Q = C2 * X + D
    return Q, Q_dash, B1, C2


def _fin(X, A, b1, c2):
    """
    Python implementation of `fin`
    """
    return concatenate([[X], solve_quadratic(A, b1, c2)])


def _iter(x0, A, B, C, D, after_1=AFTER_1):
    """
    The body of the iteration to find the first root
    """
    X = x0
    q, q_dash, b1, c2 = _eval(X, A, B, C, D)

    if q_dash == 0:
        x0 = X
    else:
        x0 = X - (q / q_dash) / after_1
    return X, x0, b1, c2


def solve_cubic(
    A, B, C, D, *, num_calls_triple=0, num_calls_double=0, recurse=True,
    after_1=AFTER_1
):
    """
    Solves the quadratic A x^3 + B x^2 + C x + D.

    Python implementation of QBC
    """
    # pylint: disable=too-many-branches
    if isreal(A):
        A = A.real
    if isreal(B):
        B = B.real
    if isreal(C):
        C = C.real
    if isreal(D):
        D = D.real

    if A == 0:
        return "quad", _fin(inf, A, B, C)
    if D == 0:
        return "0", _fin(0, A, B, C)

    if recurse:
        is_near_triple, ret_vals = check_quotients_near_triple(
            A, B, C, D, num_calls_triple=num_calls_triple,
            num_calls_double=num_calls_double,
        )
        if is_near_triple:
            return ret_vals

        is_near_double, ret_vals = check_quotients_near_double(
            A, B, C, D, num_calls_triple=num_calls_triple,
            num_calls_double=num_calls_double,
        )
        if is_near_double:
            return ret_vals

    X = - (B / A) / 3
    q, q_dash, b1, c2 = _eval(X, A, B, C, D)

    t = q / A
    r = cbrt(np_abs(t))
    s = sign(t)

    t = - q_dash / A
    if t > 0:
        r = CUBIC_CONSTANT * max([r, sqrt(t)])
    x0 = X - s * r
    if x0 == X:
        return "no iter", _fin(X, A, b1, c2)

    X, x0, b1, c2 = _iter(x0, A, B, C, D, after_1=after_1)

    while s * x0 > s * X:
        X, x0, b1, c2 = _iter(x0, A, B, C, D, after_1=after_1)

    if np_abs(A) * np_pow(X, 2) > np_abs(D * X):
        c2 = - D / X
        b1 = (c2 - C) / X

    return "iter", _fin(X, A, b1, c2)


class CubicTracker(RootTracker):
    """
    Track a given root of a changing cubic equation
    """
    def _finalise(self, **kwargs):
        self._after_1 = 1 + finfo(self._dtype).eps

    def _solve_root(self, coef, **kwargs):
        # pylint: disable=unused-variable
        A, B, C, D = coef
        case, roots = solve_cubic(A, B, C, D, after_1=self._after_1)
        return roots
