import unittest

from pyresolver import resolve, IResolveDependencyStrategy, ResolveDependencyException


class TestBase(unittest.TestCase):
    def test_resolve_success(self):
        resolve('IoC.Register', 'App.dummy', DummySum())()
        self.assertEqual(12, resolve('App.dummy', 1, 11))

    def test_resolve_fail(self):
        self.assertRaises(ResolveDependencyException, resolve, 'MISSING_KEY')

    def test_execute_in_scope(self):
        scope = resolve('Scopes.New')
        with resolve('Scopes.executeInScope', scope):
            resolve('IoC.Register', 'App.dummy', DummySum())()
            self.assertEqual(12, resolve('App.dummy', 1, 11))

        self.assertRaises(
            ResolveDependencyException,
            resolve, ('App.dummy', 1, 11)
        )

    def test_execute_in_new_scope(self):
        resolve('IoC.Register', 'App.dummy', DummySum())()

        with resolve('Scopes.executeInNewScope'):
            resolve('IoC.Register', 'App.dummy', DummySub())()
            self.assertEqual(-10, resolve('App.dummy', 1, 11))

        self.assertEqual(12, resolve('App.dummy', 1, 11))


class DummySum(IResolveDependencyStrategy):
    def __call__(self, *args):
        return args[0] + args[1]


class DummySub(IResolveDependencyStrategy):
    def __call__(self, *args):
        return args[0] - args[1]
