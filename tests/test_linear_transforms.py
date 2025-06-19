import numpy as np
import pytest

from ValueWithError import make_ValueWithError, make_ValueWithError_from_vector


def test_linear_transform():
    v1 = make_ValueWithError(1.0)
    v2 = make_ValueWithError(1.0, SE=1)
    v3 = make_ValueWithError(1.0, SE=1, N=10)
    v4 = make_ValueWithError_from_vector(np.asarray([1.0, 2.0, 3.0]))

    print(str(v2))

    assert str(-v1) == "–1"
    assert str(-v2) == "–1.0 ± 1.0"
    assert str(-v3) == "–1.0 ± 1.0"
    with pytest.raises(ValueError):
        print(-v4)

    assert str(v1 + v1) == "2"
    assert str(v1 + v2) == "2.0 ± 1.0"
    assert str(v1 + v3) == "2.0 ± 1.0"
    with pytest.raises(ValueError):
        print(v1 + v4)

    assert str(v2 + v1) == "2.0 ± 1.0"
    a = v2 + v2
    print(a)
    assert str(v2 + v2) == "2.0 ± 1.4"
    with pytest.raises(ValueError):
        print(v2 + v3)
    with pytest.raises(ValueError):
        print(v2 + v4)

    assert str(v3 + v1) == "2.0 ± 1.0"
    with pytest.raises(ValueError):
        print(v3 + v2)
    with pytest.raises(ValueError):
        print(v3 + v3)
    with pytest.raises(ValueError):
        print(v3 + v4)

    with pytest.raises(ValueError):
        print(v4 + v1)
    with pytest.raises(ValueError):
        print(v4 + v2)
    with pytest.raises(ValueError):
        print(v4 + v3)
    with pytest.raises(ValueError):
        print(v4 + v4)

    assert str(v1 + 1) == "2"  # type: ignore[reportArgumentType]
    assert str(v2 + 1) == "2.0 ± 1.0"  # type: ignore[reportArgumentType]
    assert str(v3 + 1) == "2.0 ± 1.0"  # type: ignore[reportArgumentType]
    with pytest.raises(ValueError):
        print(v4 + 1)  # type: ignore[reportArgumentType]

    assert str(1 + v1) == "2"  # type: ignore[reportArgumentType]
    assert str(1 + v2) == "2.0 ± 1.0"  # type: ignore[reportArgumentType]
    assert str(1 + v3) == "2.0 ± 1.0"  # type: ignore[reportArgumentType]
    with pytest.raises(ValueError):
        print(1 + v4)  # type: ignore[reportArgumentType]

    assert v1 * -1 == -v1  # type: ignore[reportArgumentType]
    assert v2 * -1 == -v2  # type: ignore[reportArgumentType]
    assert v3 * -1 == -v3  # type: ignore[reportArgumentType]
    with pytest.raises(ValueError):
        print(v4 * 1)  # type: ignore[reportArgumentType]

    assert v1 * v1 == v1
    assert v1 * v2 == v2
    assert v1 * v3 == v3
    with pytest.raises(ValueError):
        print(v1 * v4)

    assert v2 * v1 == v2
    with pytest.raises(ValueError):
        print(v2 * v2)
    with pytest.raises(ValueError):
        print(v2 * v3)
    with pytest.raises(ValueError):
        print(v2 * v4)

    assert v3 * v1 == v3
    with pytest.raises(ValueError):
        print(v3 * v2)
    with pytest.raises(ValueError):
        print(v3 * v3)
    with pytest.raises(ValueError):
        print(v3 * v4)

    with pytest.raises(ValueError):
        print(v4 * v1)
    with pytest.raises(ValueError):
        print(v4 * v2)
    with pytest.raises(ValueError):
        print(v4 * v3)
    with pytest.raises(ValueError):
        print(v4 * v4)


if __name__ == "__main__":
    test_linear_transform()
