from abc import ABC, abstractmethod
from typing import Any, Callable


class ICommand(ABC):
    @abstractmethod
    def __call__(self) -> None:
        ...


class IResolveDependencyStrategy(ABC):
    @abstractmethod
    def __call__(self, *args: Any) -> Any:
        ...


class IDependenciesContainer(ABC):
    @abstractmethod
    def __init__(self, not_found_strategy: Callable):
        ...

    @abstractmethod
    def __getitem__(self, key: str) -> IResolveDependencyStrategy:
        ...

    @abstractmethod
    def __setitem__(self, key: str, strategy: IResolveDependencyStrategy):
        ...
