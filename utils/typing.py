from inspect import isclass
from typing import TypeVar, Any


def _dive(origin: Any, target: str) -> bool:
    if target == origin.__name__:
        return True

    if len(origin.__bases__) > 0:
        for base in origin.__bases__:
            if not base == origin:
                if _dive(base, target):
                    return True

    return False


def type_compare(type_var: TypeVar, other: Any, _overhead: Any = None) -> bool:
    other = type(other)
    if not isclass(other):
        return NotImplemented

    bound = type_var.__bound__
    if bound:
        arg = bound.__forward_arg__
        if arg:
            return _dive(other, arg)

    return False
