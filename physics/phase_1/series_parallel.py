def series(*resistors):
    return sum(resistors)


def parallel(*resistors):
    return 1 / sum(1 / r for r in resistors)


def eq_series_n(r_single, n):
    return r_single * n


def eq_parallel_n(r_single, n):
    return r_single / n
