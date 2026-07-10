"""
physics.py
Pure equations only. No fig/ax objects live in this file — that's the
rule that lets one formula feed multiple panels (and multiple topics)
without copy-pasting math into plotting code.

Two starter topics: three-phase short circuit, and a radial-feeder
power flow (approximate, for a teaching-scale illustration).
"""
import numpy as np


# ---------------------------------------------------------------- SHORT CIRCUIT
def three_phase_fault_current(v_source_kv, z_source_ohm, z_line_ohm_per_km,
                                fault_distance_km):
    """
    I_k'' at a fault `fault_distance_km` down a feeder.
    Simplified single-source radial model (extend to IEC 60909 c-factor
    and Zₖ = Zₛ + Zₗᵢₙₑ·(R+jX) once you're ready for the full standard).
    """
    z_total = z_source_ohm + z_line_ohm_per_km * fault_distance_km
    v_phase = (v_source_kv * 1000) / np.sqrt(3)
    i_fault = v_phase / abs(z_total)
    return i_fault  # amps


def fault_current_profile(v_source_kv, z_source_ohm, z_line_ohm_per_km,
                            distances_km):
    return np.array([
        three_phase_fault_current(v_source_kv, z_source_ohm,
                                   z_line_ohm_per_km, d)
        for d in distances_km
    ])


# ---------------------------------------------------------------- POWER FLOW
def voltage_drop_radial(v_send_pu, r_pu, x_pu, p_pu, q_pu):
    """
    Approximate per-unit voltage drop along a radial line
    (the standard linearized ΔV ≈ (RP + XQ)/V approximation used for
    quick feeder-voltage-profile teaching plots).
    """
    delta_v = (r_pu * p_pu + x_pu * q_pu) / v_send_pu
    return v_send_pu - delta_v


def voltage_profile(v_send_pu, r_pu_per_km, x_pu_per_km, p_pu, q_pu,
                     distances_km):
    v = [v_send_pu]
    for i in range(1, len(distances_km)):
        seg_km = distances_km[i] - distances_km[i - 1]
        v_next = voltage_drop_radial(v[-1], r_pu_per_km * seg_km,
                                      x_pu_per_km * seg_km, p_pu, q_pu)
        v.append(v_next)
    return np.array(v)