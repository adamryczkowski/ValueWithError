from __future__ import annotations

from typing import Iterator, Optional

import numpy as np
from pydantic import BaseModel

from .value_with_error_impl import ImplValueWithError, ImplValueVec, ImplValueWithoutError, ImplValueWithErrorN, \
    IValueWithError, ImplValueWithErrorCI, CI_95, CI_any


def make_ValueWithError(mean: float, SE: float = None, SD: float = None, N: int = None, CI: CI_any | CI_95 = None):
    if N is None:
        if SE is None and SD is None:
            obj = ImplValueWithoutError(value=mean)
        else:
            assert SD is None, "Cannot build ValueWithError with SD. Provide just SE or N instead."
            obj = ImplValueWithError(value=mean, SE=SE)
    elif SD is not None:
        assert SE is None, "Ambiguous input. Cannot build ValueWithError with both SE and SD. Provide just one."
        obj = ImplValueWithErrorN(value=mean, SD=SD, N=N)
    elif SE is not None:
        obj = ImplValueWithErrorN(value=mean, SD=SE * np.sqrt(N), N=N)
    else:
        obj = ImplValueWithoutError(value=mean)

    if CI is not None:
        obj = ImplValueWithErrorCI(obj=obj, CI=CI)
    return ValueWithError(impl=obj)

def make_ValueWithError_from_vector(vector: np.ndarray, N: int = None, CI: CI_any | CI_95 = None):
    obj = ImplValueVec(values=vector, N=N)
    if CI is not None:
        obj = ImplValueWithErrorCI(obj=obj, CI=CI)
    return ValueWithError(impl=obj)


class ValueWithError(BaseModel):
    """A class that represents a value with an error."""
    impl: ImplValueWithError | ImplValueVec | ImplValueWithErrorN | ImplValueWithoutError | ImplValueWithErrorCI

    @property
    def value(self) -> float:
        return self.impl.value

    @property
    def SE(self) -> Optional[float]:
        return self.impl.SE

    @property
    def SD(self) -> Optional[float]:
        return self.impl.SD

    @property
    def N(self) -> Optional[int | float]:
        return self.impl.N

    @property
    def CI95(self) -> CI95:
        return self.impl.CI95

    def get_CI(self, level: float) -> CI_any | CI_95:
        return self.impl.get_CI(level)

    def stripCI(self) -> IValueWithError:
        return self.impl.stripCI()

    def __repr__(self):
        return repr(self.impl)

    def estimateMean(self) -> ValueWithError:
        if self.SE is None or self.N is None:
            obj = ImplValueWithoutError(value=self.value)
        else:
            obj = ImplValueWithError(value=self.value, SE=self.SE)
        return ValueWithError(impl=obj)

    def estimateSE(self) -> Optional[ValueWithError]:
        if self.SE is None:
            return None
        elif self.N is None:
            obj = ImplValueWithoutError(value=self.SE)
        else:
            obj = ImplValueWithError(value=self.SE, SE=self.SE / np.sqrt(2 * (self.N - 1)))
        return ValueWithError(impl=obj)

    def estimateSD(self) -> Optional[ValueWithError]:
        if self.SD is None:
            return None
        elif self.N is None:
            obj = ImplValueWithoutError(value=self.SD)
        else:
            obj = ImplValueWithError(value=self.SD, SE=self.SD / np.sqrt(self.N - 1))
        return ValueWithError(impl=obj)


def make_ValueWithError_from_generator(generator: Iterator[float] | np.ndarray, N: int | None = None,
                                       estimate_mean: bool = False) -> ImplValueWithError:
    """
    Creates a ValueWithError from a generator using the inline method.
    :param generator: A generator that returns a float on each iteration.
    :param N: The number of iterations to run the generator. Otherwise, we iterate until the generator stops.
    :return: the ValueWithError
    """
    sum = 0.
    sumsq = 0.
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
