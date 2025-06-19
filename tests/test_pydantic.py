from ValueWithError import (
    ValueWithError,
    make_ValueWithError,
    make_ValueWithError_from_vector,
)
from pydantic import BaseModel
import numpy as np


# def test_basic():
#     obj = ImplValueWithoutError(value=10)
#     json = obj.model_dump_json(by_alias=True)
#     print(f"Serialized object {repr(obj)}: {json}")
#     obj2 = ImplValueWithoutError.model_validate_json(json)
#     assert repr(obj) == repr(obj2)


def test_api():
    v1 = make_ValueWithError(1.0)
    v2 = make_ValueWithError(1.0, SE=1)
    v3 = make_ValueWithError(1.0, SE=1, N=10)
    v4 = make_ValueWithError_from_vector(np.asarray([1.0, 2.0, 3.0]))

    s1 = v1.model_dump_json()
    o1 = ValueWithError.model_validate_json(s1)
    assert o1 == v1

    s2 = v2.model_dump_json()
    o2 = ValueWithError.model_validate_json(s2)
    assert o2 == v2

    s3 = v3.model_dump_json()
    o3 = ValueWithError.model_validate_json(s3)
    assert o3 == v3

    s4 = v4.model_dump_json()
    o4 = ValueWithError.model_validate_json(s4)
    assert str(o4) == str(v4)


def test1():
    class A(BaseModel):
        val: int | str
        dval: dict[str, int | str]
        verr: ValueWithError

    a = A(val=1, dval={"a": "a", "b": 2}, verr=make_ValueWithError(10, 1, 100))
    a = make_ValueWithError(10, 1, 100)
    json = a.model_dump_json(by_alias=True)

    print(f"Serialized object {repr(a)}: {json}")

    a2 = ValueWithError.model_validate_json(json)

    print(f"Testing if {repr(a)} == {repr(a2)}")
    assert repr(a) == repr(a2)


#
#
#
# def test2():
#     class ImplValErr(BaseModel):
#         val: int
#
#     class ImplVectErr(BaseModel):
#         vals: str
#
#     class ValErr(BaseModel):
#         impl2: ImplValErr | ImplVectErr
#
#     class VectErr(BaseModel):
#         impl: ImplVectErr
#
#     class MainEf(BaseModel):
#         one_dim_pars: list[ValErr | VectErr]
#
#     c = MainEf(one_dim_pars=[ValErr(impl2=ImplValErr(val=10))])
#     json = c.model_dump_json()
#     c2 = MainEf.model_validate_json(json)
#     assert c2 == c
#
#     c = MainEf(one_dim_pars=[VectErr(impl=ImplVectErr(vals="a"))])
#     json = c.model_dump_json()
#     c2 = MainEf.model_validate_json(json)
#     print(c2)
#     assert c2 == c
#
#
# # def test3():
# #     class StanResultMainEffects(BaseModel):
# #         one_dim_pars: list[
# #             ValueWithError | VectorOfValues
# #         ]  # Parameter name in format "par" or "par[10][2][3]"
# #
# #     result = StanResultMainEffects(one_dim_pars=[make_ValueWithError(10, 1, 100)])
# #     print(result)
# #     json = result.model_dump_json()
# #     result2 = StanResultMainEffects.model_validate_json(json)
# #     print(result2)
#
#
if __name__ == "__main__":
    test_api()
    test1()
    # test2()
    # test3()
