import numpy as np


def i_buildup(t, v_source, r, tau):
    return v_source / r * (1 - np.exp(-t / tau))


def i_decay(t, i_initial, tau):
    return i_initial * np.exp(-t / tau)


def time_constant(r, l):
    return l / r
