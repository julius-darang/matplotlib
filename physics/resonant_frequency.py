import numpy as np


def f0(l, c):
    return 1 / (2 * np.pi * np.sqrt(l * c))


def f0_curve(c_values, l):
    return f0(l, c_values)
