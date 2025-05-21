import numpy as np
from overrides import overrides
from pydantic import BaseModel, Field
from scipy.stats import norm as norm_dist

from .CI import CI_95, CI_any
from .iface import (
    IValueWithError_Estimate,
    I_CI,
    IValueWithError_LinearTransforms,
    IValueWithError_Minimal,
)
from .ImplValueWithoutError import ImplValueWithoutError
from .repr_config import (
    ValueWithErrorRepresentationConfig,
    suggested_precision_digit_pos_for_SE,
    repr_value_with_error,
)


class ImplStudentValueWithError(
    BaseModel, IValueWithError_Estimate, IValueWithError_LinearTransforms
):
    value_: float = Field(alias="value")
    SE_: float = Field(ge=0, alias="SE")
    N_: int | float = Field(ge=0, alias="N")

    # def __init__(self, value: float, SE: float, N: float):
    #     super().__init__(value=value, SE=SE, N=N)

    @property
    @overrides
    def SE(self) -> float:
        return self.SE_

    @property
    @overrides
    def SD(self) -> float:
        return self.SE_ * np.sqrt(self.N_)

    @property
    @overrides
    def N(self) -> int | float:
        return self.N_

    @property
    @overrides
    def value(self) -> float:
        return self.value_

    @overrides
    def suggested_precision_digit_pos(
        self, config: ValueWithErrorRepresentationConfig
    ) -> int:
        return suggested_precision_digit_pos_for_SE(
            self.value_, self.SD if config.prefer_sd else self.SE_, config
        )

    def _get_CI(self, level: float, SE: float) -> I_CI:
        if np.isclose(level, 0.95):
            return CI_95(
                self.value_ - 1.959963984540054 * SE,
                self.value_ + 1.959963984540054 * SE,
            )
        else:
            t = float(norm_dist.ppf(1 - (1 - level) / 2))
            return CI_any(
                lower=self.value_ - t * SE,
                upper=self.value_ + t * SE,
                level=level,
            )

    @overrides
    def get_CI(self, level: float) -> I_CI:
        return self._get_CI(self.SE_, level)

    @overrides
    def get_CI_from_SD(self, level: float) -> I_CI:
        return self._get_CI(self.SD, level)

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
        config: ValueWithErrorRepresentationConfig,
        absolute_precision_digit: int | None = None,
    ) -> str:
        if absolute_precision_digit is None:
            absolute_precision_digit = self.suggested_precision_digit_pos(config)
        return repr_value_with_error(
            self.value_,
            self.SD if config.prefer_sd else self.SE_,
            absolute_precision_digit,
            config,
        )

    @overrides
    def __neg__(self) -> IValueWithError_LinearTransforms:
        return ImplStudentValueWithError(value=-self.value_, SE=self.SE_, N=self.N_)

    @overrides
    def __add__(  # pyright: ignore[reportIncompatibleMethodOverride]
        self, other: IValueWithError_Minimal | float
    ) -> IValueWithError_LinearTransforms:
        if isinstance(other, float):
            return ImplStudentValueWithError(
                value=self.value_ + other, SE=self.SE_, N=self.N_
            )
        elif isinstance(other, ImplValueWithoutError):
            return ImplStudentValueWithError(
                value=self.value_ + other.value_, SE=self.SE_, N=self.N_
            )
        else:
            raise TypeError(f"Unsupported type for addition: {type(other)}")

    @overrides
    def __mul__(  # pyright: ignore[reportIncompatibleMethodOverride]
        self, other: IValueWithError_Minimal | float
    ) -> IValueWithError_LinearTransforms:
        if isinstance(other, float):
            return ImplStudentValueWithError(
                value=self.value_ * other, SE=self.SE_, N=self.N_
            )
        elif isinstance(other, ImplValueWithoutError):
            return ImplStudentValueWithError(
                value=self.value_ * other.value_, SE=self.SE_, N=self.N_
            )
        else:
            raise TypeError(f"Unsupported type for addition: {type(other)}")
