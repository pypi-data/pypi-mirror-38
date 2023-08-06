from categories import applicative, functor, semigroup
from categories import sappend


class Validation:
    _SUCCESS_TYPE = 'Success'
    _FAILURE_TYPE = 'Failure'

    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        return '{}({})'.format(self.type, repr(self.value))

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return (self.type == other.type and
                    self.__dict__ == other.__dict__)
        else:
            return False

    def match(self, constructor):
        return constructor(self.value).type == self.type

    @classmethod
    def failure(cls, value):
        return cls(cls._FAILURE_TYPE, value)

    @classmethod
    def success(cls, value):
        return cls(cls._SUCCESS_TYPE, value)


Failure = Validation.failure
Success = Validation.success


def _sappend(a, b):
    if a.type == b.type:
        return Validation(a.type, sappend(a.value, b.value))
    elif a.match(Failure):
        return a
    else:
        return b


def _fmap(f, x):
    if x.match(Failure):
        return x
    else:
        return Success(f(x.value))


def _apply(f, x):
    if f.match(Success) and x.match(Success):
        return Success(f.value(x.value))
    elif f.match(Failure):
        return f
    else:
        return x


semigroup.instance(Validation, _sappend)
functor.instance(Validation, _fmap)
applicative.instance(Validation, Success, _apply)
