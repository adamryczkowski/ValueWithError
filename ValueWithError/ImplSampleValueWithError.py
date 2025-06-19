from __future__ import annotations

import numpy as np
from overrides import overrides
from pydantic import BaseModel, ConfigDict, Field

from .CI import CI_95, CI_any
from .ImplNormalValueWithError import ImplNormalValueWithError
from .ImplStudentValueWithError import ImplStudentValueWithError
from .iface import IValueWithError_Sample, I_CI, IValueWithError_Estimate
from .pydantic_numpy import NDArraySerializer
from .repr_config import (
    ValueWithErrorRepresentationConfig as Config,
    suggested_precision_digit_pos_for_SE,
    repr_value_with_error,
)


class ImplSampleValueWithError(IValueWithError_Sample, BaseModel):
    """Class that remembers all the individual values that makes the mean and SE."""

    sample_: NDArraySerializer = Field(alias="sample")
    model_config = ConfigDict(arbitrary_types_allowed=True, serialize_by_alias=True)

    # def __init__(self, sample: np.ndarray, **kwargs):
    #     super().__init__(sample_=sample, **kwargs)

    @property
    @overrides
    def sample(self) -> np.ndarray:
        return self.sample_

    @property
    @overrides
    def N(self) -> int | float:
        return len(self.sample)

    @overrides
    def get_CI_from_SD(self, level: float) -> I_CI:
        return self.student_estimate().get_CI_from_SD(level=level)

    @property
    @overrides
    def value(self) -> float:
        return float(np.mean(self.sample))

    @property
    @overrides
    def SD(self) -> float:
        return float(np.std(self.sample))

    @property
    @overrides
    def SE(self) -> float:
        return float(self.SD / np.sqrt(self.N))

    @overrides
    def suggested_precision_digit_pos(self, config: Config) -> int:
        return suggested_precision_digit_pos_for_SE(
            self.value, self.SD if config.prefer_sd else self.SE, config
        )

    @overrides
    def pretty_repr(
        self,
        config: Config,
        absolute_precision_digit: int | None = None,
    ) -> str:
        if absolute_precision_digit is None:
            absolute_precision_digit = self.suggested_precision_digit_pos(config)
        if config.prefer_sd:
            return repr_value_with_error(
                self.value, self.SD, absolute_precision_digit, config
            )
        return repr_value_with_error(
            self.value, self.SE, absolute_precision_digit, config
        )

    @property
    @overrides
    def CI95(self) -> CI_95:
        return CI_95.CreateFromVector(self.sample)

    @overrides
    def get_CI(self, level: float) -> I_CI:
        return CI_any.CreateFromVector(self.sample_, level=level)

    @overrides
    def student_estimate(self) -> IValueWithError_Estimate:
        try:
            return ImplStudentValueWithError(value=self.value, SE=self.SE, N=self.N)
        except Exception as e:
            raise ValueError(f"Failed to create student estimate: {e}")

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
        return f"continuous sample of size {self.N} with mean {self}"

    # @field_validator("sample_", mode='before')
    # @classmethod
    # def validate_sample(cls, v: Any) -> np.ndarray:
    #     return nd_array_before_validator(v)
