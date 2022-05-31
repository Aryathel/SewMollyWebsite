from typing import Any


class PostInit(type):
    def __call__(cls, *args, **kwargs) -> Any:
        obj = type.__call__(cls, *args, **kwargs)
        if hasattr(obj, '__post_init__'):
            obj.__post_init__(*args, **kwargs)
        return obj


class Framework(object, metaclass=PostInit):
    def __post_init__(self, *args, **kwargs) -> None:
        pass
