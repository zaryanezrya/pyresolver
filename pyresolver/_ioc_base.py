from typing import Any, Callable

from .interfaces import IDependenciesContainer, IResolveDependencyStrategy, ICommand
from .exceptions import ResolveDependencyException


class IOCBaseContainer(IDependenciesContainer):
    def __init__(self, not_found_strategy: Callable):
        self.__not_found_strategy = not_found_strategy
        self.__store = {}

        self.__store["IoC.Resolve"] = IOCBaseResolveResolver(self)
        self.__store["IoC.Register"] = IOCBaseRegisterCommandResolver(self)
        self.__store["IoC.BaseContainer"] = lambda: self

    def __getitem__(self, key: str) -> IResolveDependencyStrategy:
        try:
            return self.__store[key]
        except KeyError:
            return self.__not_found_strategy(key)
        except ResolveDependencyException as e:
            raise e

    def __setitem__(self, key: str, strategy: IResolveDependencyStrategy):
        self.__store[key] = strategy


class IOCBaseResolveResolver(IResolveDependencyStrategy):
    def __init__(self, container: IDependenciesContainer):
        self.__container = container

    def __call__(self, *args: Any) -> IResolveDependencyStrategy:
        key = args[0]
        return self.__container[key](*args[1:])


class IOCBaseRegisterCommandResolver(IResolveDependencyStrategy):
    def __init__(self, container: IDependenciesContainer):
        self.__container = container

    def __call__(self, *args: Any) -> IResolveDependencyStrategy:
        try:
            key = args[0]
            strategy = args[1]
            # TODO: Throw ResolveDependencyException "agrs[0] must have type String, args[1] must have IResolveDependencyStrategy"
            return IOCBaseRegisterCommand(self.__container, key, strategy)
        except IndexError:
            raise ResolveDependencyException(
                "IoC.Register requires two args: key(str) and strategy(IResolveDependencyStrategy)"
            )


class IOCBaseRegisterCommand(ICommand):
    def __init__(
        self,
        scope: IDependenciesContainer,
        key: str,
        strategy: IResolveDependencyStrategy,
    ):
        self.container = scope
        self.key = key
        self.strategy = strategy

    def __call__(self) -> None:
        self.container[self.key] = self.strategy
