from functools import reduce
from infix import make_infix

from categories import instances


__instances = {}
get_instance = instances.make_getter(__instances, 'Semigroup')
_add_instance = instances.make_adder(__instances)
undefine_instance = instances.make_undefiner(__instances)


class Semigroup:
    def __init__(self, sappend):
        self.sappend = sappend


def instance(type, sappend):
    instance = Semigroup(sappend)
    _add_instance(type, instance)
    return instance


@make_infix('or')
def sappend(*xs):
    instance = get_instance(type(xs[0]))
    return reduce(instance.sappend, xs)


sp = sappend


def associativity_law(x, y, z):
    """
    (x <> y) <> z = x <> (y <> z)
      where (<>) = sappend
    """
    return sappend(sappend(x, y), z) == sappend(x, sappend(y, z))
