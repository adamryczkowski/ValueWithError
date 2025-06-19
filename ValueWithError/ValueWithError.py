from __future__ import annotations

from typing import Union, Optional

import numpy as np
from pydantic import BaseModel

from .ImplNormalValueWithError import ImplNormalValueWithError
from .ImplSampleValueWithError import ImplSampleValueWithError
from .ImplStudentValueWithError import ImplStudentValueWithError
from .ImplValueWithoutError import ImplValueWithoutError
from .iface import (
    IValueWithError_SE,
    IValueWithError_Estimate,
    IValueWithError_Sample,
    I_CI,
)
from .repr_config import ValueWithErrorRepresentationConfig


class ValueWithError(BaseModel):
    obj: Union[
        ImplValueWithoutError,
        ImplNormalValueWithError,
        ImplStudentValueWithError,
        ImplSampleValueWithError,
    ]

    def suggested_precision_digit_pos(
        self, config: ValueWithErrorRepresentationConfig
    ) -> int:
        return self.obj.suggested_precision_digit_pos(config)

    @property
    def value(self) -> float:
        return self.obj.value

    def pretty_repr(
        self,
        config: ValueWithErrorRepresentationConfig,
        absolute_precision_digit: int | None = None,
    ) -> str:
        return self.obj.pretty_repr(
            config, absolute_precision_digit=absolute_precision_digit
        )

    def __str__(self) -> str:
        return self.obj.__str__()

    @property
    def SE(self) -> float | None:
        if isinstance(self.obj, IValueWithError_SE):
            return self.obj.SE
        return None

    @property
    def CI95(self) -> I_CI | None:
        if isinstance(self.obj, IValueWithError_SE):
            return self.obj.CI95
        return None

    def get_CI(self, level: float) -> I_CI | None:
        if isinstance(self.obj, IValueWithError_SE):
            return self.obj.get_CI(level)
        return None

    @property
    def SD(self) -> float | None:
        if isinstance(self.obj, IValueWithError_Estimate):
            return self.obj.SD
        return None

    @property
    def N(self) -> int | float | None:
        if isinstance(self.obj, IValueWithError_Estimate):
            return self.obj.N
        return None

    def get_CI_from_SD(self, level: float) -> I_CI | None:
        if isinstance(self.obj, IValueWithError_Estimate):
            return self.obj.get_CI_from_SD(level)
        return None

    @property
    def sample(self) -> np.ndarray | None:
        if isinstance(self.obj, IValueWithError_Sample):
            return self.obj.sample
        return None

    def student_estimate(self) -> ValueWithError | None:
        if isinstance(self.obj, IValueWithError_Sample):
            se_obj = self.obj.student_estimate()
            assert isinstance(se_obj, ImplStudentValueWithError)
            return ValueWithError(obj=se_obj)
        if isinstance(self.obj, IValueWithError_Estimate):
            return self
        return None

    @property
    def SDEstimate(self) -> Optional[ValueWithError]:
        if isinstance(self.obj, (ImplValueWithoutError, ImplNormalValueWithError)):
            return None
        assert isinstance(
            self.obj, (ImplStudentValueWithError, ImplSampleValueWithError)
        )
        obj = self.obj.SDEstimate
        return ValueWithError(obj=obj)

    @property
    def SEEstimate(self) -> Optional[ValueWithError]:
        if isinstance(self.obj, ImplValueWithoutError):
            return None
        if isinstance(self.obj, ImplNormalValueWithError):
            obj = ImplValueWithoutError(value=self.obj.SE)
        else:
            assert isinstance(
                self.obj, (ImplStudentValueWithError, ImplSampleValueWithError)
            )
            obj = self.obj.SEEstimate
        return ValueWithError(obj=obj)
