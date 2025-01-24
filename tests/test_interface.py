from ValueWithError import make_ValueWithError_from_vector
import numpy as np


def test1():
    np.random.seed(123)
    vec = np.random.normal(123456, 10, 100)
    b = make_ValueWithError_from_vector(vec)

    assert repr(b.meanEstimate) == "123456.3 ± 1.1"
    assert repr(b.CI95) == "CI_95%: (123436, 123478)"
    assert repr(b.get_CI(0.995)) == "CI_99.5%: (123429, 123480)"
    assert repr(b.SDEstimate) == "11.3 ± 1.1"
    assert repr(b.SEEstimate) == "1.128 ± 0.080"


if __name__ == "__main__":
    test1()
