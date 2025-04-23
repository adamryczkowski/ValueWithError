import ast
from typing import Annotated

import numpy as np
from pydantic import BeforeValidator, PlainSerializer


def nd_array_before_validator(x):
    # custom before validation logic
    if isinstance(x, str):
        x_list = ast.literal_eval(x)
        x = np.array(x_list)
    if isinstance(x, list):
        x = np.array(x)
    return x


def nd_array_serializer(x):
    # custom serialization logic
    return x.tolist()


NDArraySerializer = Annotated[
    np.ndarray,
    BeforeValidator(nd_array_before_validator),
    PlainSerializer(nd_array_serializer, return_type=list),
]
