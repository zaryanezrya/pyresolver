import unittest

from pyresolver import resolve
from pyresolver.exception import ResolveDependencyException


class TestBase(unittest.TestCase):
    def test_ioc_resolve_missing_key_fail(self):
        self.assertRaises(ResolveDependencyException, resolve, 'MISSING_KEY')

    def test_ioc_register_and_ioc_resolve_success(self):
        resolve('IoC.Register', 'App.add', lambda *args: args[0] + args[1])()
        self.assertEqual(12, resolve('App.add', 1, 11))

    def test_ioc_register_no_args_fail(self):
        self.assertRaises(ResolveDependencyException, resolve, 'IoC.Register')

    def test_ioc_register_bad_arg_fail(self):
        resolve('IoC.Register', 'App.dummy', 1)()
        self.assertRaises(ResolveDependencyException, resolve, 'App.dummy')
