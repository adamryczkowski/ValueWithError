from ValueWithError import ValueWithErrorRepresentationConfig
from ValueWithError.ImplValueWithoutError import ImplValueWithoutError
import numpy as np


def check_repr(
    instance: ImplValueWithoutError, config: ValueWithErrorRepresentationConfig
) -> str:
    """Check the string representation of the instance."""
    return instance.pretty_repr(config)


def test_all():
    VALUE = 52.127
    instance = ImplValueWithoutError(value=VALUE)
    assert instance.value == VALUE

    assert (
        check_repr(
            instance=instance,
            config=ValueWithErrorRepresentationConfig(
                pad_raw_value_with_zeros=False, significant_digit_bare=4
            ),
        )
        == "52.13"
    )

    assert (
        check_repr(
            instance=instance,
            config=ValueWithErrorRepresentationConfig(
                pad_raw_value_with_zeros=True, significant_digit_bare=8
            ),
        )
        == "52.127000"
    )

    assert (
        check_repr(
            instance=instance,
            config=ValueWithErrorRepresentationConfig(
                pad_raw_value_with_zeros=False, significant_digit_bare=8
            ),
        )
        == "52.127"
    )

    assert (
        check_repr(
            instance=instance,
            config=ValueWithErrorRepresentationConfig(
                pad_raw_value_with_zeros=True, significant_digit_bare=1
            ),
        )
        == "50"
    )

    assert (
        check_repr(
            instance=instance,
            config=ValueWithErrorRepresentationConfig(
                pad_raw_value_with_zeros=False, significant_digit_bare=1
            ),
        )
        == "50"
    )

    assert (
        check_repr(
            instance=instance,
            config=ValueWithErrorRepresentationConfig(
                pad_raw_value_with_zeros=True, significant_digit_bare=0
            ),
        )
        == "100"
    )

    assert (
        check_repr(
            instance=instance,
            config=ValueWithErrorRepresentationConfig(
                pad_raw_value_with_zeros=True, significant_digit_bare=-1
            ),
        )
        == "0"
    )


def test_inf():
    config = ValueWithErrorRepresentationConfig()
    assert ImplValueWithoutError(value=np.inf).pretty_repr(config) == "∞"
    assert ImplValueWithoutError(value=-np.inf).pretty_repr(config) == "–∞"
    assert ImplValueWithoutError(value=np.nan).pretty_repr(config) == "NaN"


if __name__ == "__main__":
    test_all()
    test_inf()
