## ValueWithError Python library

This library provides a class for storing values with errors and nicely printing them. It also facilitates working with confidence intervals (CI).

### Usage

```python
from ValueWithError import value_with_error, from_samples

# Create a value with standard error
a = value_with_error(value=1.0, error=0.1)
print(a)
# Prints: 1.00 ± 0.10
print(a.CI95)
# Prints: CI_95%: (0.80, 1.20)

# Create with number of samples for student-t distribution
a = value_with_error(value=1.0, error=0.1, n_samples=5)
print(a.CI95)
# Prints: CI_95%: (0.72, 1.28) - a bigger interval because of the smaller sample size

# Create from array of observations/samples
import numpy as np

measurements = np.random.normal(123456, 10, 100)
b = from_samples(measurements)

print(b)
# Prints: 123456 ± 11
print(b.CI95)
# Prints: CI_95%: (123436, 123476)
```

### Working with Confidence Intervals

The library provides easy access to confidence intervals:

```python
from ValueWithError import from_samples
import numpy as np

# Create a value from sample measurements
measurements = np.random.normal(100, 5, 30)
result = from_samples(measurements)

# Get the 95% confidence interval (default)
ci_95 = result.CI95
print(ci_95)
# Prints: CI_95%: (98.2, 101.8)

# Get a custom confidence interval
ci_99 = result.get_CI(0.99)
print(ci_99)
# Prints: CI_99%: (97.1, 102.9)
```

### Memory-Efficient Processing

For large datasets, you can use the streaming interface:

```python
from ValueWithError import from_stream
import numpy as np

def random_generator(mean, std, size):
    for i in range(size):
        yield np.random.normal(mean, std)

# Process values without storing them all in memory
result = from_stream(random_generator(123456, 10, 10000))
print(result)
# Prints: 123456.0 ± 1.1
```

### From Samples to Student Estimate

When working with sample data, you can get a student estimate for more accurate confidence intervals:

```python
from ValueWithError import from_samples
import numpy as np

# Generate some sample data
measurements = np.random.normal(100, 5, 20)

# Create a ValueWithError from samples
sample_result = from_samples(measurements)
print(sample_result)
# Prints: 100.2 ± 5.1

# Get student estimate for the mean
mean_estimate = sample_result.student_estimate()
print(mean_estimate)
# Prints: 100.2 ± 1.1

# Compare confidence intervals
print(sample_result.CI95)  # Based on sample distribution
# Prints: CI_95%: (90.2, 110.2)

print(mean_estimate.CI95)  # Based on student-t distribution
# Prints: CI_95%: (97.9, 102.5)
```

### Edge Cases

ValueWithError handles edge cases gracefully:

```python
from ValueWithError import value_with_error
import numpy as np

# Value without error
a = value_with_error(1.0)
print(a)
# Prints: 1.00

# NaN and Inf values
a = value_with_error(np.nan, 0.1)
print(a)
# Prints: NaN

b = value_with_error(np.inf, 0.1)
print(b)
# Prints: ∞
```

### Customizing Output

You can customize how values are displayed:

```python
from ValueWithError import value_with_error, ValueWithErrorRepresentationConfig

# Create a custom configuration
config = ValueWithErrorRepresentationConfig(
    significant_digit_se=3,  # Show 3 significant digits for SE
    pad_raw_value_with_zeros=True,  # Pad with zeros
)

a = value_with_error(1.0, 0.1)
print(a.pretty_repr(config))
# Prints: 1.000 ± 0.100
```
