## ValueWithError Python library

This library provides a class for storing values with errors and nicely printing them. It also facilitates working with CI (confidence/credible intervals).

### Usage

```python
from ValueWithError import ValueWithError, ValueWithErrorVec

a = ValueWithError(1.0, 0.1)
print(a) 
# Prints: 1.00 ± 0.10
print(a.get_CI95()) # 95% confidence interval calculated assuming normal distribution. 
# Prints: CI_95%: (0.80, 1.20)

a = ValueWithError(1.0, 0.1, N = 5) # N is the number of samples used to calculate the value. It is used by the CI calculation.
print(a.get_CI95())
# Prints: CI_95%: (0.72, 1.28) - a bigger interval because of the smaller N

import numpy as np
vec = np.random.normal(123456, 10, 100)
b = ValueWithErrorVec(vec)

print(b)
# Prints: 123456 ± 10
print(b.get_CI95())
# Prints: CI_95%: (123441, 123475)
```

`ValueWithErrorVec` is a class that calculates the value with error of a vector of values and stores that vector for potential later use. Standard error can be defined in two ways: 

* Standard deviation of the vector (the default)
* Standard error of the mean of the vector (if `estimate_mean=True` is passed to the constructor)

Confidence intervals for the ValueWithErrorVec are calculated using percentiles. 

```python
import numpy as np
from ValueWithError import ValueWithErrorVec
vec = np.random.normal(123456, 10, 100)
b = ValueWithErrorVec(vec, estimate_mean=True)

print(b)
# Prints: 123457.59 ± 0.95
print(b.get_CI95())
# Prints: CI_95%: (123437, 123475)
print(b.get_CI(0.995))
# Prints: CI_99.5%: (123428, 123441)

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
print(a.get_CI95())
# Prints: CI_95%: (1.0, 1.0)
```

It also handles NaN and Inf values:

```python
from ValueWithError import ValueWithError
import numpy as np
a = ValueWithError(np.nan, 0.1)
print(a)
# Prints: NaN
print(a.get_CI95())
# Prints: CI_95%: (NaN, NaN)
b = ValueWithError(np.inf, 0.1)
print(b)
# Prints: ∞
print(b.get_CI95())
# Prints: CI_95%: (∞, ∞)
```

If one does not want to print the error, it can be suppressed:

```python
from ValueWithError import ValueWithError
a = ValueWithError(1.0, None)
print(a)
# Prints: 1.0
a.get_CI95() is None 
# Prints: True
```

By default, all the values are rounded to two significant digits. This default cannot be changed for the ValueWithError class, but it can be customized by calling the `value_with_error_repr` function directly:

```python
from ValueWithError import value_with_error_repr, CI_repr

print(value_with_error_repr(1.0, 0.1, significant_digit_se=3))
# Prints: 1.000 ± 0.100
print(CI_repr(0.123456789, 0.1987654321, significant_digit=3))
# Prints: (0.1235, 0.1988)
```

#### ValueWithErrorCI

Internally ValueWithError stores the value, the error and optionally N - the number of samples used to calculate this statistic. ValueWithErrorCI additionally stores a single confidence interval. It is useful when one wants to store not only a value ± error, but also a single CI inteerval, e.g. when the distribution is not really normal. 

If one does not care about the memory footprint, the ValueWithErrorVec should be used instead, as it stores the whole vector and can calculate any statistic on demand, including percentile CI.

```python
from ValueWithError import ValueWithErrorCI
a = ValueWithErrorCI(1.0, 0.1, 0.9, 1.1)
print(a)
# Prints: "1.00 ± 0.10 CI_95%: (0.90, 1.10)"

b = ValueWithErrorCI(1.0, 0.1, 0.9, 1.1, ci_level=0.99)
print(b)
# Prints: "1.00 ± 0.10 CI_99%: (0.90, 1.10)"
```
