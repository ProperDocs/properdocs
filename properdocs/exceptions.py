from __future__ import annotations

from click import ClickException, echo


class ProperDocsException(ClickException):
    """
    The base class which all ProperDocs exceptions inherit from. This should
    not be raised directly. One of the subclasses should be raised instead.
    """


MkDocsException = ProperDocsException  # Legacy alias


class Abort(ProperDocsException, SystemExit):
    """Abort the build."""

    code = 1

    def show(self, *args, **kwargs) -> None:
        echo('\n' + self.format_message())


class ConfigurationError(ProperDocsException):
    """
    This error is raised by configuration validation when a validation error
    is encountered. This error should be raised by any configuration options
    defined in a plugin's [config_scheme][].
    """


class BuildError(ProperDocsException):
    """
    This error may be raised by ProperDocs during the build process. Plugins should
    not raise this error.
    """


class PluginError(BuildError):
    """
    A subclass of [`properdocs.exceptions.BuildError`][] which can be raised by plugin
    events.
    """
