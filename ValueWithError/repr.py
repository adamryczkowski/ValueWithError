#
#
# def value_with_error_repr(
#         mean: float,
#         SE: float | None,
#         significant_digit_se: int = 2,
#         significant_digit_bare: int = 4,
#         suppress_se: bool = False,
# ) -> str:
#     assert SE is None or SE >= 0
#
#     if isinf(mean):
#         return "∞"
#
#     if isnan(mean):
#         return "NaN"
#
#     if SE is not None:
#         if isnan(SE):
#             SE = None
#
#
#     if SE is None or np.isclose(SE, 0):
#         SE = None
#         absolute_digit_pos = digit_position(mean)
#         if not np.isclose(mean, 0):
#             absolute_digit = floor(log(abs(mean), 10)) - significant_digit_bare + 1
#         else:
#             absolute_digit = -significant_digit_bare + 1
#     else:
#         absolute_digit = floor(log(abs(SE), 10)) - significant_digit_se + 1
#
#     if absolute_digit <= 0:
#         round_value_txt = f"{round(mean, -absolute_digit):.{-absolute_digit}f}"
#     else:
#         round_value_txt = f"{round(mean, -absolute_digit):_.0f}"
#
#     if SE is not None:
#         if not suppress_se:
#             if absolute_digit <= 0:
#                 round_se_txt = f"{round(SE, -absolute_digit):.{-absolute_digit}f}"
#             else:
#                 round_se_txt = f"{round(SE, -absolute_digit):_.0f}"
#             return f"{round_value_txt} ± {round_se_txt}"
#         else:
#             return f"{round_value_txt}"
#     else:
#         if "." in round_value_txt:
#             round_value_txt = round_value_txt.rstrip("0").rstrip(".")
#         return f"{round_value_txt}"
#

# def CI_repr(lower: float, upper: float, significant_digit: int = 2) -> str:
#     if not isnan(lower) and not isnan(upper):
#         assert lower <= upper
#
#     with warnings.catch_warnings():
#         warnings.simplefilter("ignore")
#         SE = upper - lower
#
#     if isnan(SE) or isinf(SE) or SE == 0:
#         absolute_digits = []
#         if not isnan(lower) and not isinf(lower):
#             absolute_digits.append(floor(log(abs(lower), 10)) - significant_digit + 1)
#         if not isnan(upper) and not isinf(upper):
#             absolute_digits.append(floor(log(abs(upper), 10)) - significant_digit + 1)
#         if len(absolute_digits) == 0:
#             absolute_digit = 0
#         else:
#             absolute_digit = absolute_digits[0]
#     else:
#         absolute_digit = floor(log(abs(SE), 10)) - significant_digit + 1
#
#     if isnan(lower):
#         round_lower_txt = "NaN"
#     elif isinf(lower):
#         if lower < 0:
#             round_lower_txt = "-∞"
#         else:
#             round_lower_txt = "∞"
#     else:
#         if absolute_digit <= 0:
#             round_lower_txt = f"{round(lower, -absolute_digit):.{-absolute_digit}f}"
#         else:
#             round_lower_txt = f"{round(lower, -absolute_digit):_.0f}"
#
#     if isnan(upper):
#         round_upper_txt = "NaN"
#     elif isinf(upper):
#         if upper < 0:
#             round_upper_txt = "-∞"
#         else:
#             round_upper_txt = "∞"
#     else:
#         if absolute_digit <= 0:
#             round_upper_txt = f"{round(upper, -absolute_digit):.{-absolute_digit}f}"
#         else:
#             round_upper_txt = f"{round(upper, -absolute_digit):_.0f}"
#
#     return f"({round_lower_txt}, {round_upper_txt})"
#
#
# def show_values_err_manual(
#         x: list[float] | np.ndarray,
#         digits: int,
#         dx: None | list[float] | np.ndarray = None,
# ) -> list[str]:
#     """
#     Lowest level function to show values (potentially with errors) rounded to digits.
#     """
#     assert isinstance(x, (list, np.ndarray))
#     if dx is not None:
#         assert isinstance(dx, (list, np.ndarray))
#         assert len(x) == len(dx)
#     if dx is None:
#         return [f"{round_with_padding(one_x, digits)}" for one_x in x]
#     else:
#         return [
#             f"{round_with_padding(one_x, digits)} ± {round_with_padding(one_dx, digits)}"
#             for one_x, one_dx in zip(x, dx)
#         ]
#
#
#
# def show_values_err(
#         x: list[float] | np.ndarray,
#         dx: None | list[float] | np.ndarray = None,
#         significant_digit_se: int = 2,
#         significant_digit_bare: int = 4,
#         show_err: bool = True,
# ) -> list[str]:
#     assert isinstance(x, (list, np.ndarray))
#     if dx is not None:
#         if isinstance(dx, float):
#             dx = np.repeat(dx, len(x))
#         assert isinstance(dx, (list, np.ndarray))
#         assert len(x) == len(dx)
#         mean_digits = show_value_err_digits(
#             dx, significant_digits_count=significant_digit_se
#         )
#     else:
#         mean_digits = show_value_err_digits(
#             x, significant_digits_count=significant_digit_bare
#         )
#     if show_err:
#         ans = show_value_err_manual(x, digits=mean_digits, dx=dx)
#     else:
#         ans = show_value_err_manual(x, digits=mean_digits)
#     return ans
