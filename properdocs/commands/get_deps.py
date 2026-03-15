# Copyright (c) 2023 Oleh Prypin <oleh@pryp.in>

from __future__ import annotations

import dataclasses
import datetime
import functools
import io
import logging
import os
import sys
import urllib.parse
from collections.abc import Collection, Mapping, Sequence
from typing import IO, Any, BinaryIO

import yaml

from properdocs.config.base import _open_config_file
from properdocs.utils import cache
from properdocs.utils import yaml as yaml_util

SafeLoader: type[yaml.SafeLoader | yaml.CSafeLoader]
try:
    from yaml import CSafeLoader as SafeLoader
except ImportError:
    from yaml import SafeLoader

log = logging.getLogger(__name__)


class YamlLoaderWithSuppressions(SafeLoader):  # type: ignore
    pass


# Prevent errors from trying to access external modules which may not be installed yet.
YamlLoaderWithSuppressions.add_constructor("!ENV", lambda loader, node: None)
YamlLoaderWithSuppressions.add_constructor("!relative", lambda loader, node: None)
YamlLoaderWithSuppressions.add_multi_constructor(
    "tag:yaml.org,2002:python/name:", lambda loader, suffix, node: None
)
YamlLoaderWithSuppressions.add_multi_constructor(
    "tag:yaml.org,2002:python/object/apply:", lambda loader, suffix, node: None
)


DEFAULT_PROJECTS_FILE = "https://raw.githubusercontent.com/properdocs/catalog/main/projects.yaml"

BUILTIN_PLUGINS = {"search"}
_BUILTIN_EXTENSIONS = [
    "abbr",
    "admonition",
    "attr_list",
    "codehilite",
    "def_list",
    "extra",
    "fenced_code",
    "footnotes",
    "md_in_html",
    "meta",
    "nl2br",
    "sane_lists",
    "smarty",
    "tables",
    "toc",
    "wikilinks",
    "legacy_attrs",
    "legacy_em",
]
BUILTIN_EXTENSIONS = {
    *_BUILTIN_EXTENSIONS,
    *(f"markdown.extensions.{e}" for e in _BUILTIN_EXTENSIONS),
}

_NotFound = ()


def _dig(cfg, keys: str):
    """
    Receives a string such as 'foo.bar' and returns `cfg['foo']['bar']`, or `_NotFound`.

    A list of single-item dicts gets converted to a flat dict. This is intended for `plugins` config.
    """
    key, _, rest = keys.partition(".")
    try:
        cfg = cfg[key]
    except (KeyError, TypeError):
        return _NotFound
    if isinstance(cfg, list):
        orig_cfg = cfg
        cfg = {}
        for item in reversed(orig_cfg):
            if isinstance(item, dict) and len(item) == 1:
                cfg.update(item)
            elif isinstance(item, str):
                cfg[item] = {}
    if not rest:
        return cfg
    return _dig(cfg, rest)


def _strings(obj) -> Sequence[str]:
    if isinstance(obj, str):
        return (obj,)
    else:
        return tuple(obj)


@functools.cache
def _entry_points(group: str) -> Mapping[str, Any]:
    if sys.version_info >= (3, 10):
        from importlib.metadata import entry_points
    else:
        from importlib_metadata import entry_points

    eps = {ep.name: ep for ep in entry_points(group=group)}
    log.debug(f"Available '{group}' entry points: {sorted(eps)}")
    return eps


@dataclasses.dataclass(frozen=True)
class _PluginKind:
    projects_key: str
    entry_points_key: str

    def __str__(self) -> str:
        return self.projects_key.rpartition("_")[-1]


def get_projects_file(path: str | None = None) -> BinaryIO:
    if path is None:
        path = DEFAULT_PROJECTS_FILE
    if urllib.parse.urlsplit(path).scheme in ("http", "https"):
        content = cache.download_and_cache_url(path, datetime.timedelta(days=1))
    else:
        with open(path, "rb") as f:
            content = f.read()
    return io.BytesIO(content)


