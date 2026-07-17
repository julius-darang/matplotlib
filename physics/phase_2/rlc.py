import numpy as np


def step_response(t, zeta, omega0=1.0, V_s=1.0):
    if zeta < 1:
        wd = omega0 * np.sqrt(1 - zeta ** 2)
        phi = np.arccos(zeta)
        return V_s * (
            1
            - np.exp(-zeta * omega0 * t)
            / np.sqrt(1 - zeta ** 2)
            * np.sin(wd * t + phi)
        )
    elif zeta == 1:
        return V_s * (1 - (1 + omega0 * t) * np.exp(-omega0 * t))
    else:
        gamma = omega0 * np.sqrt(zeta ** 2 - 1)
        s1 = -zeta * omega0 + gamma
        s2 = -zeta * omega0 - gamma
        return V_s * (
            1 - (s2 * np.exp(s1 * t) - s1 * np.exp(s2 * t)) / (s2 - s1)
        )


def settling_time(zeta, omega0=1.0, V_s=1.0, tol=0.02, t_max=80, n=16000):
    t = np.linspace(0, t_max, n)
    v = step_response(t, zeta, omega0, V_s)
    within = np.abs(v - V_s) / V_s < tol
    outside = np.where(~within)[0]
    if len(outside) == 0:
        return 0.0
    last_out = outside[-1]
    if last_out + 1 >= n:
        return t_max
    return t[last_out + 1]


def settling_sweep(
    zeta_min=0.05,
    zeta_max=3.0,
    n_points=300,
    omega0=1.0,
    V_s=1.0,
    tol=0.02,
    t_max=80,
):
    zetas = np.linspace(zeta_min, zeta_max, n_points)
    t_settle = np.array(
        [settling_time(z, omega0, V_s, tol, t_max) for z in zetas]
    )
    return zetas, t_settle
