from categories import applicative, functor, mappend
from categories import monad, monoid
from categories import semigroup, sappend


class Maybe:
    _JUST_TYPE = 'Just'
    _NOTHING_TYPE = 'Nothing'

    def __init__(self, type, value=None):
        self.type = type
        if self.type == self._JUST_TYPE:
            self.value = value

    def __repr__(self):
        return ('Nothing' if self.type == self._NOTHING_TYPE else
                'Just({})'.format(repr(self.value)))

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return (self.type == other.type and
                    self.__dict__ == other.__dict__)
        else:
            return False

    def match(self, constructor):
        if self.type == self._NOTHING_TYPE:
            return constructor == self.nothing
        else:
            return constructor == self.just

    @classmethod
    def just(cls, value):
        return cls(cls._JUST_TYPE, value)

    @classmethod
    def nothing(cls):
        return cls(cls._NOTHING_TYPE)


Just = Maybe.just
Nothing = Maybe.nothing


def _mappend(a, b):
    if a == Nothing():
        return b
    elif b == Nothing():
        return a
    else:
        return Just(mappend(a.value, b.value))


def _sappend(a, b):
    if a.match(Nothing):
        return b
    elif b.match(Nothing):
        return a
    else:
        return Just(sappend(a.value, b.value))


def _fmap(f, x):
    return Just(f(x.value)) if x.match(Just) else Nothing()


def _apply(f, x):
    if f.match(Just) and x.match(Just):
        return Just(f.value(x.value))
    else:
        return Nothing()


def _bind(m, f):
    if m.match(Nothing):
        return Nothing()
    else:
        return f(m.value)


functor.instance(Maybe, _fmap)
semigroup.instance(Maybe, _sappend)
monoid.instance(Maybe, lambda: Nothing(), _mappend)
applicative.instance(Maybe, Just, _apply)
monad.instance(Maybe, Just, _bind)
