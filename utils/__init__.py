from typing import Dict, Union

from .email import MailFactory as Mail
from .framework import Framework
from .auth import Google


def sort_nested_dict(data: Dict[str, Union[dict, str]]) -> Dict[str, Union[dict, str]]:
    for k, v in data.items():
        if type(v) == dict:
            data[k] = sort_nested_dict(v)
    return dict(sorted(data.items()))


__all__ = {
    "Mail",
    "Framework",
    "Google",
    "sort_nested_dict"
}
