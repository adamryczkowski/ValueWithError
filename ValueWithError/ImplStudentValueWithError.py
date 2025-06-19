from numbers import Number

import numpy as np
from overrides import overrides
from pydantic import BaseModel, Field, ConfigDict
from scipy.stats import norm as norm_dist

from .CI import CI_95, CI_any
from .ImplNormalValueWithError import ImplNormalValueWithError
from .ImplValueWithoutError import ImplValueWithoutError
from .iface import (
    IValueWithError_Estimate,
    I_CI,
    IValueWithError_LinearTransforms,
    IValueWithError_Minimal,
)
from .repr_config import (
    ValueWithErrorRepresentationConfig as Config,
    suggested_precision_digit_pos_for_SE,
    repr_value_with_error,
)


class ImplStudentValueWithError(
    BaseModel, IValueWithError_Estimate, IValueWithError_LinearTransforms
):
    value_: float = Field(alias="value")
    SE_: float = Field(ge=0, alias="SE")
    N_: int | float = Field(ge=0, alias="N")
    model_config = ConfigDict(serialize_by_alias=True)

    # def __init__(self, value: float, SE: float, N: float, **kwargs):
    #     super().__init__(value=value, SE=SE, N=N, **kwargs)

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
    def suggested_precision_digit_pos(self, config: Config) -> int:
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
        return self._get_CI(level=level, SE=self.SE_)

    @overrides
    def get_CI_from_SD(self, level: float) -> I_CI:
        return self._get_CI(level=level, SE=self.SD)

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
        self, other: IValueWithError_Minimal | Number
    ) -> IValueWithError_LinearTransforms:
        if isinstance(other, Number):
            return ImplStudentValueWithError(
                value=self.value_ + float(other),  # type: ignore[reportArgumentType]
                SE=self.SE_,
                N=self.N_,  # type: ignore[reportArgumentType]
            )
        elif isinstance(other, ImplValueWithoutError):
            return ImplStudentValueWithError(
                value=self.value_ + other.value_, SE=self.SE_, N=self.N_
            )
        else:
            raise ValueError(f"Unsupported type for addition: {type(other)}")

    @overrides
    def __mul__(  # pyright: ignore[reportIncompatibleMethodOverride]
        self, other: IValueWithError_Minimal | Number
    ) -> IValueWithError_LinearTransforms:
        if isinstance(other, Number):
            return ImplStudentValueWithError(
                value=self.value_ * float(other),  # type: ignore[reportArgumentType]
                SE=self.SE_,
                N=self.N_,  # type: ignore[reportArgumentType]
            )
        elif isinstance(other, ImplValueWithoutError):
            return ImplStudentValueWithError(
                value=self.value_ * other.value_, SE=self.SE_, N=self.N_
            )
        else:
            raise ValueError(f"Unsupported type for multiplication: {type(other)}")

    @property
    def SDEstimate(self) -> ImplNormalValueWithError:
        return ImplNormalValueWithError(value=self.SD, SE=self.SD / np.sqrt(self.N - 1))

    @property
    def SEEstimate(self) -> ImplNormalValueWithError:
        return ImplNormalValueWithError(value=self.SE, SE=self.SE / np.sqrt(self.N - 1))

    def __str__(self) -> str:
        config = Config()
        return self.pretty_repr(config, self.suggested_precision_digit_pos(config))

    @property
    @overrides
    def short_description(self) -> str:
        return "value, standard error and sample size"
