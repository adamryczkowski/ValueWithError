from typing import Iterator

import numpy as np
from overrides import overrides
from .iface import IValueWithError


class ValueWithErrorVec(IValueWithError):
    """Class that remembers all the individual values that makes the mean and SE."""

    _values: np.ndarray
    _estimate_mean: bool

    def __init__(self, values: np.ndarray, estimate_mean: bool = False):
        self._values = values
        self._estimate_mean = bool(estimate_mean)

    @property
    @overrides
    def value(self) -> float | np.ndarray:
        return np.mean(self._values)

    @property
    @overrides
    def SE(self) -> np.ndarray:
        if self._estimate_mean:
            return np.std(self._values) / np.sqrt(len(self._values))
        else:
            return np.std(self._values)

    @property
    def vector(self) -> np.ndarray:
        return self._values

    @overrides
    def estimateSE(self) -> IValueWithError:
        se = self.SE
        ans = ValueWithError(se, se * np.sqrt(0.5 / (len(self._values) - 1)))
        return ans

    def __len__(self):
        return len(self._values)


class ValueWithError(IValueWithError):
    _value: float | np.ndarray
    _SE: float | None
    _N: int | None

    def __init__(self, value: float | np.ndarray, SE: float | np.ndarray | None, N: int | np.ndarray | None = None):
        if isinstance(value, np.ndarray):
            assert len(value.shape) == 1
            assert len(value) == 1
        if SE is not None:
            if isinstance(SE, np.ndarray):
                assert len(SE.shape) == 1
                assert len(SE) == 1
            SE = float(SE)

        if N is not None:
            assert isinstance(N, int) or isinstance(N, np.ndarray)
            if isinstance(N, np.ndarray):
                assert len(N.shape) == 1
                assert len(N) == 1
            N = int(N)

        self._value = float(value)
        self._SE = SE
        self._N = N

    @property
    @overrides
    def value(self) -> float:
        return self._value

    @value.setter
    def value(self, value: float | np.ndarray):
        if isinstance(value, np.ndarray):
            assert len(value.shape) == 1
            assert len(value) == 1
            value = value[0]
        self._value = float(value)

    @property
    @overrides
    def SE(self) -> np.ndarray | None:
        return self._SE

    @SE.setter
    def SE(self, value: float | np.ndarray | None):
        if value is not None:
            if isinstance(value, np.ndarray):
                assert len(value.shape) == 1
                assert len(value) == 1
                value = value[0]
            value = float(value)
        self._SE = value

    @overrides
    def estimateSE(self) -> IValueWithError:
        if self._N is not None and self._SE is not None:
            se = self.SE
            ans = ValueWithError(se, se * np.sqrt(0.5 / (self._N - 1)))
            return ans
        else:
            raise ValueError("Cannot estimate SE without N and SE")

    @staticmethod
    def CreateFromVectorSE(observations: np.ndarray):
        """
        Creates a ValueWithError from a vector of observations
        :param observations:
        :return:
        """
        value = np.mean(observations)
        SE = np.std(observations) / np.sqrt(len(observations))
        return ValueWithError(value, SE, len(observations))

    @staticmethod
    def CreateFromVectorSD(observations: np.ndarray):
        """
        Creates a ValueWithError from a vector of posterior draws.
        :param observations:
        :return:
        """
        value = np.mean(observations)
        SD = np.std(observations)
        return ValueWithError(value, SD, len(observations))


def make_ValueWithError_from_generator(generator: Iterator[float], N: int | None = None,
                                       estimate_mean: bool = False) -> ValueWithError:
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
    SE = np.sqrt(sumsq / count - mean * mean)
    if estimate_mean:
        SE = SE / np.sqrt(count)
    return ValueWithError(mean, SE, count)
