# import numpy as np
#
# from ValueWithError import make_ValueWithError_from_vector, CI_95, make_ValueWithError
#
#
# def test_basic():
#     a = make_ValueWithError(1.0, 0.1)
#     assert repr(a) == "1.00 ± 0.10"
#
#     # 95% confidence interval calculated assuming normal distribution.
#     assert repr(a.CI95) == "CI_95%: (0.80, 1.20)"
#
#     a = make_ValueWithError(
#         1.0, 0.1, N=5
#     )  # N is the number of samples used to calculate the value. It is used by the CI calculation.
#     assert repr(
#         a.CI95
#     )  # Prints: CI_95%: (0.72, 1.28) - a bigger interval because of the smaller N
#
#     np.random.seed(123)
#     vec = np.random.normal(123456, 10, 100)
#     b = make_ValueWithError_from_vector(vector=vec)
#
#     assert repr(b) == "123456 ± 11"
#     assert repr(b.CI95) == "CI_95%: (123436, 123478)"
#     c = b.get_ValueWithError([0.95])
#     assert repr(c) == "123456 ± 11 CI_95%: (123436, 123478)"
#
#
# def test_vec():
#     np.random.seed(123)
#     vec = np.random.normal(123456, 10, 100)
#     b = make_ValueWithError_from_vector(vec)
#
#     assert repr(b.meanEstimate) == "123456.3 ± 1.1"
#     assert repr(b.CI95) == "CI_95%: (123436, 123478)"
#     assert repr(b.get_CI(0.995)) == "CI_99.5%: (123429, 123480)"
#
#
# def test_edge1():
#     a = make_ValueWithError(1.0, 0.0)
#     assert repr(a) == "1"
#     assert repr(a.CI95) == "CI_95%: (1.0, 1.0)"
#
#
# def test_edge2():
#     a = make_ValueWithError(np.nan, 0.1)
#     assert repr(a) == "NaN"
#     assert repr(a.CI95) == "CI_95%: (NaN, NaN)"
#     b = make_ValueWithError(np.inf, 0.1)
#     assert repr(b) == "∞"
#     assert repr(b.CI95) == "CI_95%: (∞, ∞)"
#
#
# def test_error_with_ci():
#     a = make_ValueWithError(1.0, 0.1, CI=CI_95(lower=0.9, upper=1.1))
#     assert repr(a) == "1.00 ± 0.10 CI_95%: (0.90, 1.10)"
#     assert repr(a.get_CI(0.99)) == "CI_99%: (0.74, 1.26)"
#
#     b = make_ValueWithError(1.0, CI=CI_95(lower=0.9, upper=1.1))
#     # Test for assertion
#     assert repr(b.get_CI(0.95)) == "CI_95%: (0.90, 1.10)"
#
#     assert repr(b.get_CI(0.99)) == "CI_99%: (1.0, 1.0)"
#
#     assert repr(a.CI95) == "CI_95%: (0.90, 1.10)"
#
#
# def test_sign():
#     a = make_ValueWithError(-13)
#     b = make_ValueWithError(-13, 1)
#     c = make_ValueWithError(-13, 1, 24)
#     assert repr(a) == "-13"
#     assert repr(-a) == "13"
#     assert repr(b) == "-13.0 ± 1.0"
#     assert repr(-b) == "13.0 ± 1.0"
#     assert repr(c) == "-13.0 ± 1.0"
#     assert repr(-c) == "13.0 ± 1.0"
#
#
# if __name__ == "__main__":
#     test_basic()
#     test_vec()
#     test_edge1()
#     test_edge2()
#     test_error_with_ci()
#     test_sign()
