from __future__ import annotations

from abc import ABC, abstractmethod

import numpy as np

from .repr import value_with_error_repr, CI_repr
from overrides import overrides


class IValueWithError(ABC):
    @property
    @abstractmethod
    def value(self) -> float | np.ndarray:
        ...

    @property
    @abstractmethod
    def SE(self) -> float | np.ndarray | None:
        ...

    @property
    @abstractmethod
    def N(self) -> int | None:
        ...

    @abstractmethod
    def get_CI(self, level: float) -> I_CI:
        ...

    @abstractmethod
    def get_CI95(self) -> I_CI:
        ...

    @abstractmethod
    def estimateSE(self) -> IValueWithError:
        ...

    @abstractmethod
    def estimateMean(self) -> IValueWithError:
        ...

    def __repr__(self) -> str:
        return value_with_error_repr(self.value, self.SE)

    def repr(self, suppress_se: bool = False) -> str:
        return value_with_error_repr(self.value, self.SE, suppress_se)

    def stripCI(self) -> IValueWithError:
        return self


class I_CI(ABC):
    @property
    @abstractmethod
    def lower(self) -> float | np.ndarray:
        ...

    @property
    @abstractmethod
    def upper(self) -> float | np.ndarray:
        ...

    @property
    @abstractmethod
    def level(self) -> float:
        ...

    def __repr__(self) -> str:
        if 1 - self.level < 0.01:
            return f"CI_{round(self.level * 1000) / 10}%: {CI_repr(self.lower, self.upper)}"
        return f"CI_{round(self.level * 100)}%: {CI_repr(self.lower, self.upper)}"

    @property
    def level_txt(self) -> str:
        if 1 - self.level < 0.01:
            return f"{round(self.level * 1000) / 10}"
        return f"{round(self.level * 100)}"

    @property
    def width(self) -> float:
        return self.upper - self.lower

    @property
    def pretty_lower(self) -> str:
        return value_with_error_repr(self.lower, self.width, suppress_se=True)

    @property
    def pretty_upper(self) -> str:
        return value_with_error_repr(self.upper, self.width, suppress_se=True)


class I95CI(I_CI):
    """A class that simply holds two numbers that represent a 95% confidence/credible interval."""

    @property
    @overrides
    def level(self) -> float:
        return 0.95

    def __repr__(self) -> str:
        return f"CI_95%: {CI_repr(self.lower, self.upper)}"
