from ValueWithError import ValueWithError, make_ValueWithError
from pydantic import BaseModel
from ValueWithError.ImplValueWithoutError import ImplValueWithoutError


def test_basie():
    obj = ImplValueWithoutError(value=10)
    json = obj.model_dump_json(by_alias=True)
    print(f"Serialized object {repr(obj)}: {json}")
    obj2 = ImplValueWithoutError.model_validate_json(json)
    assert repr(obj) == repr(obj2)


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
    test_basie()
    test1()
    # test2()
    # test3()
