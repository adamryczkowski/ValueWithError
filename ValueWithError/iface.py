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

    @abstractmethod
    def get_CI(self, level: float) -> I_CI:
        ...

    @abstractmethod
    def get_CI95(self) -> I_CI:
        ...

    @abstractmethod
    def estimateSE(self) -> IValueWithError:
        ...

    def __repr__(self) -> str:
        return value_with_error_repr(self.value, self.SE)


    def stripCI(self)->IValueWithError:
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
    def level_txt(self)->str:
        if 1 - self.level < 0.01:
            return f"{round(self.level * 1000) / 10}"
        return f"{round(self.level * 100)}"

    @property
    def width(self)->float:
        return self.upper - self.lower

class I95CI(I_CI):
    """A class that simply holds two numbers that represent a 95% confidence/credible interval."""

    @property
    @overrides
    def level(self) -> float:
        return 0.95

    def __repr__(self) -> str:
        return f"CI_95%: {CI_repr(self.lower, self.upper)}"

