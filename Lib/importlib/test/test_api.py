import unittest
import importlib
from . import support


class ImportModuleTests(unittest.TestCase):

    """Test importlib.import_module."""

    def test_module_import(self):
        # Test importing a top-level module.
        with support.mock_modules('top_level') as mock:
            with support.import_state(meta_path=[mock]):
                module = importlib.import_module('top_level')
                self.assertEqual(module.__name__, 'top_level')

    def test_absolute_package_import(self):
        # Test importing a module from a package with an absolute name.
        pkg_name = 'pkg'
        pkg_long_name = '{0}.__init__'.format(pkg_name)
        name = '{0}.mod'.format(pkg_name)
        with support.mock_modules(pkg_long_name, name) as mock:
            with support.import_state(meta_path=[mock]):
                module = importlib.import_module(name)
                self.assertEqual(module.__name__, name)

    def test_relative_package_import(self):
        # Test importing a module from a package through a relatve import.
        pkg_name = 'pkg'
        pkg_long_name = '{0}.__init__'.format(pkg_name)
        module_name = 'mod'
        absolute_name = '{0}.{1}'.format(pkg_name, module_name)
        relative_name = '.{0}'.format(module_name)
        with support.mock_modules(pkg_long_name, absolute_name) as mock:
            with support.import_state(meta_path=[mock]):
                module = importlib.import_module(relative_name, pkg_name)
                self.assertEqual(module.__name__, absolute_name)

    def test_absolute_import_with_package(self):
        # Test importing a module from a package with an absolute name with
        # the 'package' argument given.
        pkg_name = 'pkg'
        pkg_long_name = '{0}.__init__'.format(pkg_name)
        name = '{0}.mod'.format(pkg_name)
        with support.mock_modules(pkg_long_name, name) as mock:
            with support.import_state(meta_path=[mock]):
                module = importlib.import_module(name, pkg_name)
                self.assertEqual(module.__name__, name)

    def test_relative_import_wo_package(self):
        # Relative imports cannot happen without the 'package' argument being
        # set.
        self.assertRaises(TypeError, importlib.import_module, '.support')


def test_main():
    from test.support import run_unittest
    run_unittest(ImportModuleTests)


if __name__ == '__main__':
    test_main()
