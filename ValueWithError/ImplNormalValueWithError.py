from __future__ import annotations

import numpy as np
from overrides import overrides
from pydantic import BaseModel, Field, ConfigDict
from scipy.stats import norm as norm_dist

from .CI import CI_95, CI_any
from .ImplValueWithoutError import ImplValueWithoutError
from .iface import (
    IValueWithError_SE,
    I_CI,
    IValueWithError_LinearTransforms,
    IValueWithError_Minimal,
)
from .repr_config import (
    ValueWithErrorRepresentationConfig as Config,
    repr_value_with_error,
    suggested_precision_digit_pos_for_SE,
)


class ImplNormalValueWithError(
    BaseModel, IValueWithError_SE, IValueWithError_LinearTransforms
):
    value_: float = Field(alias="value")
    SE_: float = Field(ge=0, alias="SE")
    model_config = ConfigDict(serialize_by_alias=True)

    # def __init__(self, value: float, SE: float, **kwargs):
    #     super().__init__(value_=value, SE_=SE, **kwargs)

    @property
    @overrides
    def SE(self) -> float:
        return self.SE_

    @property
    @overrides
    def value(self) -> float:
        return self.value_

    @overrides
    def suggested_precision_digit_pos(self, config: Config) -> int:
        return suggested_precision_digit_pos_for_SE(self.value_, self.SE_, config)

    @overrides
    def get_CI(self, level: float) -> I_CI:
        if np.isclose(level, 0.95):
            return CI_95(
                self.value_ - 1.959963984540054 * self.SE_,
                self.value_ + 1.959963984540054 * self.SE_,
            )
        else:
            z = float(norm_dist.ppf(1 - (1 - level) / 2))
            return CI_any(
                lower=self.value_ - z * self.SE_,
                upper=self.value_ + z * self.SE_,
                level=level,
            )

    @property
    @overrides
    def CI95(self) -> I_CI:
        return CI_95(
            lower=self.value_ - 1.959963984540054 * self.SE_,
            upper=self.value_ + 1.959963984540054 * self.SE_,
        )

    @overrides
    def pretty_repr(
        self,
        config: Config,
        absolute_precision_digit: int | None = None,
    ) -> str:
        if absolute_precision_digit is None:
            absolute_precision_digit = self.suggested_precision_digit_pos(config)
        return repr_value_with_error(
            self.value_, self.SE_, absolute_precision_digit, config
        )

    @overrides
    def __neg__(self) -> ImplNormalValueWithError:
        return ImplNormalValueWithError(value=-self.value_, SE=self.SE_)

    @overrides
    def __add__(  # pyright: ignore[reportIncompatibleMethodOverride]
        self, other: IValueWithError_Minimal | float
    ) -> IValueWithError_LinearTransforms:
        if isinstance(other, float):
            return ImplNormalValueWithError(value=self.value_ + other, SE=self.SE_)
        elif isinstance(other, ImplValueWithoutError):
            return ImplNormalValueWithError(
                value=self.value_ + other.value_, SE=self.SE_
            )
        elif isinstance(other, ImplNormalValueWithError):
            # A little controversial, as this implies that the errors are independent
            return ImplNormalValueWithError(
                value=self.value_ + other.value_, SE=np.sqrt(self.SE_**2 + other.SE_**2)
            )
        else:
            raise TypeError(f"Unsupported type for addition: {type(other)}")

    @overrides
    def __mul__(  # pyright: ignore[reportIncompatibleMethodOverride]
        self, other: IValueWithError_Minimal | float
    ) -> IValueWithError_LinearTransforms:
        if isinstance(other, float):
            return ImplNormalValueWithError(value=self.value_ * other, SE=self.SE_)
        elif isinstance(other, ImplValueWithoutError):
            return ImplNormalValueWithError(
                value=self.value_ * other.value_, SE=self.SE_
            )
        elif isinstance(other, ImplNormalValueWithError):
            # A little controversial, as this implies that the errors are independent
            return ImplNormalValueWithError(
                value=self.value_ * other.value_,
                SE=np.sqrt(
                    (self.SE_ * other.value_) ** 2 + (self.value_ * other.SE_) ** 2
                ),
            )
        else:
            raise TypeError(f"Unsupported type for multiplication: {type(other)}")

    def __str__(self) -> str:
        config = Config()
        return self.pretty_repr(config, self.suggested_precision_digit_pos(config))
