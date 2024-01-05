from __future__ import annotations

from abc import ABC, abstractmethod

import numpy as np

from .repr import value_with_error_repr


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
    def estimateSE(self) -> IValueWithError:
        ...

    def __repr__(self) -> str:
        return value_with_error_repr(self.value, self.SE)
