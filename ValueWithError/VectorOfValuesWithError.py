from numbers import Number
from typing import Iterator

from pydantic import BaseModel

from .ImplValueWithoutError import ImplValueWithoutError
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

    items: list[UnionOfAllValueWithErrorImpls]

    def __init__(self, items: list[UnionOfAllValueWithErrorImpls | float]):
        # Ensure all items are of the correct type
        for item in items:
            assert isinstance(item, (float, UnionOfAllValueWithErrorImpls))
        items = [  # type: ignore[reportArgumentType]
            ImplValueWithoutError(value=item) if isinstance(item, float) else item
            for item in items
        ]
        super().__init__(items=items)

    def table_repr(
        self,
        config: Config | None = None,
        absolute_precision_digit: int | None = None,
    ) -> list[str]:
        if config is None:
            config = Config(
                pad_raw_value_with_zeros=True,
                significant_digit_bare=2,
                detect_integers=False,
            )
        if absolute_precision_digit is None:
            out_precisions: list[int] = []
            for i, item in enumerate(self.items):
                if isinstance(item, Number):
                    # noinspection PyTypeChecker
                    item = float(item)  # pyright: ignore[reportArgumentType]
                    precision = suggested_precision_digit_pos(item, config, False)
                    if precision is not None:
                        out_precisions.append(precision)
                    continue
                assert isinstance(item, IValueWithError_Minimal)
                precision = item.suggested_precision_digit_pos(config)
                if precision is not None:
                    out_precisions.append(precision)
            if len(out_precisions) == 0:
                out_precisions = [0]
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
        return ans

    def __len__(self) -> int:
        return len(self.items)

    def __getitem__(self, index: int) -> UnionOfAllValueWithErrorImpls:
        return self.items[index]

    def __iter__(self) -> Iterator[UnionOfAllValueWithErrorImpls]:  # type: ignore[override]
        return iter(self.items)
