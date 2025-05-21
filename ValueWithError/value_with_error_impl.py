# from __future__ import annotations
#
# from typing import Iterator, Optional, Annotated
#
# import numpy as np
# from pydantic import BaseModel, model_validator, Field, ConfigDict
#
# # from pydantic.dataclasses import dataclass
# from dataclasses import dataclass
# from scipy.stats import t as t_dist, norm as norm_dist
# from .pydantic_numpy import NDArraySerializer
# from .iface import I_CI,IValueWithError_Minimal , IValueWithError_SE, IValueWithError_Estimate , IValueWithError_Sample
# #from .repr import value_with_error_repr, CI_repr, show_value_err_digits
# from overrides import overrides
#
# from .repr_config import ValueWithErrorRepresentationConfig, absolute_rounding_digit
# from .repr import digit_position, round_to_string
#
#
#
#
#
# class ImplStudentValueWithError(BaseModel):
#     value: float
#     SD: Annotated[float, Field(ge=0)]
#     N: Annotated[float, Field(ge=1)]
#
#     def __repr__(self):
#         return value_with_error_repr(self.value, self.SD)
#
#     @property
#     def CI95(self) -> CI_95:
#         return CI_95(
#             lower=float(self.value - t_dist.ppf(0.975, self.N - 1) * self.SD),
#             upper=float(self.value + t_dist.ppf(0.975, self.N - 1) * self.SD),
#         )
#
#     def get_CI(self, level: float) -> CI_any | None:
#         t = t_dist.ppf(1 - (1 - level) / 2, self.N - 1)
#         return CI_any(
#             lower=float(self.value - t * self.SD),
#             upper=float(self.value + t * self.SD),
#             level=level,
#         )
#
#     def compressed_copy(self):
#         return self
#
#     def __neg__(self) -> ImplStudentValueWithError:
#         return ImplStudentValueWithError(value=-self.value, SD=self.SD, N=self.N)
#
#
# # class ImplValueVec(BaseModel):
# #     """Class that remembers all the individual values that makes the mean and SE."""
# #
# #     values: NDArraySerializer
# #     N: float | int
# #     model_config = ConfigDict(arbitrary_types_allowed=True)
# #
# #     def __init__(self, values: np.ndarray, N: float | int | None = None):
# #         if N is not None:
# #             super().__init__(values=values, N=N)
# #         else:
# #             super().__init__(values=values, N=len(values))
# #
# #     @property
# #     def vector(self) -> np.ndarray:
# #         return self.values
# #
# #     @property
# #     def value(self) -> float:
# #         return float(np.mean(self.values))
# #
# #     @property
# #     def SD(self) -> float:
# #         return float(np.std(self.values))
# #
# #     # @property
# #     # def SE(self) -> float:
# #     #     return self.SD / np.sqrt(self.N)
# #
# #     def __repr__(self):
# #         return value_with_error_repr(self.value, self.SD)
# #
# #     @property
# #     def sample_length(self):
# #         return len(self.values)
# #
# #     @property
# #     def CI95(self) -> CI_95:
# #         return CI_95.CreateFromVector(self.values)
# #
# #     def get_CI(self, level: float) -> I_CI:
# #         return CI_any.CreateFromVector(self.values, level=level)
# #
# #     def compressed_copy(self):
# #         return ImplStudentValueWithError(value=self.value, SD=self.SD, N=self.N)
# #
# #
#
# #
# # class ImplValueWithErrorCI(BaseModel):
# #     """An extension to the ValueWithError that also remembers a single CI."""
# #
# #     obj: Union[
# #         ImplValueWithError, ImplValueWithErrorN, ImplValueVec, ImplValueWithoutError
# #     ]
# #     CI: Union[CI_95, CI_any]
# #
# #     def __repr__(self):
# #         return f"{repr(self.obj)} {repr(self.CI)}"
# #
# #     def get_CI(self, level: float) -> CI_any | CI_95:
# #         if level == self.CI.level:
# #             return self.CI
# #         else:
# #             raise ValueError("Cannot get CI with different level than the one stored")
# #
# #     @property
# #     def CI95(self) -> CI_95:
# #         return self.get_CI(0.95)
# #
# #     @property
# #     def value(self) -> float:
# #         return self.obj.value
# #
# #     @property
# #     def SE(self) -> Optional[float]:
# #         return self.obj.SE
# #
# #     @property
# #     def SD(self) -> Optional[float]:
# #         return self.obj.SD
# #
# #     @property
# #     def N(self) -> Optional[int | float]:
# #         return self.obj.N
# #
# #     def stripCI(self) -> IValueWithError:
# #         return self.obj
# #
# #     def compressed_copy(self):
# #         impl = self.obj.compressed_copy()
# #         return ImplValueWithErrorCI(obj=impl, CI=self.CI)
