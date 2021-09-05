from abc import ABC, abstractmethod
from typing import Any


class IResolveDependencyStrategy (ABC):
    @abstractmethod
    def __call__(self, *args: Any) -> Any: ...
