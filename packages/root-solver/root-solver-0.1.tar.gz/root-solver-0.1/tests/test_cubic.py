from functools import cmp_to_key

from pytest import approx

from hypothesis import given, note, event, assume, example
from hypothesis.strategies import floats, complex_numbers

from numpy import isnan, inf, conj, isreal, abs as np_abs, isfinite

from root_solver import solve_cubic
from root_solver._cubic import (
    get_quotients_near_double, get_quotients_near_triple,
)

sensible_floats = floats(allow_nan=False, allow_infinity=False)
sensible_complex = complex_numbers(allow_nan=False, allow_infinity=False)


def generate_coefficents_from_roots(x_1, x_2, x_3):
    a = - (x_1 + x_2 + x_3)
    b = x_1 * x_2 + x_3 * (x_1 + x_2)
    c = - x_1 * x_2 * x_3
    return a, b, c


def bool_to_cmp(cond):
    return 1 if cond else -1


def pairwise_complex_cmp(a, b):
    if a == b:
        return 0
    if np_abs(a) == np_abs(b):
        if a.real == b.real:
            return bool_to_cmp(a.imag > b.imag)
        return bool_to_cmp(a.real > b.real)
    return bool_to_cmp(np_abs(a) > np_abs(b))


@given(sensible_floats, sensible_floats, sensible_floats)
@example(3., 1., 2.)
@example(0, 1., 2.)
@example(-1., -1., -1.)
@example(-1., 1., 1.)
def test_solve_cubic_all_real(x_1, x_2, x_3):
    A = 1
    B, C, D = generate_coefficents_from_roots(x_1, x_2, x_3)
    assume(all(isfinite([B, C, D])))
    note("B = {}".format(B))
    note("C = {}".format(C))
    note("D = {}".format(D))

    note("triple quotients: [{}, {}, {}]".format(*get_quotients_near_triple(
        A, B, C, D
    )))
    note("double quotients: [{}, {}]".format(*get_quotients_near_double(
        A, B, C, D
    )))

    case, roots = solve_cubic(A, B, C, D)
    note("Roots before ordering: [{}, {}, {}]".format(*roots))
    note("Case is {}".format(case))
    event("Case is {}".format(case))

    assert sorted(roots) == approx(sorted([x_1, x_2, x_3]))


@given(sensible_floats, sensible_complex)
def test_solve_cubic_all_complex(x_1, x_2):
    if isreal(x_2):
        x_2 = x_2.real
        x_3 = x_2
    else:
        x_3 = conj(x_2)

    A = 1
    B, C, D = generate_coefficents_from_roots(x_1, x_2, x_3)
    assume(all(isreal([B, C, D])))
    assume(all(isfinite([B, C, D])))
    note("B = {}".format(B))
    note("C = {}".format(C))
    note("D = {}".format(D))

    note("triple quotients: [{}, {}, {}]".format(*get_quotients_near_triple(
        A, B, C, D
    )))
    note("double quotients: [{}, {}]".format(*get_quotients_near_double(
        A, B, C, D
    )))

    case, roots = solve_cubic(A, B, C, D)
    note("Given roots before ordering: [{}, {}, {}]".format(x_1, x_2, x_3))
    note("Roots before ordering: [{}, {}, {}]".format(*roots))
    note("Case is {}".format(case))
    event("Case is {}".format(case))

    sorted_out_roots = sorted(roots, key=cmp_to_key(pairwise_complex_cmp))
    sorted_in_roots = sorted(
        [x_1, x_2, x_3], key=cmp_to_key(pairwise_complex_cmp)
    )

    assert sorted_out_roots == approx(sorted_in_roots)
