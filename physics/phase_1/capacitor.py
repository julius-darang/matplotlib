import numpy as np


def v_charge(t, v_source, tau):
    return v_source * (1 - np.exp(-t / tau))


def v_discharge(t, v_source, tau):
    return v_source * np.exp(-t / tau)


def time_constant(r, c):
    return r * c
