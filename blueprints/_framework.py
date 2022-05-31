from inspect import isclass
from typing import Any, Dict, Optional, TYPE_CHECKING, Type, List, TypeVar

from flask import Blueprint

from utils import Framework
from utils.typing import type_compare

if TYPE_CHECKING:
    from .app import App

AppType = TypeVar('AppType', bound='App')
SchemeType = TypeVar('SchemeType', bound='Scheme')


class Scheme(Blueprint, Framework):
    app: Optional[AppType] = None
    children: Optional[List[Type[SchemeType]]] = None
    url_prefix: str = None
    options: dict[str, Any] = {}

    def __init__(self, app: AppType, /, *args, children: Optional[List[Type[SchemeType]]] = None, **kwargs):
        self.app = app
        self.children = children

        if not self.name:
            self.name = args[0]
        if not self.import_name:
            self.name = args[1]

        for k in kwargs:
            self.options[k] = kwargs[k]
            if k == 'url_prefix':
                self.url_prefix = kwargs[k]

        super().__init__(
            self.name,
            self.import_name,
            **self.options
        )

    def __init_subclass__(
            cls,
            name: str = None,
            module: str = None,
            url_prefix: str = None,
            **kwargs
    ) -> None:
        cls.name = name
        cls.import_name = module
        cls.url_prefix = url_prefix
        cls.options = kwargs
        cls.options['url_prefix'] = url_prefix

    def __post_init__(self, *args, **kwargs) -> None:
        self._register_routes()

        if self.children is not None:
            for child in self.children:
                setattr(self.app, child.name, child(self))
                print(getattr(self.app, child.name))

        self.app.register_blueprint(self, url_prefix=self.url_prefix)

    def _register_routes(self) -> None:
        cls: Type[Scheme] = self.__class__
        for attr in cls.__dict__.values():
            if isclass(attr) and issubclass(attr, Route):
                attr(self)


class Route(Framework):
    app: Optional[AppType]
    endpoint: str
    blueprint: Scheme
    route: str
    options: Dict[str, Any] = {}

    def __init__(self, blueprint: Scheme, route: str = None, endpoint: str = None, **kwargs) -> None:
        self.app = blueprint.app
        self.blueprint = blueprint
        if route:
            self.route = route
        if endpoint:
            self.endpoint = endpoint
        for k in kwargs:
            self.options[k] = kwargs[k]

    def __init_subclass__(
            cls,
            route: str = None,
            endpoint: str = None,
            **kwargs
    ) -> None:
        cls.route = route
        cls.endpoint = endpoint
        cls.options = kwargs

    def __post_init__(self, *args, **kwargs) -> None:
        # print(self.route, self.endpoint)
        self.blueprint.add_url_rule(self.route, self.endpoint, self.callback, **self.options)

    def callback(self, *args, **kwargs) -> Any:
        raise NotImplementedError()
