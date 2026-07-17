import numpy as np

K_B = 1.380649e-23
Q_E = 1.602176634e-19
IS_0 = 1e-12
N = 1.5
T_REF = 25.0

def v_thermal(t_celsius):
    return K_B * (t_celsius + 273.15) / Q_E

def isat(t_celsius):
    return IS_0 * 2 ** ((t_celsius - T_REF) / 10.0)

def diode_current(v, t_celsius):
    vt = v_thermal(t_celsius)
    is_ = isat(t_celsius)
    return is_ * (np.exp(v / (N * vt)) - 1)

def turn_on_voltage(t_celsius, i_threshold=100e-6):
    vt = v_thermal(t_celsius)
    is_ = isat(t_celsius)
    return N * vt * np.log(i_threshold / is_ + 1)
