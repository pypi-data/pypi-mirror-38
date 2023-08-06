from functools import reduce
from infix import make_infix


def funcall(f, *args):
    return f(*args)


def unit(x):
    """The identity function.  Returns whatever argument it's called with."""
    return x


def flip(f):
    """
    Return a function that reverses the arguments it's called with.

    :param f: A function that takes exactly two arguments
    :Example:

       >>> exp = lambda x, y: x ** y
       >>> flip_exp = flip(exp)
       >>> exp(2, 3)
       8
       >>> flip_exp(2, 3)
       9
    """
    return lambda x, y: f(y, x)


@make_infix('or')
def compose(*fs):
    """
    Return a function that is the composition of the functions in ``fs``.
    All functions in ``fs`` must take a single argument.

    Adapted from this StackOverflow answer:
    https://stackoverflow.com/a/34713317

    :Example:

       >>> compose(f, g)(x) == f(g(x))
    """
    return lambda x: reduce(flip(funcall), reversed(fs), x)


cp = compose
