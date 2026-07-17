import numpy as np


def power_triangle(P=100.0, PF=1.0):
    S = P / PF
    Q = np.sqrt(S**2 - P**2)
    return P, Q, S


def s_vs_pf(P=100.0):
    PF_vals = np.linspace(0.6, 1.0, 300)
    S_vals = P / PF_vals
    return PF_vals, S_vals
