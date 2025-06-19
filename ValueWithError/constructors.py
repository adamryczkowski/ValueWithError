from typing import Iterator

import numpy as np

from .ImplNormalValueWithError import ImplNormalValueWithError
from .ImplSampleValueWithError import ImplSampleValueWithError
from .ImplStudentValueWithError import ImplStudentValueWithError
from .ImplValueWithoutError import ImplValueWithoutError
from .ValueWithError import ValueWithError


def make_ValueWithError(
    mean: float,
    SE: float | None = None,
    N: int | float | None = None,
) -> ValueWithError:
    if SE is None:
        assert N is None
        return ValueWithError(obj=ImplValueWithoutError(value=mean))
    else:
        if N is None:
            return ValueWithError(obj=ImplNormalValueWithError(value=mean, SE=SE))
        else:
            return ValueWithError(obj=ImplStudentValueWithError(value=mean, SE=SE, N=N))


def make_ValueWithError_from_vector(vector: np.ndarray) -> ValueWithError:
    return ValueWithError(obj=ImplSampleValueWithError(sample=vector))


def make_ValueWithError_from_generator(
    generator: Iterator[float] | np.ndarray,
    N: int | None = None,
) -> ValueWithError:
    """
    Creates a ValueWithError from a generator using the inline method.
    :param generator: A generator that returns a float on each iteration.
    :param N: The number of iterations to run the generator. Otherwise, we iterate until the generator stops.
    :return: the ValueWithError
    """
    sum = 0.0
    sumsq = 0.0
    count = 0
    for value in generator:
        sum += value
        sumsq += value * value
        count += 1
        if N is not None and count >= N:
            break

    if count == 0:
        raise ValueError("Cannot create ValueWithError from empty generator")

    mean = sum / count
    SD = np.sqrt(sumsq / count - mean * mean)
    ans = make_ValueWithError(mean=float(mean), SE=float(SD) / np.sqrt(count), N=count)
    assert isinstance(ans, ImplSampleValueWithError)
    return ValueWithError(obj=ans)


def fromJSON(json: dict) -> ValueWithError:
    return ValueWithError.model_validate(json)


def make_ImplValueWithError(
    mean: float,
    SE: float | None = None,
    N: int | float | None = None,
) -> ImplNormalValueWithError | ImplStudentValueWithError | ImplValueWithoutError:
    """
    Creates an implementation object directly without requiring the user to interact with private classes.
    :param mean: The mean value.
    :param SE: The standard error (optional).
    :param N: The number of samples (optional).
    :return: An implementation object.
    """
    if SE is None:
        assert N is None
        return ImplValueWithoutError(value=mean)
    else:
        if N is None:
            return ImplNormalValueWithError(value=mean, SE=SE)
        else:
            return ImplStudentValueWithError(value=mean, SE=SE, N=N)


def value_with_error(
    value: float,
    error: float | None = None,
    n_samples: int | float | None = None,
) -> ValueWithError:
    """
    Creates a ValueWithError object with a value and its associated error.

    Args:
        value: The measured or calculated value
        error: The standard error (SE)
        n_samples: Number of samples used (for student-t distribution)

    Returns:
        ValueWithError object
    """
    return make_ValueWithError(mean=value, SE=error, N=n_samples)


def from_samples(samples: np.ndarray) -> ValueWithError:
    """
    Creates a ValueWithError object from a vector of observations.

    Args:
        samples: Array of measurements or samples

    Returns:
        ValueWithError object with mean, SE and CIs calculated from samples
    """
    return make_ValueWithError_from_vector(samples)


def from_stream(
    generator: Iterator[float],
    max_samples: int | None = None,
) -> ValueWithError:
    """
    Creates a ValueWithError object from a stream of values without storing all samples.

    Args:
        generator: Iterator yielding float values
        max_samples: Maximum number of samples to process

    Returns:
        ValueWithError object
    """
    return make_ValueWithError_from_generator(generator, max_samples)
