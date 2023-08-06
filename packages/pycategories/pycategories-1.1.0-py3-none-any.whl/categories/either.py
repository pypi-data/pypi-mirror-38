from categories import applicative, functor, monad


class Either:
    _RIGHT_TYPE = 'Right'
    _LEFT_TYPE = 'Left'

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
    def left(cls, value):
        return cls(cls._LEFT_TYPE, value)

    @classmethod
    def right(cls, value):
        return cls(cls._RIGHT_TYPE, value)


Left = Either.left
Right = Either.right


def _fmap(f, x):
    if x.match(Right):
        return Right(f(x.value))
    else:
        return x


def _apply(f, x):
    if f.match(Right) and x.match(Right):
        return Right(f.value(x.value))
    elif f.match(Left):
        return f
    elif x.match(Left):
        return x


def _bind(m, f):
    """
    (>>=) :: Monad m => m a -> (a -> m b) -> m b
    """
    if m.match(Right):
        return f(m.value)
    else:
        return m


functor.instance(Either, _fmap)
applicative.instance(Either, Right, _apply)
monad.instance(Either, Right, _bind)
