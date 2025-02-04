from __future__ import annotations

from typing import Iterator, Optional, Union

import numpy as np
from pydantic import BaseModel

from .value_with_error_impl import (
    ImplNormalValueWithError,
    ImplValueVec,
    ImplValueWithoutError,
    ImplStudentValueWithError,
    # ImplValueWithErrorCI,
    CI_95,
    CI_any,
)


def make_ValueWithError(
    mean: float,
    SD: float = None,
    N: int = None,
    CI: CI_any | CI_95 = None,
) -> ValueWithError:
    if SD is None:
        assert N is None
        obj = ImplValueWithoutError(value=mean)
    else:
        if N is None:
            obj = ImplNormalValueWithError(value=mean, SD=SD)
        else:
            obj = ImplStudentValueWithError(value=mean, SD=SD, N=N)

    if CI is not None:
        return ValueWithError(impl=obj, cis={CI.level: CI})
    return ValueWithError(impl=obj)


def make_ValueWithError_from_vector(
    vector: np.ndarray, N: int = None
) -> VectorOfValues:
    obj = ImplValueVec(values=vector, N=N)
    return VectorOfValues(impl=obj)


class ValueWithError(BaseModel):
    """A class that represents a value with an error."""

    impl: Union[
        ImplStudentValueWithError,
        ImplNormalValueWithError,
        # ImplValueVec,
        ImplValueWithoutError,
    ]
    cis: dict[float, CI_any | CI_95] = {}

    @property
    def value(self) -> float:
        return self.impl.value

    @property
    def SE(self) -> Optional[float]:
        if self.N is None:
            return None
        return self.impl.SD / np.sqrt(self.N)

    @property
    def SD(self) -> Optional[float]:
        return self.impl.SD

    @property
    def N(self) -> Optional[int | float]:
        return self.impl.N

    @property
    def CI95(self) -> CI95:
        if 0.95 not in self.cis:
            return self.impl.CI95
        else:
            return self.cis[0.95]

    def get_CI(self, level: float) -> CI_any | CI_95:
        if level in self.cis:
            return self.cis[level]
        else:
            return self.impl.get_CI(level)

    def stripCI(self):
        self.cis.clear()

    def __repr__(self):
        ans = repr(self.impl)
        if len(self.cis) > 0:
            # ans += " CIs: "
            for ci in self.cis.values():
                ans += " " + repr(ci)
            # ans = ans.rstrip()
        return ans

    def __str__(self):
        return self.__repr__()

    @property
    def meanEstimate(self) -> ValueWithError:
        if self.SD is None or self.N is None:
            obj = ImplValueWithoutError(value=self.value)
        else:
            obj = ImplStudentValueWithError(value=self.value, SD=self.SE, N=self.N)
        return ValueWithError(impl=obj)

    @property
    def SDEstimate(self) -> Optional[ValueWithError]:
        if self.SD is None or self.N is None:
            return None
        elif self.N is None:
            obj = ImplValueWithoutError(value=self.SD)
        else:
            obj = ImplNormalValueWithError(
                value=self.SD, SD=self.SD / np.sqrt(self.N - 1)
            )
        return ValueWithError(impl=obj)

    @property
    def SEEstimate(self) -> Optional[ValueWithError]:
        if self.SE is None or self.N is None:
            return None
        elif self.N is None:
            obj = ImplValueWithoutError(value=self.SE)
        else:
            obj = ImplNormalValueWithError(
                value=self.SE, SD=self.SE / np.sqrt(self.N - 1)
            )
        return ValueWithError(impl=obj)


class VectorOfValues(BaseModel):
    impl: ImplValueVec

    @property
    def value(self) -> float:
        return self.impl.value

    @property
    def SD(self) -> Optional[float]:
        return self.impl.SD

    @property
    def SE(self) -> Optional[float]:
        if self.impl.N == 0:
            return None
        if self.impl.N <= 1:
            return 0.0
        return self.impl.SD / np.sqrt(self.impl.N)

    @property
    def N(self) -> Optional[int | float]:
        return self.impl.N

    @property
    def CI95(self) -> CI95:
        return self.impl.CI95

    def get_CI(self, level: float) -> CI_any | CI_95:
        return self.impl.get_CI(level)

    def __repr__(self):
        return repr(self.impl)

    @property
    def meanEstimate(self) -> ValueWithError:
        if self.SD is None or self.N is None:
            obj = ImplValueWithoutError(value=self.value)
        else:
            obj = ImplStudentValueWithError(value=self.value, SD=self.SE, N=self.N)
        return ValueWithError(impl=obj)

    @property
    def SEEstimate(self) -> Optional[ValueWithError]:
        if self.SE is None:
            return None
        elif self.N is None:
            obj = ImplValueWithoutError(value=self.SE)
        else:
            obj = ImplNormalValueWithError(
                value=self.SE, SD=float(self.SE / np.sqrt(2 * (self.N - 1)))
            )
        return ValueWithError(impl=obj)

    @property
    def SDEstimate(self) -> Optional[ValueWithError]:
        if self.SD is None or self.N is None:
            return None
        elif self.N is None:
            obj = ImplValueWithoutError(value=self.SD)
        else:
            obj = ImplNormalValueWithError(
                value=self.SD, SD=self.SD / np.sqrt(self.N - 1)
            )
        return ValueWithError(impl=obj)

    def get_ValueWithError(self, CI_levels: list[float] = None) -> ValueWithError:
        if CI_levels is None:
            CI_levels = []
        obj = ImplStudentValueWithError(
            value=self.impl.value, SD=self.impl.SD, N=self.impl.N
        )
        cis = {
            level: CI_any.CreateFromVector(self.impl.values, N=None, level=level)
            for level in CI_levels
        }
        return ValueWithError(impl=obj, cis=cis)

    # @property
    # def meanEstimate(self) -> ValueWithError:
    #     obj = ImplStudentValueWithError(
    #         value=self.impl.value, SD=self.impl.SD / np.sqrt(self.N), N=self.impl.N
    #     )
    #     return ValueWithError(impl=obj)


def make_ValueWithError_from_generator(
    generator: Iterator[float] | np.ndarray,
    N: int | None = None,
    estimate_mean: bool = False,
) -> ImplNormalValueWithError:
    """
    Creates a ValueWithError from a generator using the inline method.
    :param generator: A generator that returns a float on each iteration.
    :param N: The number of iterations to run the generator. Otherwise, we iterate until the generator stops.
    :return: the ValueWithError
    """
    sum = 0.0
    sumsq = 0.0
    count = 0
    for value in generator:
        sum += value
        sumsq += value * value
        count += 1
        if N is not None and count >= N:
            break

    if count == 0:
        raise ValueError("Cannot create ValueWithError from empty generator")

    mean = sum / count
    SD = np.sqrt(sumsq / count - mean * mean)
    return make_ValueWithError(mean=float(mean), SD=float(SD), N=count)


def fromJSON(json: dict) -> ValueWithError:
    return ImplNormalValueWithError.model_validate(json)
