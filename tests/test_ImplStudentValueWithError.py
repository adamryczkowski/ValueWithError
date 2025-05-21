import pytest
from ValueWithError import ValueWithErrorRepresentationConfig
from ValueWithError.ImplStudentValueWithError import ImplStudentValueWithError
import numpy as np


def check_repr(
    instance: ImplStudentValueWithError, config: ValueWithErrorRepresentationConfig
) -> str:
    """Check the string representation of the instance."""
    return instance.pretty_repr(config)


def test_all():
    assert (
        check_repr(
            instance=ImplStudentValueWithError(value=123.123456, SE=0.123, N=1),
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
            instance=ImplStudentValueWithError(value=123.123456, SE=0.123, N=1),
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
            instance=ImplStudentValueWithError(value=123.123456, SE=np.inf, N=1),
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
            instance=ImplStudentValueWithError(value=123.123456, SE=-np.inf, N=1),
            config=ValueWithErrorRepresentationConfig(
                pad_raw_value_with_zeros=True,
                significant_digit_bare=2,
                significant_digit_se=2,
            ),
        )

    with pytest.raises(Exception) as _:
        check_repr(
            instance=ImplStudentValueWithError(value=123.123456, SE=np.nan, N=1),
            config=ValueWithErrorRepresentationConfig(
                pad_raw_value_with_zeros=True,
                significant_digit_bare=10,
                significant_digit_se=2,
            ),
        )

    assert (
        check_repr(
            instance=ImplStudentValueWithError(value=123.123456, SE=0.0, N=1),
            config=ValueWithErrorRepresentationConfig(
                significant_digit_se=1, significant_digit_bare=5
            ),
        )
        == "123.12"
    )

    assert (
        check_repr(
            instance=ImplStudentValueWithError(value=123.123456, SE=0.0, N=1),
            config=ValueWithErrorRepresentationConfig(significant_digit_bare=2),
        )
        == "120"
    )

    assert (
        check_repr(
            instance=ImplStudentValueWithError(value=123.123456, SE=0.123, N=1),
            config=ValueWithErrorRepresentationConfig(significant_digit_se=1),
        )
        == "123.1 ± 0.1"
    )

    assert (
        check_repr(
            instance=ImplStudentValueWithError(value=123.123456, SE=0.199, N=1),
            config=ValueWithErrorRepresentationConfig(significant_digit_se=1),
        )
        == "123.1 ± 0.2"
    )

    assert (
        check_repr(
            instance=ImplStudentValueWithError(value=np.inf, SE=0.199, N=1),
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
            instance=ImplStudentValueWithError(value=-np.inf, SE=0.199, N=1),
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
            instance=ImplStudentValueWithError(value=np.nan, SE=0.199, N=1),
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
