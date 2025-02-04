from ValueWithError import ValueWithError, make_ValueWithError
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


if __name__ == "__main__":
    test1()
