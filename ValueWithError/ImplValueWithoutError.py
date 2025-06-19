from __future__ import annotations

from overrides import overrides
from pydantic import BaseModel, Field, ConfigDict

from .iface import (
    IValueWithError_Minimal,
    IValueWithError_LinearTransforms,
    IValueWithError_SE,
)
from .repr_config import (
    ValueWithErrorRepresentationConfig as Config,
    round_to_string,
    suggested_precision_digit_pos,
)


class ImplValueWithoutError(
    BaseModel, IValueWithError_Minimal, IValueWithError_LinearTransforms
):
    """Value without error, that still implements the IValueWithError interface."""

    value_: float = Field(alias="value")
    model_config = ConfigDict(serialize_by_alias=True)

    # def __init__(self, value: float, **kwargs):
    #     super().__init__(value=value, **kwargs)

    @property
    @overrides
    def value(self) -> float:
        return self.value_

    @overrides
    def pretty_repr(
        self,
        config: Config,
        absolute_precision_digit: int | None = None,
    ) -> str:
        if absolute_precision_digit is None:
            absolute_precision_digit = self.suggested_precision_digit_pos(config)
        return round_to_string(
            self.value,
            absolute_precision_digit,
            config.pad_raw_value_with_zeros,
            config.detect_integers,
        )

    @overrides
    def suggested_precision_digit_pos(self, config: Config) -> int:
        return suggested_precision_digit_pos(self.value_, config, False)

    @overrides
    def __neg__(self) -> ImplValueWithoutError:
        return ImplValueWithoutError(value=-self.value_)

    @overrides
    def __add__(  # pyright: ignore[reportIncompatibleMethodOverride]
        self, other: IValueWithError_Minimal | float
    ) -> IValueWithError_LinearTransforms:
        if isinstance(other, float):
            return ImplValueWithoutError(value=self.value_ + other)
        elif isinstance(other, ImplValueWithoutError):
            return ImplValueWithoutError(value=self.value_ + other.value_)
        elif isinstance(other, IValueWithError_SE):
            assert isinstance(other, IValueWithError_LinearTransforms)
            return other.__add__(self)
        else:
            raise TypeError(f"Unsupported type for addition: {type(other)}")

    @overrides
    def __mul__(  # pyright: ignore[reportIncompatibleMethodOverride]
        self, other: IValueWithError_Minimal | float
    ) -> IValueWithError_LinearTransforms:
        if isinstance(other, float):
            return ImplValueWithoutError(value=self.value_ * other)
        elif isinstance(other, ImplValueWithoutError):
            return ImplValueWithoutError(value=self.value_ * other.value_)
        elif isinstance(other, IValueWithError_SE):
            assert isinstance(other, IValueWithError_LinearTransforms)
            return other + self
        else:
            raise TypeError(f"Unsupported type for addition: {type(other)}")

    def __str__(self) -> str:
        config = Config()
        return self.pretty_repr(config, self.suggested_precision_digit_pos(config))
