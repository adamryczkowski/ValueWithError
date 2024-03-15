from __future__ import annotations
from typing import Iterator

import numpy as np
from overrides import overrides
from .iface import IValueWithError, I95CI, I_CI
import scipy.stats
from math import isnan


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

    @overrides
    def get_CI(self, level: float) -> I_CI:
        return CI.CreateFromVector(self._values, level=level)

    @overrides
    def get_CI95(self) -> I95CI:
        return CI95.CreateFromVector(self._values)


class CI(I_CI):
    _lower: float
    _upper: float
    _level: float

    def CreateFromVector(generator: Iterator[float] | np.ndarray, N: int | None = None,
                         level: float = 0.95) -> CI95 | CI:
        v = [x for i, x in enumerate(generator) if N is None or i < N]

        perc = np.percentile(v, [(1 - level) / 2, 1 - (1 - level) / 2])
        if level == 0.95:
            return CI95(perc[0], perc[1])
        else:
            return CI(perc[0], perc[1], level)

    def __init__(self, lower: float, upper: float, level: float):
        assert isinstance(lower, float)
        assert isinstance(upper, float)
        assert isinstance(level, float)
        assert lower <= upper
        assert 0 < level < 1
        self._lower = lower
        self._upper = upper
        self._level = level

    @property
    @overrides
    def lower(self) -> float | np.ndarray:
        return self._lower

    @property
    @overrides
    def upper(self) -> float | np.ndarray:
        return self._upper

    @property
    @overrides
    def level(self) -> float:
        return self._level


class CI95(I95CI):
    _lower: float
    _upper: float

    def CreateFromVector(generator: Iterator[float] | np.ndarray, N: int | None = None) -> CI95:
        v = [x for i, x in enumerate(generator) if N is None or i < N]
        perc = np.percentile(v, [2.5, 97.5])
        return CI95(perc[0], perc[1])

    def __init__(self, lower: float, upper: float):
        assert isinstance(lower, float)
        assert isinstance(upper, float)
        if not isnan(lower) and not isnan(upper):
            assert lower <= upper
        self._lower = lower
        self._upper = upper

    @property
    @overrides
    def lower(self) -> float | np.ndarray:
        return self._lower

    @property
    @overrides
    def upper(self) -> float | np.ndarray:
        return self._upper


class ValueWithError(IValueWithError):
    _value: float | np.ndarray
    _SE: float | None
    _N: int | None

    def CreateFromVector(generator: Iterator[float] | np.ndarray, N: int | None = None,
                         estimate_mean: bool = False) -> ValueWithError:
        return make_ValueWithError_from_generator(generator, N, estimate_mean)

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

    @overrides(check_signature=False)  # We are allowing for None in the returned type just for this class
    def get_CI95(self) -> CI95 | None:
        if self.SE is None:
            return None
        if self._N is None:
            # Assume N is infinity and use normal distribution
            t = scipy.stats.norm.ppf(0.975)
        else:
            t = scipy.stats.t.ppf(0.975, self._N - 1)
        return CI95(self.value - t * self.SE, self.value + t * self.SE)

    @overrides(check_signature=False)  # We are allowing for None in the returned type just for this class
    def get_CI(self, level: float) -> CI | None:
        if self.SE is None:
            return None
        if self._N is None:
            # Assume N is infinity and use normal distribution
            t = scipy.stats.norm.ppf(1 - (1 - level) / 2)
        else:
            t = scipy.stats.t.ppf(1 - (1 - level) / 2, self._N - 1)
        return CI(self.value - t * self.SE, self.value + t * self.SE, level)

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



class ValueWithErrorCI(ValueWithError):
    """An extension to the ValueWithError that also remembers a single CI."""
    _ci: I_CI

    def __init__(self, value: float | np.ndarray, SE: float | np.ndarray | None,
                 ci_lower: float, ci_upper: float, ci_level: float = 0.95,
                 N: int | np.ndarray | None = None):
        super().__init__(value, SE, N)
        if ci_level == 0.95:
            self._ci = CI95(ci_lower, ci_upper)
        else:
            self._ci = CI(ci_lower, ci_upper, ci_level)

    @property
    def CI(self) -> I_CI:
        return self._ci

    @CI.setter
    def CI(self, value: I_CI):
        assert isinstance(value, I_CI)
        self._ci = value

    @overrides
    def __repr__(self):
        return f"{super().__repr__()} {self._ci}"

    @overrides
    def get_CI(self, level: float) -> CI | None:
        if level == self._ci.level:
            return self._ci
        else:
            raise ValueError("Cannot get CI with different level than the one stored")

    @overrides(check_signature=False)
    def get_CI95(self) -> I_CI:
        if self._ci.level == 0.95:
            return self._ci
        else:
            raise ValueError("Cannot get CI95 when the stored CI is not 95%")

    def stripCI(self)->ValueWithError:
        return ValueWithError(self._value, self._SE, self._N)


def make_ValueWithError_from_generator(generator: Iterator[float] | np.ndarray, N: int | None = None,
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