def get_deps(
    config_file: IO | os.PathLike | str | None = None,
    projects_file: IO | None = None,
) -> Collection[str]:
    """
    Print PyPI package dependencies inferred from a properdocs.yml file based on a reverse mapping of known projects.

    Args:
        config_file: Non-default properdocs.yml file - content as a buffer, or path.
        projects_file: File/buffer that declares all known ProperDocs-related projects.
            The file is in YAML format and contains `projects: [{mkdocs_theme:, mkdocs_plugin:, markdown_extension:}]
    """
    if isinstance(config_file, (str, os.PathLike)):
        config_file = os.path.abspath(config_file)
    with _open_config_file(config_file) as opened_config_file:
        cfg = yaml_util.yaml_load(opened_config_file, loader=YamlLoaderWithSuppressions)
    if not isinstance(cfg, dict):
        raise ValueError(
            f"The configuration is invalid. Expected a key-value mapping but received {type(cfg)}"
        )

    packages_to_install = set()

    if all(c not in cfg for c in ("site_name", "theme", "plugins", "markdown_extensions")):
        log.warning(f"The file {config_file!r} doesn't seem to be a properdocs.yml config file")
    else:
        if _dig(cfg, "theme.locale") not in (_NotFound, "en"):
            packages_to_install.add("properdocs[i18n]")
        else:
            packages_to_install.add("properdocs")

    try:
        theme = cfg["theme"]["name"]
    except (KeyError, TypeError):
        theme = cfg.get("theme")
    themes = {theme} if theme else set()

    plugins = set(_strings(_dig(cfg, "plugins"))) - BUILTIN_PLUGINS
    extensions = set(_strings(_dig(cfg, "markdown_extensions"))) - BUILTIN_EXTENSIONS

    wanted_plugins = (
        (_PluginKind("properdocs_theme", "properdocs.themes"), themes),
        (_PluginKind("mkdocs_theme", "mkdocs.themes"), themes),
        (_PluginKind("properdocs_plugin", "properdocs.plugins"), plugins),
        (_PluginKind("mkdocs_plugin", "mkdocs.plugins"), plugins),
        (_PluginKind("markdown_extension", "markdown.extensions"), extensions),
    )
    for kind, wanted in (wanted_plugins[0], wanted_plugins[2], wanted_plugins[4]):
        log.debug(f"Wanted {kind}s: {sorted(wanted)}")

    if projects_file is None:
        projects_file = get_projects_file()
    with projects_file:
        projects = yaml.load(projects_file, Loader=SafeLoader)["projects"]

    for project in projects:
        for kind, wanted in wanted_plugins:
            available = _strings(project.get(kind.projects_key, ()))
            for entry_name in available:
                if (  # Also check theme-namespaced plugin names against the current theme.
                    "/" in entry_name
                    and theme is not None
                    and kind.projects_key in ("properdocs_plugin", "mkdocs_plugin")
                    and entry_name.startswith(f"{theme}/")
                    and entry_name[len(theme) + 1 :] in wanted
                    and entry_name not in wanted
                ):
                    entry_name = entry_name[len(theme) + 1 :]
                if entry_name in wanted:
                    if "pypi_id" in project:
                        install_name = project["pypi_id"]
                    elif "github_id" in project:
                        install_name = "git+https://github.com/{github_id}".format_map(project)
                    else:
                        log.error(
                            f"Can't find how to install {kind} '{entry_name}' although it was identified as {project}"
                        )
                        continue
                    packages_to_install.add(install_name)
                    for extra_key, extra_pkgs in project.get("extra_dependencies", {}).items():
                        if _dig(cfg, extra_key) is not _NotFound:
                            packages_to_install.update(_strings(extra_pkgs))

                    wanted.remove(entry_name)

    warnings: dict[str, str] = {}

    for kind, wanted in wanted_plugins:
        for entry_name in sorted(wanted):
            dist_name = None
            ep = _entry_points(kind.entry_points_key).get(entry_name)
            if ep is not None and ep.dist is not None:
                dist_name = ep.dist.name
            base_warning = (
                f"{str(kind).capitalize()} '{entry_name}' is not provided by any registered project"
            )
            if ep is not None:
                warning = base_warning + " but is installed locally"
                if dist_name:
                    warning += f" from '{dist_name}'"
                warnings[base_warning] = warning  # Always prefer the lesser warning
            else:
                warnings.setdefault(base_warning, base_warning)

    for warning in warnings.values():
        if " is installed " in warning:
            log.info(warning)
        else:
            log.warning(warning)

    return sorted(packages_to_install)
