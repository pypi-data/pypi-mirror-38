import abc
from collections.abc import Iterable

from functoolsplus.utils.implementations import get_impl, provide_impl_for


class Functor(abc.ABC):

    @abc.abstractmethod
    def __map__(self, func):
        return NotImplemented

    @classmethod
    def __subclasshook__(cls, C):
        if cls is Functor:
            if any(
                    '__map__' in test_cls.__dict__
                    for test_cls in C.__mro__):
                return True
        return NotImplemented


def map(func, obj):

    if isinstance(obj, Functor):
        result = obj.__map__(func)
        if result is not NotImplemented:
            return result

    try:
        impl_cls = get_impl(Functor, type(obj))
    except TypeError:
        pass
    else:
        result = impl_cls.__map__(obj, func)
        if result is not NotImplemented:
            return result

    obj_type = type(obj)
    raise TypeError(f'{obj_type!r} does not support map interface')


@provide_impl_for(Functor, Iterable)
class _IterableFunctorImpl(Functor, Iterable):

    def __map__(self, func):
        cls = self.__class__
        return cls(func(item) for item in self)
