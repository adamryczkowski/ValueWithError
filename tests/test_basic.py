import pytest
def test_basic():
    from ValueWithError import ValueWithError, ValueWithErrorVec

    a = ValueWithError(1.0, 0.1)
    assert repr(a) == "1.00 ± 0.10"

    # 95% confidence interval calculated assuming normal distribution.
    assert repr(a.get_CI95()) == "CI_95%: (0.80, 1.20)"

    a = ValueWithError(1.0, 0.1,
                       N=5)  # N is the number of samples used to calculate the value. It is used by the CI calculation.
    assert repr(a.get_CI95())# Prints: CI_95%: (0.72, 1.28) - a bigger interval because of the smaller N

    import numpy as np
    np.random.seed(123)
    vec = np.random.normal(123456, 10, 100)
    b = ValueWithErrorVec(vec)

    print(b)
    assert repr(b) == "123456 ± 11"
    assert repr(b.get_CI95()) == "CI_95%: (123436, 123478)"

def test_vec():
    from ValueWithError import ValueWithErrorVec
    import numpy as np
    np.random.seed(123)
    vec = np.random.normal(123456, 10, 100)
    b = ValueWithErrorVec(vec, estimate_mean=True)

    assert repr(b) == "123456.3 ± 1.1"
    assert repr(b.get_CI95()) == "CI_95%: (123436, 123478)"
    assert repr(b.get_CI(0.995)) == "CI_99.5%: (123428.0, 123431.7)"

def test_edge1():
    from ValueWithError import ValueWithError
    a = ValueWithError(1.0, 0.0)
    assert repr(a) == "1.0"
    assert repr(a.get_CI95()) == "CI_95%: (1.0, 1.0)"

def test_edge2():
    from ValueWithError import ValueWithError
    import numpy as np
    a = ValueWithError(np.nan, 0.1)
    assert repr(a) == "NaN"
    assert repr(a.get_CI95()) == "CI_95%: (NaN, NaN)"
    b = ValueWithError(np.inf, 0.1)
    assert repr(b) == "∞"
    assert repr(b.get_CI95()) == "CI_95%: (∞, ∞)"

def test_error_with_ci():
    from ValueWithError import ValueWithErrorCI

    a = ValueWithErrorCI(1.0, 0.1, 0.9, 1.1)
    assert repr(a) == "1.00 ± 0.10 CI_95%: (0.90, 1.10)"

    # Test for assertion
    with pytest.raises(ValueError):
        a.get_CI(0.99)

    assert repr(a.get_CI95()) == "CI_95%: (0.90, 1.10)"