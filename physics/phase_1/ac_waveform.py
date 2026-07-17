import numpy as np


def sine_wave(t, amplitude=1.0, frequency=1.0, phase=0.0):
    return amplitude * np.sin(2 * np.pi * frequency * t + phase)


def deg_to_rad(degrees):
    return np.deg2rad(degrees)
