from numbers import Number

import numpy as np
from pydantic import BaseModel

from .ValueWithError import UnionOfAllValueWithErrorImpls
from .constructors import make_ValueWithError
from .iface import IValueWithError_Minimal
from .repr_config import (
    ValueWithErrorRepresentationConfig as Config,
    suggested_precision_digit_pos,
)


class VectorOfValuesWithError(BaseModel):
    """
    The main point of this class is to represent the values in a coherent manner, i.e. with shared precision and representation.
    """

    items: list[UnionOfAllValueWithErrorImpls | float]

    def table_repr(
        self,
        config: Config,
        absolute_precision_digit: int | None = None,
    ) -> str:
        if absolute_precision_digit is None:
            out_precisions: np.ndarray = np.zeros(len(self.items), dtype=int)
            for i, item in enumerate(self.items):
                if isinstance(item, Number):
                    # noinspection PyTypeChecker
                    item = float(item)  # pyright: ignore[reportArgumentType]
                    out_precisions[i] = suggested_precision_digit_pos(
                        item, config, False
                    )
                    continue
                assert isinstance(item, IValueWithError_Minimal)
                out_precisions[i] = item.suggested_precision_digit_pos(config)

            # We need to gather the precisions - probably find the some lower centile of it, and use it throughout
            out_precisions.sort()
            quantile = 0.8
            absolute_precision_digit = out_precisions[
                int(len(out_precisions) * quantile)
            ]

        ans: list[str] = [""] * len(self.items)
        for i, item in enumerate(self.items):
            if isinstance(item, Number):
                # noinspection PyTypeChecker
                item = make_ValueWithError(item)  # pyright: ignore[reportArgumentType]
            assert isinstance(item, IValueWithError_Minimal)
            ans[i] = item.pretty_repr(config, absolute_precision_digit)
        return str(ans)
