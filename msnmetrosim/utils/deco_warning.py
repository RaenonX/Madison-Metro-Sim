"""Decorators to yield warnings under various circumstances."""
import functools
import warnings

__all__ = ("temporary_func",)


def temporary_func(func):
    """
    Decorator to yield warnings indicating that the function is for temporary use, and should be removed later.

    Example::

    >>> @temporary_func
    >>> def temp_func():
    >>>     pass
    """

    @functools.wraps(func)
    def new_func(*args, **kwargs):
        warnings.warn(f"Temporary function called: {func}.",
                      category=DeprecationWarning,
                      stacklevel=2)
        return func(*args, **kwargs)

    return new_func
