# Semigroup:
from categories.semigroup import sappend, sp

# Monoid:
from categories.monoid import mappend, mempty, mp

# Functor:
from categories.functor import fmap, fp

# Applicative:
from categories.applicative import ap, apply, pure

# Monad:
from categories.monad import bind, mreturn

# Set up default instances for some built-in types:
from categories import builtins
