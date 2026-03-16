"""
This module shows a warning to users that are still using the `mkdocs` executable, and doesn't show up for `properdocs`.

It kicks in as long as at least one plugin calls the `setup` function.
Please add our warning to your plugin in the following way:

```
import properdocs.replacement_warning

properdocs.replacement_warning.setup()
```

This should be added somewhere in your module's topmost import (__init__.py) at the top level, to activate early.
"""

import os
import os.path
import sys
import textwrap

_warning_message = '''\
----------------------------------------------------------------

WARNING: MkDocs may break support for all existing plugins and themes soon!

The owner of MkDocs has completely abandoned maintenance of the project, and instead is planning \
to publish a "version 2" which will not support any existing themes, plugins or even your \
configuration files. This v2 may eventually replace what you download with `pip install mkdocs`, \
suddenly breaking the build of your existing site.

To avoid these risks, switch to *ProperDocs*, a continuation of MkDocs 1.x and a drop-in replacement that supports your current MkDocs setup.
Simply install it with `pip install properdocs` and build your site with `properdocs build` instead of the MkDocs equivalents.

For more info visit https://github.com/ProperDocs/properdocs/discussions/33 and https://properdocs.org/

(This warning was initiated by one of the plugins that you depend on.)

----------------------------------------------------------------'''


def setup():
    global _warning_message
    if not _warning_message:
        return

    if is_running_from_mkdocs():
        # Allow to silence this warning with NO_MKDOCS_2_WARNING=true
        if os.environ.get('NO_MKDOCS_2_WARNING', '').lower() != 'true':
            print(colorize_message(_warning_message), file=sys.stderr)  # noqa: T201

    # Prevent warnings from the theme that already uses this environment variable.
    # That warning does not apply to ProperDocs.
    os.environ['NO_MKDOCS_2_WARNING'] = 'true'

    _warning_message = ''  # Disable all activations other than the first one.


def is_running_from_mkdocs():
    if 'mkdocs' not in sys.modules:
        return False

    dir, name = os.path.split(sys.argv[0])
    if name in ('mkdocs', 'mkdocs.exe'):
        return True
    elif name.endswith('.py'):
        dir, name = os.path.split(dir)
        if name == 'mkdocs':
            return True
    return False


def colorize_message(message: str, max_width: int = 145) -> str:
    try:  # Try to colorize and rewrap the message, ignore all errors just in case.
        import re
        import shutil

        if terminal_width := shutil.get_terminal_size(fallback=(0, 0)).columns:
            lines = []
            for line in message.split('\n'):
                lines.extend(textwrap.wrap(line, width=min(terminal_width, max_width)) or [''])
            message = '\n'.join(lines)

        import click

        message = re.sub(r'\bWARNING\b', lambda m: click.style(m[0], fg='red', bold=True), message)
        message = re.sub(r'https://\S+', lambda m: click.style(m[0], bold=True), message)
        message = re.sub(
            r'\B`\b[\s\S]+?\b`\B', lambda m: click.style(m[0], bold=True, fg='yellow'), message
        )
        message = re.sub(r'\B\*\b([\s\S]+?)\b\*\B', lambda m: click.style(m[1], bold=True), message)
    except Exception:
        pass
    return message
