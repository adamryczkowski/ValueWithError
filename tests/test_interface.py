import ValueWithError
from ValueWithError import (
    make_ValueWithError_from_vector,
    ValueWithErrorRepresentationConfig as Config,
)
import numpy as np


def test1():
    np.random.seed(123)
    vec = np.random.normal(123456, 10, 100)
    b = make_ValueWithError_from_vector(vec)

    assert str(b) == "123456.3 ± 1.1"
    assert str(b.pretty_repr(Config(prefer_sd=True))) == "123456 ± 11"
    t = b.student_estimate()
    assert str(t) == "123456.3 ± 1.1"
    assert str(b.CI95) == "CI_95%: (123436, 123478)"
    assert str(b.get_CI(0.995)) == "CI_99.5%: (123429, 123480)"
    assert str(b.SDEstimate) == "11.3 ± 1.1"
    assert str(b.SEEstimate) == "1.13 ± 0.11"

    c = ValueWithError.make_ValueWithError(mean=b.value, SE=b.SE, N=b.N)
    assert str(c) == "123456.3 ± 1.1"
    assert str(c.get_CI_from_SD(level=0.95)) == "CI_95%: (123434, 123478)"
    assert str(c.get_CI_from_SD(0.995)) == "CI_99.5%: (123425, 123488)"
    assert str(c.SDEstimate) == "11.3 ± 1.1"
    assert str(c.SEEstimate) == "1.13 ± 0.11"


if __name__ == "__main__":
    test1()
