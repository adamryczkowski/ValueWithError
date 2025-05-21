# from pydantic import BaseModel
#
#
# class ValuesWithError(BaseModel):
#     """A class that represents a list of values with uniform error display precision of values, SE and confidence intervals."""
#
#     impl: list[ImplValueVec]
#     cis: dict[float, CI_any | CI_95] = {}
#
#     @property
#     def value(self) -> float:
#         return self.impl.value
#
#     @property
#     def SD(self) -> Optional[float]:
#         return self.impl.SD
#
#     @property
#     def SE(self) -> Optional[float]:
#         if self.N == 0:
#             return None
#         if self.N <= 1:
#             return 0.0
#         return self.impl.SD / np.sqrt(self.N)
