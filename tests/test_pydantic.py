from ValueWithError import VectorOfValues, ValueWithError, make_ValueWithError
from pydantic import BaseModel


def test1():
    class A(BaseModel):
        val: int | str
        dval: dict[str, int | str]
        verr: ValueWithError

    a = A(val=1, dval={"a": "a", "b": 2}, verr=make_ValueWithError(10, 1, 100))
    a = make_ValueWithError(10, 1, 100)
    json = a.model_dump_json()

    print(json)

    a2 = ValueWithError.model_validate_json(json)
    print(repr(a2))


def test2():
    class ImplValErr(BaseModel):
        val: int

    class ImplVectErr(BaseModel):
        vals: str

    class ValErr(BaseModel):
        impl2: ImplValErr | ImplVectErr

    class VectErr(BaseModel):
        impl: ImplVectErr

    class MainEf(BaseModel):
        one_dim_pars: list[ValErr | VectorOfValues]

    c = MainEf(one_dim_pars=[ValErr(impl2=ImplValErr(val=10))])
    # c = MainEf(one_dim_pars=[make_ValueWithError(10,1,100)])

    json = c.model_dump_json()

    c2 = MainEf.model_validate_json(json)
    print(c2)


def test3():
    class StanResultMainEffects(BaseModel):
        one_dim_pars: list[
            ValueWithError | VectorOfValues
        ]  # Parameter name in format "par" or "par[10][2][3]"

    result = StanResultMainEffects(one_dim_pars=[make_ValueWithError(10, 1, 100)])
    print(result)
    json = result.model_dump_json()
    result2 = StanResultMainEffects.model_validate_json(json)
    print(result2)


if __name__ == "__main__":
    # test1()
    # test2()
    test3()
