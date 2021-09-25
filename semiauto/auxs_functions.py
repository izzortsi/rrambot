# %%

from semiauto.constants import *

# %%


def interval_to_sec(interval: str):
    try:
        return int(interval[:-1]) * seconds_per_unit[interval[-1]]
    except (ValueError, KeyError):
        return None


def sync_intervals(time_range: str, interval_1: str, interval_2: str):

    trange_unit = time_range[-1]
    trange_sec = interval_to_sec(time_range)
    i1_sec = interval_to_sec(interval_1)
    i2_sec = interval_to_sec(interval_2)

    if not i1_sec <= i2_sec:
        i1_sec, i2_sec = i2_sec, i1_sec

    n_units = int((trange_sec / i1_sec) * i2_sec / interval_to_sec(f"1{trange_unit}"))

    return f"{n_units}{trange_unit}"


def to_relative_date(ntimes: str):
    """signature: to_relative_date(ntimes: str)"""

    return


# %%
