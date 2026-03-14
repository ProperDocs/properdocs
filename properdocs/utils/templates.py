from __future__ import annotations

from typing import TYPE_CHECKING, Sequence, TypedDict

if TYPE_CHECKING:
    import datetime

from markupsafe import Markup

try:
    from jinja2 import pass_context as contextfilter  # type: ignore
except ImportError:
    from jinja2 import contextfilter  # type: ignore

from properdocs.utils import normalize_url

if TYPE_CHECKING:
    from properdocs.config.config_options import ExtraScriptValue
    from properdocs.config.defaults import ProperDocsConfig
    from properdocs.structure.files import File
    from properdocs.structure.nav import Navigation
    from properdocs.structure.pages import Page


class TemplateContext(TypedDict):
    nav: Navigation
    pages: Sequence[File]
    base_url: str
    extra_css: Sequence[str]  # Do not use, prefer `config.extra_css`.
    extra_javascript: Sequence[str]  # Do not use, prefer `config.extra_javascript`.
    properdocs_version: str
    mkdocs_version: str
    build_date_utc: datetime.datetime
    config: ProperDocsConfig
    page: Page | None


@contextfilter
def url_filter(context: TemplateContext, value: str) -> str:
    """A Template filter to normalize URLs."""
    return normalize_url(str(value), page=context['page'], base=context['base_url'])


@contextfilter
def script_tag_filter(context: TemplateContext, extra_script: ExtraScriptValue) -> str:
    """Converts an ExtraScript value to an HTML <script> tag line."""
    html = '<script src="{0}"'
    if not isinstance(extra_script, str):
        if extra_script.type:
            html += ' type="{1.type}"'
        if extra_script.defer:
            html += ' defer'
        if extra_script.async_:
            html += ' async'
    html += '></script>'
    return Markup(html).format(url_filter(context, str(extra_script)), extra_script)
