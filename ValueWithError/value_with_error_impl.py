from __future__ import annotations

from typing import Iterator, Optional, Annotated

import numpy as np
from pydantic import BaseModel, model_validator, Field, ConfigDict

# from pydantic.dataclasses import dataclass
from dataclasses import dataclass
from scipy.stats import t as t_dist, norm as norm_dist
from .pydantic_numpy import NDArraySerializer
from .iface import I_CI
from .repr import value_with_error_repr, CI_repr


class ImplValueWithoutError(BaseModel):
    """Value without error, that still implements the IValueWithError interface."""

    value: float

    def __repr__(self):
        return value_with_error_repr(self.value, None)

    @property
    def SE(self) -> Optional[float]:
        return None

    @property
    def SD(self) -> Optional[float]:
        return None

    @property
    def N(self) -> Optional[int | float]:
        return None

    @property
    def CI95(self) -> CI_95:
        return CI_95(lower=self.value, upper=self.value)

    def get_CI(self, level: float) -> I_CI:
        return CI_any(lower=self.value, upper=self.value, level=level)

    def __neg__(self) -> ImplValueWithoutError:
        return ImplValueWithoutError(value=-self.value)


class ImplNormalValueWithError(BaseModel):
    value: float
    SD: Annotated[float, Field(ge=0)]

    def __repr__(self):
        return value_with_error_repr(self.value, self.SD)

    @property
    def CI95(self) -> CI_95:
        return CI_95(
            lower=self.value - 1.96 * self.SD, upper=self.value + 1.96 * self.SD
        )

    def get_CI(self, level: float = 0.95) -> I_CI | None:
        if level == 0.95:
            return self.CI95
        t = norm_dist.ppf(1 - (1 - level) / 2)
        return CI_any(
            lower=float(self.value - t * self.SD),
            upper=float(self.value + t * self.SD),
            level=level,
        )

    # @property
    # def SD(self) -> Optional[float]:
    #     return None

    @property
    def N(self) -> Optional[int | float]:
        return None

    def __neg__(self) -> ImplNormalValueWithError:
        return ImplNormalValueWithError(value=-self.value, SD=self.SD)


class ImplStudentValueWithError(BaseModel):
    value: float
    SD: Annotated[float, Field(ge=0)]
    N: Annotated[float, Field(ge=1)]

    def __repr__(self):
        return value_with_error_repr(self.value, self.SD)

    @property
    def CI95(self) -> CI_95:
        return CI_95(
            lower=float(self.value - t_dist.ppf(0.975, self.N - 1) * self.SD),
            upper=float(self.value + t_dist.ppf(0.975, self.N - 1) * self.SD),
        )

    def get_CI(self, level: float) -> CI_any | None:
        t = t_dist.ppf(1 - (1 - level) / 2, self.N - 1)
        return CI_any(
            lower=float(self.value - t * self.SD),
            upper=float(self.value + t * self.SD),
            level=level,
        )

    def compressed_copy(self):
        return self

    def __neg__(self) -> ImplStudentValueWithError:
        return ImplStudentValueWithError(value=-self.value, SD=self.SD, N=self.N)


class ImplValueVec(BaseModel):
    """Class that remembers all the individual values that makes the mean and SE."""

    values: NDArraySerializer
    N: float | int
    model_config = ConfigDict(arbitrary_types_allowed=True)

    def __init__(self, values: np.ndarray, N: float | int | None = None):
        if N is not None:
            super().__init__(values=values, N=N)
        else:
            super().__init__(values=values, N=len(values))

    @property
    def vector(self) -> np.ndarray:
        return self.values

    @property
    def value(self) -> float:
        return float(np.mean(self.values))

    @property
    def SD(self) -> float:
        return float(np.std(self.values))

    # @property
    # def SE(self) -> float:
    #     return self.SD / np.sqrt(self.N)

    def __repr__(self):
        return value_with_error_repr(self.value, self.SD)

    @property
    def sample_length(self):
        return len(self.values)

    @property
    def CI95(self) -> CI_95:
        return CI_95.CreateFromVector(self.values)

    def get_CI(self, level: float) -> I_CI:
        return CI_any.CreateFromVector(self.values, level=level)

    def compressed_copy(self):
        return ImplStudentValueWithError(value=self.value, SD=self.SD, N=self.N)


