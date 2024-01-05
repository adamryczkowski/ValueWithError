## ValueWithError Python library

This library provides a class for storing values with errors and nicely printing them.

### Usage

```python
from ValueWithError import ValueWithError, ValueWithErrorVec

a = ValueWithError(1.0, 0.1)
print(a) 
# Prints: 1.00 ± 0.10

import numpy as np
vec = np.random.normal(123456, 10, 100)
b = ValueWithErrorVec(vec)

print(b)
# Prints: 123456 ± 10
```

`ValueWithErrorVec` is a class that calculates the value with error of a vector of values and stores that vector for potential later use. Standard error can be defined in two ways: 

* Standard deviation of the vector (the default)
* Standard error of the mean of the vector (if `estimate_mean=True` is passed to the constructor)

```python
import numpy as np
from ValueWithError import ValueWithErrorVec
vec = np.random.normal(123456, 10, 100)
b = ValueWithErrorVec(vec, estimate_mean=True)

print(b)
# Prints: 123457.59 ± 0.95
```

If one needs small memory footprint, there's an online version of the calculation that doesn't ever store the vector. At the moment this method is not faster than the vector version, but it's more memory efficient.

```python
import numpy as np
from timeit import timeit
from ValueWithError import ValueWithErrorVec, make_ValueWithError_from_generator

def random_generator(mean, std, size):
    for i in range(size):
        yield np.random.normal(mean, std)
        
method1 = lambda : ValueWithErrorVec([v for v in random_generator(123456, 10, 10000)], estimate_mean=True)
method2 = lambda : make_ValueWithError_from_generator(random_generator(123456, 10, 10000), estimate_mean=True)

print(timeit(method1, number=10))
# Prints: 0.17308157600928098
print(timeit(method2, number=10))
# Prints: 0.16921406201436184
```

### Edge cases

ValueWithError class is designed to handle edge cases gracefully. For example, if the error is zero, the value is printed without the error:

```python
from ValueWithError import ValueWithError
a = ValueWithError(1.0, 0.0)
print(a)
# Prints: 1.00
```

It also handles NaN and Inf values:

```python
from ValueWithError import ValueWithError
import numpy as np
a = ValueWithError(np.nan, 0.1)
print(a)
# Prints: NaN
b = ValueWithError(np.inf, 0.1)
print(b)
# Prints: ∞
```

If one does not want to print the error, it can be suppressed:

```python
from ValueWithError import ValueWithError
a = ValueWithError(1.0, None)
print(a)
# Prints: 1.0
```

By default all the values are rounded to two significant digits. This default cannot be changed for the ValueWithError class, but it can be customized by calling the `value_with_error_repr` function directly:

```python
from ValueWithError import value_with_error_repr
print(value_with_error_repr(1.0, 0.1, significant_digit_se=3))
# Prints: 1.000 ± 0.100
```
