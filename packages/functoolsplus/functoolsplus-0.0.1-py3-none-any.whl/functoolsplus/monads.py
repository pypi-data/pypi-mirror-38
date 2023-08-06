import abc
from collections.abc import Iterable

from functoolsplus.utils.implementations import get_impl, provide_impl_for


class Monad(abc.ABC):

    @abc.abstractmethod
    def __flatmap__(self, func):
        return NotImplemented

    @staticmethod
    @abc.abstractmethod
    def __unit__(cls, value):
        return NotImplemented


def flatmap(func, obj):
    if isinstance(obj, Monad):
        result = obj.__flatmap__(func)
        if result is not NotImplemented:
            return result

    obj_type = type(obj)
    try:
        impl_cls = get_impl(Monad, obj_type)
    except TypeError:
        pass
    else:
        result = impl_cls.__flatmap__(obj, func)
        if result is not NotImplemented:
            return result

    raise TypeError(f'{obj_type!r} does not support flatmap interface')


def unit(cls, value):
    if issubclass(cls, Monad):
        result = cls.__unit__(cls, value)
        if result is not NotImplemented:
            return result

    try:
        impl_cls = get_impl(Monad, cls)
    except TypeError:
        pass
    else:
        result = impl_cls.__unit__(cls, value)
        if result is not NotImplemented:
            return result

    raise TypeError(f'{cls!r} does not support unit interface')


@provide_impl_for(Monad, Iterable)
class _IterableMonadImpl(Monad, Iterable):

    def __flatmap__(self, func):
        cls = type(self)
        return cls(_flatmap_iter(self, func))

    @staticmethod
    def __unit__(cls, value):
        return cls([value])


def _flatmap_iter(obj, func):
    for item in obj:
        for result_item in func(item):
            yield result_item