@dataclass
class CI_95(I_CI, BaseModel):
    lower: float  # type: ignore
    upper: float  # type: ignore

    def __init__(self, lower: float, upper: float, **kwargs):
        super().__init__(lower=lower, upper=upper, **kwargs)

    @model_validator(mode="after")
    def lower_le_upper(self):
        if self.lower > self.upper:
            raise ValueError("Lower bound must not be greater than upper bound")
        return self

    def __repr__(self):
        return f"CI_95%: {CI_repr(self.lower, self.upper)}"

    @staticmethod
    def CreateFromVector(
        generator: Iterator[float] | np.ndarray, N: int | None = None
    ) -> CI_95:
        v = [x for i, x in enumerate(generator) if N is None or i < N]
        perc = np.percentile(v, [2.5, 97.5])
        return CI_95(lower=float(perc[0]), upper=float(perc[1]))

    @property
    def level(self) -> float:
        return 0.95

    def __neg__(self) -> CI_95:
        return CI_95(lower=-self.upper, upper=-self.lower)


class CI_any(I_CI, BaseModel):
    lower: float  # type: ignore
    upper: float  # type: ignore
    level_: Annotated[float, Field(gt=0, lt=1)]  # type: ignore

    @property
    def level(self) -> float:
        return self.level_

    def __init__(self, lower: float, upper: float, level: float = 0.95, **kwargs):
        super().__init__(lower=lower, upper=upper, level_=level, **kwargs)

    def __repr__(self):
        if 1 - self.level < 0.01:
            return f"CI_{round(self.level * 1000) / 10}%: {CI_repr(self.lower, self.upper)}"
        return f"CI_{round(self.level * 100)}%: {CI_repr(self.lower, self.upper)}"

    @model_validator(mode="after")
    def lower_le_upper(self):
        if self.lower > self.upper:
            raise ValueError("Lower bound must not be greater than upper bound")
        return self

    @staticmethod
    def CreateFromVector(
        generator: Iterator[float] | np.ndarray,
        N: int | None = None,
        level: float = 0.95,
    ) -> CI_95 | CI_any:
        v = [x for i, x in enumerate(generator) if N is None or i < N]

        perc = np.percentile(v, [(1 - level) * 50, 100 - (1 - level) * 50])
        if level == 0.95:
            return CI_95(lower=float(perc[0]), upper=float(perc[1]), level=0.95)
        else:
            return CI_any(
                lower=float(perc[0]), upper=float(perc[1]), level=float(level)
            )

    def __neg__(self) -> CI_any:
        return CI_any(lower=-self.upper, upper=-self.lower, level=self.level)


#
# class ImplValueWithErrorCI(BaseModel):
#     """An extension to the ValueWithError that also remembers a single CI."""
#
#     obj: Union[
#         ImplValueWithError, ImplValueWithErrorN, ImplValueVec, ImplValueWithoutError
#     ]
#     CI: Union[CI_95, CI_any]
#
#     def __repr__(self):
#         return f"{repr(self.obj)} {repr(self.CI)}"
#
#     def get_CI(self, level: float) -> CI_any | CI_95:
#         if level == self.CI.level:
#             return self.CI
#         else:
#             raise ValueError("Cannot get CI with different level than the one stored")
#
#     @property
#     def CI95(self) -> CI_95:
#         return self.get_CI(0.95)
#
#     @property
#     def value(self) -> float:
#         return self.obj.value
#
#     @property
#     def SE(self) -> Optional[float]:
#         return self.obj.SE
#
#     @property
#     def SD(self) -> Optional[float]:
#         return self.obj.SD
#
#     @property
#     def N(self) -> Optional[int | float]:
#         return self.obj.N
#
#     def stripCI(self) -> IValueWithError:
#         return self.obj
#
#     def compressed_copy(self):
#         impl = self.obj.compressed_copy()
#         return ImplValueWithErrorCI(obj=impl, CI=self.CI)
