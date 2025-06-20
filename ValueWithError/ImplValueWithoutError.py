from __future__ import annotations

from overrides import overrides
from pydantic import BaseModel, Field, ConfigDict
from numbers import Number

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
        if absolute_precision_digit is None:
            absolute_precision_digit = config.significant_digit_bare - 1
        return round_to_string(
            self.value,
            absolute_precision_digit,
            config.pad_raw_value_with_zeros,
            config.detect_integers,
            config.inf_threshold,
        )

    @overrides
    def suggested_precision_digit_pos(self, config: Config) -> int | None:
        return suggested_precision_digit_pos(self.value_, config, False)

    @overrides
    def __neg__(self) -> ImplValueWithoutError:
        return ImplValueWithoutError(value=-self.value_)

    @overrides
    def __add__(  # pyright: ignore[reportIncompatibleMethodOverride]
        self, other: IValueWithError_Minimal | Number
    ) -> IValueWithError_LinearTransforms:
        if isinstance(other, Number):
            return ImplValueWithoutError(value=self.value_ + float(other))  # type: ignore[reportArgumentType]
        elif isinstance(other, ImplValueWithoutError):
            return ImplValueWithoutError(value=self.value_ + other.value_)
        elif isinstance(other, IValueWithError_SE):
            if not isinstance(other, IValueWithError_LinearTransforms):
                raise ValueError(
                    f"Addition not supported between {self.short_description} and type {type(other)}"
                )
            return other + self
        else:
            raise ValueError(f"Unsupported type for addition: {type(other)}")

    @overrides
    def __mul__(  # pyright: ignore[reportIncompatibleMethodOverride]
        self, other: IValueWithError_Minimal | Number
    ) -> IValueWithError_LinearTransforms:
        if isinstance(other, Number):
            return ImplValueWithoutError(value=self.value_ * float(other))  # type: ignore[reportArgumentType]
        elif isinstance(other, ImplValueWithoutError):
            return ImplValueWithoutError(value=self.value_ * other.value_)
        elif isinstance(other, IValueWithError_SE):
            if not isinstance(other, IValueWithError_LinearTransforms):
                raise ValueError(
                    f"Multiplication not supported between {self.short_description} and type {type(other)}"
                )
            return other * self
        else:
            raise ValueError(f"Unsupported type for addition: {type(other)}")

    def __str__(self) -> str:
        config = Config()
        return self.pretty_repr(config, self.suggested_precision_digit_pos(config))

    @property
    @overrides
    def short_description(self) -> str:
        return "value without error"
