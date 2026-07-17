def thevenin_voltage(v_source, r1, r2):
    return v_source * r2 / (r1 + r2)


def thevenin_resistance(r1, r2):
    return (r1 * r2) / (r1 + r2)


def norton_current(v_th, r_th):
    return v_th / r_th


def load_voltage(v_th, r_th, r_load):
    return v_th * r_load / (r_th + r_load)


def load_current(v_th, r_th, r_load):
    return v_th / (r_th + r_load)
