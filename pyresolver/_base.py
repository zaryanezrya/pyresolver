from typing import Any
import threading

from ._scope import IDependenciesScope, DependenciesScope
from ._strategy import IResolveDependencyStrategy
from ._command import ICommand
from ._exception import ResolveDependencyException


class NotFoundInRootScope:
    def __call__(self, key) -> Any:
        raise ResolveDependencyException(f'Dependency {key} is missing')


class ScopesThreadingLocalProvider:
    __tl_store = threading.local()
    __global_root_scope = DependenciesScope(NotFoundInRootScope())

    def __init__(self):
        root_scope = self.__global_root_scope

        root_scope['IoC.Register'] = RegisterCommandResolver()
        root_scope['Scopes.Root'] = lambda: root_scope
        root_scope['Scopes.New'] = NewScopeResolver()
        root_scope['Scopes.executeInScope'] = ExecuteInScopeResolver()
        root_scope['Scopes.executeInNewScope'] = ExecuteInNewScopeResolver()

        default_scope = DependenciesScope(FindInParentScope(root_scope))

        root_scope['Scopes.Default'] = lambda: default_scope
        self.__tl_store.current_scope = default_scope

    @property
    def current(self) -> IDependenciesScope:
        current_scope = getattr(self.__tl_store, 'current_scope', None)
        if not current_scope:
            self.__tl_store.current_scope = self.__global_root_scope
            self.__tl_store.current_scope = resolve('Scopes.Default')
        return self.__tl_store.current_scope

    @current.setter
    def current(self, scope: IDependenciesScope):
        self.__tl_store.current_scope = scope


class ExecuteInScopeContextManager:
    def __init__(self, scope):
        self.new_scope = scope

    def __enter__(self):
        self.old_scope = scopes.current
        scopes.current = self.new_scope

    def __exit__(self, *args):
        scopes.current = self.old_scope


class RegisterCommandResolver(IResolveDependencyStrategy):
    def __call__(self, *args: Any) -> ICommand:
        # TODO: Throw ResolveDependencyException "Agrs[0] must have type String, arg[1] must have ResolveDepenedencyStartagy<*>"
        key = args[0]
        command = args[1]
        return RegisterCommand(
            scopes.current,
            key,
            command
        )


class NewScopeResolver(IResolveDependencyStrategy):
    def __call__(self, *args: Any) -> IDependenciesScope:
        parent = None
        if args:
            parent = args[0]
        else:
            parent = scopes.current
        return DependenciesScope(FindInParentScope(parent))


class ExecuteInScopeResolver(IResolveDependencyStrategy):
    def __call__(self, scope: IDependenciesScope) -> ExecuteInScopeContextManager:
        return ExecuteInScopeContextManager(scope)


class ExecuteInNewScopeResolver(IResolveDependencyStrategy):
    def __call__(self) -> ExecuteInScopeContextManager:
        new_scope = resolve('Scopes.New')
        return resolve('Scopes.executeInScope', new_scope)


class RegisterCommand(ICommand):
    def __init__(self, scope: IDependenciesScope, key: str, strategy: IResolveDependencyStrategy):
        self.scope = scope
        self.key = key
        self.strategy = strategy

    def __call__(self) -> None:
        self.scope[self.key] = self.strategy


class FindInParentScope:
    def __init__(self, parent_scope: IDependenciesScope):
        self.parent = parent_scope

    def __call__(self, key) -> Any:
        return self.parent[key]


scopes = ScopesThreadingLocalProvider()


def resolve(key, *args):
    # TODO: exceptions
    # only ResolveDependencyException. info: scope, key
    return scopes.current[key](*args)
