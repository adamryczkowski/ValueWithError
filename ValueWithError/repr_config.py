import warnings
from math import log, ceil, isinf, isnan

import numpy as np
from pydantic import BaseModel, Field


class ValueWithErrorRepresentationConfig(BaseModel):
    show_cis: bool = Field(default=True, description="Show confidence intervals")
    show_se: bool = Field(default=True, description="Show error")
    detect_integers: bool = Field(
        default=True,
        description="Detect integers and display them without decimal point",
    )
    prefer_sd: bool = Field(
        default=False, description="Prefer standard deviation over standard error"
    )
    show_ci_as_plusminus: bool = Field(
        default=False, description="Show confidence interval as ± notation"
    )
    significant_digit_se: int = Field(
        default=2, gt=0, description="Significant digits for standard error"
    )
    significant_digit_bare: int = Field(
        default=4, description="Significant digits for bare value"
    )
    pad_raw_value_with_zeros: bool = Field(
        default=False,
        description="Pad raw value (i.e. without SE) with zeros up to the required precision",
    )

    # __init__ is redundant, but needed to get PyCharm completion (as of May 2025)
    def __init__(
        self,
        show_cis: bool = True,
        show_se: bool = True,
        prefer_sd: bool = False,
        detect_integers=True,
        show_ci_as_plusminus: bool = False,
        significant_digit_se: int = 2,
        significant_digit_bare: int = 4,
        pad_raw_value_with_zeros: bool = False,
    ):
        super().__init__(
            show_cis=show_cis,
            show_se=show_se,
            prefer_sd=prefer_sd,
            detect_integers=detect_integers,
            show_ci_as_plusminus=show_ci_as_plusminus,
            significant_digit_se=significant_digit_se,
            significant_digit_bare=significant_digit_bare,
            pad_raw_value_with_zeros=pad_raw_value_with_zeros,
        )


def default_value_with_error_repr_config() -> ValueWithErrorRepresentationConfig:
    return ValueWithErrorRepresentationConfig()


def absolute_rounding_digit(
    signif_digit_position: int,
    value_is_SE_or_SD: bool,
    config: ValueWithErrorRepresentationConfig,
):
    """
    :param signif_digit_position: The position of the left-most non-zero (significant) digit.
    :param value_is_SE_or_SD: True if the value is a standard error or standard deviation, False if value is bare/mean.
    :param config: The configuration object containing significant digit settings.
    :return: The actual number of digits to round to. Zero means digits (i.e. 0 <= absolute_digit <= 9)
    Negative value means a digit before decimal point (123.0 would have -2)
    Positive value means a digit after decimal point (0.123 would have 3)
    """
    if value_is_SE_or_SD:
        return signif_digit_position + config.significant_digit_se - 1
    else:
        return signif_digit_position + config.significant_digit_bare - 1


def digit_position(value: float) -> int:
    """
    value: float to get the digit position of the first significant digit
    :return: The actual number of digits to round to. Zero means digits (i.e. 0 <= absolute_digit <= 9)
    Negative value means a digit before decimal point (123.0 would have -2)
    Positive value means a digit after decimal point (0.123 would have 3)
    """
    if isinf(value) or isnan(value) or np.isclose(value, 0):
        return 0
    return ceil(-log(abs(value), 10))


def suggested_precision_digit_pos(
    value: float, config: ValueWithErrorRepresentationConfig, value_is_SE_or_SD: bool
) -> int:
    """
    Returns the suggested precision digit position that works for all the values in the list.
    """

    return absolute_rounding_digit(digit_position(value), value_is_SE_or_SD, config)


