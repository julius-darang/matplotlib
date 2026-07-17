import numpy as np


def current(voltage, resistance):
    return voltage / resistance


def power(voltage, resistance):
    return voltage ** 2 / resistance


def current_profile(voltage, resistances):
    return np.array([current(voltage, r) for r in resistances])


def power_profile(voltage, resistances):
    return np.array([power(voltage, r) for r in resistances])
