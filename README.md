# ProperDocs

[![PyPI Version][pypi-v-image]][pypi-v-link]
[![Build Status][GHAction-image]][GHAction-link]

ProperDocs is a static site generator intended for project documentation. Source files are written in Markdown and converted to static HTML during the build process.

Project configuration is defined in a YAML configuration file (`properdocs.yml`). This file specifies the documentation structure, theme configuration, and optional plugin settings.

ProperDocs supports extension through plugins, themes and Markdown extensions.

For usage instructions and examples, see the Documentation.

---

## Features

Current functionality includes:

- Conversion of Markdown source files into static HTML pages
- YAML-based configuration
- Plugin system for extending functionality
- Support for Markdown extensions
- Support for third-party themes
- Static output suitable for deployment on standard web servers

Additional functionality is available through plugins.

---

## Support

If you encounter problems while using ProperDocs, the following resources are available:

-   For questions and high-level discussions, use **[Discussions]** on GitHub.
    - For small questions, a good alternative is the **[Discord server]**.
-   To report a bug or make a feature request, open an **[Issue]** on GitHub.

Support is generally limited to **core ProperDocs functionality**. Issues related to third-party themes, plugins or extensions should normally be reported to the maintainers of those projects.

Questions about such components may still be discussed in chat.

---

## Links

- [Official Documentation][properdocs]
- [Latest Release Notes][release-notes]
- [Catalog of third-party plugins, themes and recipes][catalog]

---

## Contributing

Contributions are welcome.

For development setup, coding guidelines and contribution workflow, see the **[Contributing Guide]**.

---

## Code of Conduct

All participants in the ProperDocs project are expected to follow the **[PSF Code of Conduct]**.

---

## License

ProperDocs is distributed under the [**BSD-2-Clause license**](LICENSE).

<!-- Badges -->
[pypi-v-image]: https://img.shields.io/pypi/v/properdocs.svg
[pypi-v-link]: https://pypi.org/project/properdocs/
[GHAction-image]: https://github.com/properdocs/properdocs/actions/workflows/ci.yml/badge.svg
[GHAction-link]: https://github.com/properdocs/properdocs/actions/workflows/ci.yml

<!-- Links -->
[properdocs]: https://properdocs.org
[Issue]: https://github.com/properdocs/properdocs/issues
[Discussions]: https://github.com/properdocs/properdocs/discussions
[Discord server]: https://discord.gg/CwYAgEPHZd
[release-notes]: https://properdocs.org/about/release-notes/
[Contributing Guide]: https://properdocs.org/about/contributing/
[PSF Code of Conduct]: https://www.python.org/psf/conduct/
[catalog]: https://github.com/properdocs/catalog
