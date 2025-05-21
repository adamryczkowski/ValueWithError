import numpy as np
import pytest

from ValueWithError import ValueWithErrorRepresentationConfig
from ValueWithError.ImplNormalValueWithError import ImplNormalValueWithError


def check_repr(
    instance: ImplNormalValueWithError, config: ValueWithErrorRepresentationConfig
) -> str:
    """Check the string representation of the instance."""
    return instance.pretty_repr(config)


def test_all():
    assert (
        check_repr(
            instance=ImplNormalValueWithError(value=123.123456, SE=0.123),
            config=ValueWithErrorRepresentationConfig(
                pad_raw_value_with_zeros=False,
                significant_digit_bare=4,
                significant_digit_se=2,
            ),
        )
        == "123.12 ± 0.12"
    )

    assert (
        check_repr(
            instance=ImplNormalValueWithError(value=123.123456, SE=0.123),
            config=ValueWithErrorRepresentationConfig(
                pad_raw_value_with_zeros=True,
                significant_digit_bare=4,
                significant_digit_se=2,
            ),
        )
        == "123.12 ± 0.12"
    )

    assert (
        check_repr(
            instance=ImplNormalValueWithError(value=123.123456, SE=np.inf),
            config=ValueWithErrorRepresentationConfig(
                pad_raw_value_with_zeros=True,
                significant_digit_bare=4,
                significant_digit_se=2,
            ),
        )
        == "123.1"
    )

    with pytest.raises(Exception) as _:
        check_repr(
            instance=ImplNormalValueWithError(value=123.123456, SE=-np.inf),
            config=ValueWithErrorRepresentationConfig(
                pad_raw_value_with_zeros=True,
                significant_digit_bare=2,
                significant_digit_se=2,
            ),
        )

    with pytest.raises(Exception) as _:
        check_repr(
            instance=ImplNormalValueWithError(value=123.123456, SE=np.nan),
            config=ValueWithErrorRepresentationConfig(
                pad_raw_value_with_zeros=True,
                significant_digit_bare=10,
                significant_digit_se=2,
            ),
        )

    assert (
        check_repr(
            instance=ImplNormalValueWithError(value=123.123456, SE=0.123),
            config=ValueWithErrorRepresentationConfig(significant_digit_se=1),
        )
        == "123.1 ± 0.1"
    )

    assert (
        check_repr(
            instance=ImplNormalValueWithError(value=123.123456, SE=0.199),
            config=ValueWithErrorRepresentationConfig(significant_digit_se=1),
        )
        == "123.1 ± 0.2"
    )

    assert (
        check_repr(
            instance=ImplNormalValueWithError(value=123.123456, SE=0.0),
            config=ValueWithErrorRepresentationConfig(
                significant_digit_bare=5, significant_digit_se=1
            ),
        )
        == "123.12"
    )

    assert (
        check_repr(
            instance=ImplNormalValueWithError(value=123.123456, SE=0.0),
            config=ValueWithErrorRepresentationConfig(significant_digit_bare=2),
        )
        == "120"
    )

    with pytest.raises(Exception) as _:
        ValueWithErrorRepresentationConfig(significant_digit_se=0)

    with pytest.raises(Exception) as _:
        ValueWithErrorRepresentationConfig(significant_digit_se=-1)

    assert (
        check_repr(
            instance=ImplNormalValueWithError(value=np.inf, SE=0.199),
            config=ValueWithErrorRepresentationConfig(
                pad_raw_value_with_zeros=True,
                significant_digit_bare=1,
                significant_digit_se=2,
            ),
        )
        == "∞"
    )

    assert (
        check_repr(
            instance=ImplNormalValueWithError(value=-np.inf, SE=0.199),
            config=ValueWithErrorRepresentationConfig(
                pad_raw_value_with_zeros=True,
                significant_digit_bare=1,
                significant_digit_se=2,
            ),
        )
        == "–∞"
    )
    assert (
        check_repr(
            instance=ImplNormalValueWithError(value=np.nan, SE=0.199),
            config=ValueWithErrorRepresentationConfig(
                pad_raw_value_with_zeros=True,
                significant_digit_bare=1,
                significant_digit_se=2,
            ),
        )
        == "NaN"
    )


if __name__ == "__main__":
    test_all()
