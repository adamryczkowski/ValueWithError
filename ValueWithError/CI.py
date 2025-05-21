from __future__ import annotations

from typing import Iterator

import numpy as np
from overrides import overrides
from pydantic import BaseModel, model_validator, Field

from .iface import I_CI
from .repr_config import ValueWithErrorRepresentationConfig, CI_repr


class CI_95(I_CI, BaseModel):
    lower_: float  # type: ignore
    upper_: float  # type: ignore

    def __init__(self, lower: float, upper: float, **kwargs):
        super().__init__(lower_=lower, upper_=upper, **kwargs)

    @property
    @overrides
    def lower(self) -> float:
        return self.lower_

    @property
    @overrides
    def upper(self) -> float:
        return self.upper_

    @model_validator(mode="after")
    def lower_le_upper(self):
        if self.lower_ > self.upper_:
            raise ValueError("Lower bound must not be greater than upper bound")
        return self

    @overrides
    def pretty_repr(
        self,
        config: ValueWithErrorRepresentationConfig,
        absolute_precision_digit: int | None = None,
    ) -> str:
        if absolute_precision_digit is None:
            absolute_precision_digit = self.suggested_precision_digit_pos(config)
        return f"CI_95%: {CI_repr(self.lower_, self.upper_, absolute_precision_digit, config)}"

    @staticmethod
    def CreateFromVector(
        generator: Iterator[float] | np.ndarray, N: int | None = None
    ) -> CI_95:
        v = [x for i, x in enumerate(generator) if N is None or i < N]
        perc = np.percentile(v, [2.5, 97.5])
        return CI_95(lower=float(perc[0]), upper=float(perc[1]))

    @property
    @overrides
    def level(self) -> float:
        return 0.95

    def __neg__(self) -> CI_95:
        return CI_95(lower=-self.upper, upper=-self.lower)


class CI_any(I_CI, BaseModel):
    lower_: float  # type: ignore
    upper_: float  # type: ignore
    level_: float = Field(gt=0, lt=1)  # type: ignore

    @property
    def level(self) -> float:
        return self.level_

    def __init__(self, lower: float, upper: float, level: float = 0.95, **kwargs):
        super().__init__(lower_=lower, upper_=upper, level_=level, **kwargs)

    @model_validator(mode="after")
    def lower_le_upper(self):
        if self.lower_ > self.upper_:
            raise ValueError("Lower bound must not be greater than upper bound")
        return self

    @property
    @overrides
    def lower(self) -> float:
        return self.lower_

    @property
    @overrides
    def upper(self) -> float:
        return self.upper_

    @overrides
    def pretty_repr(
        self,
        config: ValueWithErrorRepresentationConfig,
        absolute_precision_digit: int | None = None,
    ) -> str:
        if absolute_precision_digit is None:
            absolute_precision_digit = self.suggested_precision_digit_pos(config)
        return f"CI_{self.level_txt}%: {CI_repr(self.lower_, self.upper_, absolute_precision_digit, config)}"

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
