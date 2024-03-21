from math import log, floor, isinf, isnan
import warnings
import numpy as np


def value_with_error_repr(mean: float, SE: float | None, significant_digit_se: int = 2,
                          suppress_se: bool = False) -> str:
    assert SE is None or SE >= 0

    if isinf(mean):
        return f"∞"

    if isnan(mean):
        return f"NaN"

    if SE is not None:
        if isnan(SE):
            SE = None

    if SE is None or np.isclose(SE, 0):
        SE = None
        absolute_digit = floor(log(abs(mean), 10)) - significant_digit_se + 1
    else:
        absolute_digit = floor(log(abs(SE), 10)) - significant_digit_se + 1

    if absolute_digit <= 0:
        round_value_txt = f"{round(mean, -absolute_digit):.{-absolute_digit}f}"
    else:
        round_value_txt = f"{round(mean, -absolute_digit):_.0f}"

    if SE is not None:
        if not suppress_se:
            if absolute_digit <= 0:
                round_se_txt = f"{round(SE, -absolute_digit):.{-absolute_digit}f}"
            else:
                round_se_txt = f"{round(SE, -absolute_digit):_.0f}"
            return f"{round_value_txt} ± {round_se_txt}"
        else:
            return f"{round_value_txt}"
    else:
        return f"{round_value_txt}"


def CI_repr(lower: float, upper: float, significant_digit: int = 2) -> str:
    if not isnan(lower) and not isnan(upper):
        assert lower <= upper

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        SE = upper - lower

    if isnan(SE) or isinf(SE) or SE == 0:
        absolute_digits = []
        if not isnan(lower) and not isinf(lower):
            absolute_digits.append(floor(log(abs(lower), 10)) - significant_digit + 1)
        if not isnan(upper) and not isinf(upper):
            absolute_digits.append(floor(log(abs(upper), 10)) - significant_digit + 1)
        if len(absolute_digits) == 0:
            absolute_digit = 0
        else:
            absolute_digit = absolute_digits[0]
    else:
        absolute_digit = floor(log(abs(SE), 10)) - significant_digit + 1

    if isnan(lower):
        round_lower_txt = f"NaN"
    elif isinf(lower):
        if lower < 0:
            round_lower_txt = f"-∞"
        else:
            round_lower_txt = f"∞"
    else:
        if absolute_digit <= 0:
            round_lower_txt = f"{round(lower, -absolute_digit):.{-absolute_digit}f}"
        else:
            round_lower_txt = f"{round(lower, -absolute_digit):_.0f}"

    if isnan(upper):
        round_upper_txt = f"NaN"
    elif isinf(upper):
        if upper < 0:
            round_upper_txt = f"-∞"
        else:
            round_upper_txt = f"∞"
    else:
        if absolute_digit <= 0:
            round_upper_txt = f"{round(upper, -absolute_digit):.{-absolute_digit}f}"
        else:
            round_upper_txt = f"{round(upper, -absolute_digit):_.0f}"

    return f"({round_lower_txt}, {round_upper_txt})"
