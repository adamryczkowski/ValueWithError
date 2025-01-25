import ValueWithError
from ValueWithError import make_ValueWithError_from_vector
import numpy as np


def test1():
    np.random.seed(123)
    vec = np.random.normal(123456, 10, 100)
    b = make_ValueWithError_from_vector(vec)

    assert repr(b) == "123456 ± 11"

    assert repr(b.meanEstimate) == "123456.3 ± 1.1"
    assert repr(b.CI95) == "CI_95%: (123436, 123478)"
    assert repr(b.get_CI(0.995)) == "CI_99.5%: (123429, 123480)"
    assert repr(b.SDEstimate) == "11.3 ± 1.1"
    assert repr(b.SEEstimate) == "1.128 ± 0.080"

    c = ValueWithError.make_ValueWithError(mean=b.value, SD=b.SD, N=b.N)
    assert repr(c.meanEstimate) == "123456.3 ± 1.1"
    assert repr(c.CI95) == "CI_95%: (123434, 123479)"
    assert repr(c.get_CI(0.995)) == "CI_99.5%: (123424, 123489)"
    assert repr(c.SDEstimate) == "11.3 ± 1.1"
    assert repr(c.SEEstimate) == "1.13 ± 0.11"


if __name__ == "__main__":
    test1()
