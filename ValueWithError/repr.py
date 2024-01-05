from math import log, floor, isinf, isnan


def value_with_error_repr(mean: float, SE: float | None, significant_digit_se: int = 2) -> str:
    assert SE is None or SE >= 0

    if isinf(mean):
        return f"∞"

    if isnan(mean):
        return f"NaN"

    if SE is not None:
        if isnan(SE):
            SE = None

    if SE is None:
        absolute_digit = floor(log(abs(mean), 10)) - significant_digit_se + 1
    else:
        absolute_digit = floor(log(abs(SE), 10)) - significant_digit_se + 1

    if absolute_digit <= 0:
        round_value_txt = f"{round(mean, -absolute_digit):.{-absolute_digit}f}"
    else:
        round_value_txt = f"{round(mean, -absolute_digit):_.0f}"

    if SE is not None:
        if absolute_digit <= 0:
            round_se_txt = f"{round(SE, -absolute_digit):.{-absolute_digit}f}"
        else:
            round_se_txt = f"{round(SE, -absolute_digit):_.0f}"
        return f"{round_value_txt} ± {round_se_txt}"
    else:
        return f"{round_value_txt}"
