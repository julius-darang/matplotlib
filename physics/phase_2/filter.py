import numpy as np


def magnitude_db(f, fc):
    return -10 * np.log10(1 + (f / fc) ** 2)


def phase_deg(f, fc):
    return -np.degrees(np.arctan(f / fc))


def step_response(t, tau):
    return 1 - np.exp(-t / tau)


def corner_freq_rc(r, c):
    return 1 / (2 * np.pi * r * c)


def corner_freq_rl(r, l):
    return r / (2 * np.pi * l)
