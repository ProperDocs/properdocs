"""After this file is imported, all mkdocs.* imports get redirected to properdocs.* imports."""

import importlib.abc
import importlib.util
import sys


class _AliasLoader(importlib.abc.Loader):
    """Loads the module with the given name and replaces the passed spec's module."""

    def __init__(self, realname):
        self.realname = realname

    def create_module(self, spec):
        module = importlib.import_module(self.realname)
        sys.modules[spec.name] = module
        return module

    def exec_module(self, module):
        pass


class _AliasFinder:
    """When searching for any mkdocs.* module, find the corresponding properdocs.* module instead."""

    def find_spec(self, fullname, path, target=None):
        if fullname.startswith("mkdocs."):
            realname = "properdocs." + fullname.removeprefix("mkdocs.")
            spec = importlib.util.find_spec(realname)
            if spec is None:
                raise ImportError(f"No module named {realname!r}")
            return importlib.util.spec_from_loader(
                fullname,
                _AliasLoader(realname),
                is_package=spec.submodule_search_locations is not None,
            )
        return None


sys.meta_path.insert(0, _AliasFinder())
# Plus, handle the topmost module directly and without waiting for it to be requested.
sys.modules['mkdocs'] = sys.modules['properdocs']
