import numpy as np


def three_phase_fault_current(v_source_kv, z_source_ohm, z_line_ohm_per_km,
                                fault_distance_km):
    z_total = z_source_ohm + z_line_ohm_per_km * fault_distance_km
    v_phase = (v_source_kv * 1000) / np.sqrt(3)
    i_fault = v_phase / abs(z_total)
    return i_fault


def fault_current_profile(v_source_kv, z_source_ohm, z_line_ohm_per_km,
                            distances_km):
    return np.array([
        three_phase_fault_current(v_source_kv, z_source_ohm,
                                   z_line_ohm_per_km, d)
        for d in distances_km
    ])
