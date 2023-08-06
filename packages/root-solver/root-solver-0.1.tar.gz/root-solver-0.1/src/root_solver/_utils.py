"""
Utility functions
"""
from numpy import around as np_round, log2, frombuffer, uint8


def float_to_bytes(a):
    """
    Convert arbitrary sized float to bytes
    """
    return frombuffer(a.tobytes(), dtype=uint8)


def bytes_to_float(a, *, dtype):
    """
    Convert bytes to given float type
    """
    return frombuffer(a, dtype=dtype)


def check_pairwise(a, func):
    """
    Check whether a condition (computed by `func`) holds pairwise for elements
    in the sequence `a`. Assumes `func` is symmetric for the two operands.
    """
    if len(a) < 2:
        return True
    for i, x, in enumerate(a, 1):
        for y in a[i:]:
            if not func(x, y):
                return False
    return True


def get_shared_figs(np_arr, *, dtype=None):
    """
    Get shared binary digits between floats in array
    """
    base = None

    if dtype is None:
        dtype = np_arr.dtype

    for n in np_arr:
        if base is None:
            base = float_to_bytes(n)
        else:
            base = base & float_to_bytes(n)

    return bytes_to_float(base, dtype=dtype)[0]


def get_nearest_radix(x):
    """
    Get nearest power of 2 to number
    """
    return pow(2, np_round(log2(x)))
