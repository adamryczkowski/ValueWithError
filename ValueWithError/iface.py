from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

from .repr import value_with_error_repr, CI_repr


class I_CI(ABC):
    @property
    @abstractmethod
    def level(self) -> float:
        ...

    @property
    @abstractmethod
    def lower(self) -> float:
        ...

    @property
    @abstractmethod
    def upper(self) -> float:
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


class IValueWithError(ABC):
    # impl: ImplValueVec | ImplValueWithError | ImplValueWithErrorN | ImplValueWithoutError | ImplValueWithErrorCI
    # impl: ImplValueWithError

    @abstractmethod
    def __repr__(self):
        ...

    @property
    @abstractmethod
    def value(self) -> float: ...

    @property
    @abstractmethod
    def SE(self) -> Optional[float]: ...

    @property
    @abstractmethod
    def SD(self) -> Optional[float]: ...

    @property
    @abstractmethod
    def N(self) -> Optional[int | float]: ...

    @property
    @abstractmethod
    def CI95(self) -> CI95: ...

    @abstractmethod
    def get_CI(self, level: float) -> I_CI: ...

    @abstractmethod
    def stripCI(self) -> IValueWithError:
        return self
