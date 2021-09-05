from abc import ABC, abstractmethod
from typing import Callable
import threading


from ._strategy import IResolveDependencyStrategy
from ._exception import ResolveDependencyException


class IDependenciesScope(ABC):
    @abstractmethod
    def __init__(self, not_found_strategy: Callable): ...

    @abstractmethod
    def __getitem__(self, key: str) -> IResolveDependencyStrategy: ...

    @abstractmethod
    def __setitem__(self, key: str, strategy: IResolveDependencyStrategy): ...


class DependenciesScope(IDependenciesScope):
    def __init__(self, not_found_strategy: Callable):
        self.__lock = threading.Lock()
        self.__store = {}
        self.not_found_strategy = not_found_strategy

    def __getitem__(self, key: str) -> IResolveDependencyStrategy:
        try:
            with self.__lock:
                return self.__store[key]
        except KeyError:
            return self.not_found_strategy(key)
        except ResolveDependencyException as e:
            raise e

    def __setitem__(self, key: str, strategy: IResolveDependencyStrategy):
        with self.__lock:
            self.__store[key] = strategy
