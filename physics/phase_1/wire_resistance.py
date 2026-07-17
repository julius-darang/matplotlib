import numpy as np


def resistance(resistivity, length, area):
    return resistivity * length / area


def r_vs_length(lengths, resistivity, area):
    return resistivity * lengths / area


def r_vs_area(length, resistivity, areas):
    return resistivity * length / areas