def round_to_string(
    value: float, absolute_digit_pos: int, pad_with_zeroes: bool, detect_integers: bool
) -> str:
    """
    :param value: The value to represent.
    :param absolute_digit_pos: The absolute position of the least significant digit to retain in the representation.
    :param pad_with_zeroes: Only if absolute_digit>0. If True, pad with zeroes to the right of the decimal point.
    """
    if isinf(value):
        if value > 0:
            return "∞"
        else:
            return "–∞"

    if isnan(value):
        return "NaN"

    if absolute_digit_pos <= 0:
        return str(int(round(value, absolute_digit_pos)))

    if detect_integers:
        if value.is_integer():
            if value < 0:
                return f"–{int(-value)}"
            return str(int(value))
    rvalue = round(abs(value), absolute_digit_pos)
    add_minus = "–" if value < 0 else ""
    if pad_with_zeroes:
        return add_minus + format(rvalue, "." + str(absolute_digit_pos) + "f")
    return add_minus + str(round(value, absolute_digit_pos))


def suggested_precision_digit_pos_for_SE(
    mean: float, SE: float | None, config: ValueWithErrorRepresentationConfig
) -> int:
    if SE is None or isnan(SE) or isinf(SE) or np.isclose(SE, 0):
        return suggested_precision_digit_pos(mean, config, False)

    return absolute_rounding_digit(digit_position(SE), True, config)


def repr_value_with_error(
    mean: float,
    SE: float | None,
    absolute_digit_pos: int,
    config: ValueWithErrorRepresentationConfig,
) -> str:
    if isinf(mean):
        if mean > 0:
            return "∞"
        else:
            return "–∞"

    if isnan(mean):
        return "NaN"

    if SE is not None:
        if isnan(SE) or isinf(SE) or np.isclose(SE, 0):
            SE = None

    round_value_txt = round_to_string(
        mean,
        absolute_digit_pos,
        config.pad_raw_value_with_zeros or SE is not None,
        detect_integers=config.detect_integers
        and SE is None,  # We detect integers only if SE is None
    )

    if SE is not None and config.show_se and not config.show_ci_as_plusminus:
        round_SE_txt = round_to_string(
            SE, absolute_digit_pos, pad_with_zeroes=True, detect_integers=False
        )
        return f"{round_value_txt} ± {round_SE_txt}"

    return f"{round_value_txt}"


# def suggested_precision_digit_pos_for_SE(values: list[float],
#                                          config: ValueWithErrorRepresentationConfig, value_is_SE_or_SD: bool) -> int:
#     """
#     Returns the suggested precision digit position that works for all the values in the list.
#     """
#     # In the future, we may add a config option for more subtle handling of the rounding digit than just max
#     return max([absolute_rounding_digit(digit_position(value), value_is_SE_or_SD, config) for value in values])


def suggested_precision_digit_pos_for_CI(
    lower: float, upper: float, config: ValueWithErrorRepresentationConfig
) -> int:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        SE = upper - lower

    if isnan(SE) or isinf(SE) or np.isclose(SE, 0):
        absolute_digits = []
        if not isnan(lower) and not isinf(lower):
            absolute_digits.append(suggested_precision_digit_pos(lower, config, False))
        if not isnan(upper) and not isinf(upper):
            absolute_digits.append(suggested_precision_digit_pos(upper, config, False))
        if len(absolute_digits) == 0:
            return 0
        else:
            return max(absolute_digits)
    return suggested_precision_digit_pos(SE, config, True)


def CI_repr(
    lower: float,
    upper: float,
    absolute_digit_pos: int,
    config: ValueWithErrorRepresentationConfig,
) -> str:
    if not isnan(lower) and not isnan(upper):
        assert lower <= upper

    round_lower_txt = round_to_string(
        lower,
        absolute_digit_pos,
        pad_with_zeroes=config.pad_raw_value_with_zeros,
        detect_integers=False,
    )
    round_upper_txt = round_to_string(
        upper,
        absolute_digit_pos,
        pad_with_zeroes=config.pad_raw_value_with_zeros,
        detect_integers=False,
    )

    return f"({round_lower_txt}, {round_upper_txt})"
