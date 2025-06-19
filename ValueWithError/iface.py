from __future__ import annotations

from abc import ABC, abstractmethod

import numpy as np
from numbers import Number

from .repr_config import (
    ValueWithErrorRepresentationConfig,
    default_value_with_error_repr_config,
    suggested_precision_digit_pos_for_CI,
)


class I_CI(ABC):
    @property
    @abstractmethod
    def level(self) -> float: ...

    @property
    @abstractmethod
    def lower(self) -> float: ...

    @property
    @abstractmethod
    def upper(self) -> float: ...

    def suggested_precision_digit_pos(
        self, config: ValueWithErrorRepresentationConfig
    ) -> int:
        return suggested_precision_digit_pos_for_CI(self.lower, self.upper, config)

    @abstractmethod
    def pretty_repr(
        self,
        config: ValueWithErrorRepresentationConfig,
        absolute_precision_digit: int | None = None,
    ) -> str: ...

    @property
    def level_txt(self) -> str:
        if 1 - self.level < 0.01:
            return f"{round(self.level * 1000) / 10}"
        return f"{round(self.level * 100)}"

    @property
    def width(self) -> float:
        return self.upper - self.lower

    def __str__(self):
        config = default_value_with_error_repr_config()
        return self.pretty_repr(config, self.suggested_precision_digit_pos(config))

    # @property
    # def pretty_lower(self) -> str:
    #     return value_with_error_repr(self.lower, self.width, suppress_se=True)
    #
    # @property
    # def pretty_upper(self) -> str:
    #     return value_with_error_repr(self.upper, self.width, suppress_se=True)
    #


class IValueWithError_Minimal(ABC):
    """Minimal interface for getting uniform treatment of various ValueWithError backing types"""

    @abstractmethod
    def suggested_precision_digit_pos(
        self, config: ValueWithErrorRepresentationConfig
    ) -> int: ...

    @property
    @abstractmethod
    def value(self) -> float: ...

    @abstractmethod
    def pretty_repr(
        self,
        config: ValueWithErrorRepresentationConfig,
        absolute_precision_digit: int | None = None,
    ) -> str: ...

    @property
    @abstractmethod
    def short_description(self) -> str: ...

    def __str__(self) -> str:
        config = default_value_with_error_repr_config()
        return self.pretty_repr(config, self.suggested_precision_digit_pos(config))


class IValueWithError_SE(IValueWithError_Minimal):
    """Builds on IValueWithError_Minimal to add CI and SE"""

    @property
    @abstractmethod
    def SE(self) -> float: ...

    @property
    @abstractmethod
    def CI95(self) -> I_CI: ...

    @abstractmethod
    def get_CI(self, level: float) -> I_CI: ...


class IValueWithError_Estimate(IValueWithError_SE):
    """Builds on IValueWithError_SE to add information about the sample size"""

    @property
    @abstractmethod
    def SD(self) -> float: ...

    @property
    @abstractmethod
    def N(self) -> int | float: ...

    @abstractmethod
    def get_CI_from_SD(self, level: float) -> I_CI: ...


class IValueWithError_Sample(IValueWithError_Estimate):
    """Builds on IValueWithError_Estimate to add information derivable from actual sample vector"""

    @property
    @abstractmethod
    def sample(self) -> np.ndarray: ...

    @abstractmethod
    def student_estimate(self) -> IValueWithError_Estimate: ...


class IValueWithError_LinearTransforms(ABC):
    @abstractmethod
    def __neg__(self) -> IValueWithError_LinearTransforms: ...

    @abstractmethod
    def __add__(
        self, other: IValueWithError_LinearTransforms | Number
    ) -> IValueWithError_LinearTransforms: ...

    def __sub__(
        self, other: IValueWithError_LinearTransforms | Number
    ) -> IValueWithError_LinearTransforms:
        return self.__add__(other.__neg__())  # type: ignore[return-value]

    @abstractmethod
    def __mul__(
        self, other: IValueWithError_LinearTransforms | Number
    ) -> IValueWithError_LinearTransforms: ...

    def __radd__(
        self, other: IValueWithError_LinearTransforms | Number
    ) -> IValueWithError_LinearTransforms:
        return self.__add__(other)

    def __rsub__(
        self, other: IValueWithError_LinearTransforms | Number
    ) -> IValueWithError_LinearTransforms:
        return self.__neg__().__add__(other)

    def __rmul__(
        self, other: IValueWithError_LinearTransforms | Number
    ) -> IValueWithError_LinearTransforms:
        return self.__mul__(other)


# class IValueWithError_RichInterface(ABC):
#     """Universal interface for ValueWithError objects"""
#
#     def __lt__(self, other: IValueWithError_Minimal | float) -> bool:
#         return self.compare(other) < 0
#
#     def __gt__(self, other: IValueWithError_Minimal | float) -> bool:
#         return self.compare(other) > 0
#
#
#     @abstractmethod
#     def compare(self, other: IValueWithError_Minimal | float, significance_level: float = 0.05) -> int: ...
