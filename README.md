# ProperDocs

[![PyPI Version](https://img.shields.io/pypi/v/properdocs.svg)](https://pypi.org/project/properdocs/)
[![Build Status](https://github.com/properdocs/properdocs/actions/workflows/ci.yml/badge.svg)](https://github.com/properdocs/properdocs/actions/workflows/ci.yml)

## Background

ProperDocs is a fork of [MkDocs](https://github.com/mkdocs/mkdocs/), aiming to be a complete drop-in replacement for it. We do not intend to make any breaking changes, but rather focus on bug fixes and incremental features. The fork was necessary because development of the original MkDocs project was abandoned.

[**Please see our statement about forking MkDocs and how to migrate to ProperDocs**](https://github.com/orgs/ProperDocs/discussions/33).

New users can get started using the [**documentation**](https://properdocs.org).

## Description

ProperDocs is a static site generator intended for project documentation. Source files are written in Markdown and converted to static HTML during the build process. This can then be deployed to any basic webserver (most commonly, [GitHub Pages](pages.github.com)).

Project configuration is defined in a YAML configuration file ([`properdocs.yml`](https://properdocs.org/user-guide/configuration/)). This file specifies the documentation structure, theme configuration, and optional plugin settings.

ProperDocs is extensible through plugins, themes and Python-Markdown extensions. You can browse them in our [**catalog**](https://github.com/ProperDocs/catalog).

[Our own **documentation**](https://properdocs.org/) uses ProperDocs. Examples and instructions on how to get started can be found there.

If you're coming from MkDocs, check our [message welcoming MkDocs users](https://github.com/orgs/ProperDocs/discussions/33).

## Support and discussions

If you need help, do not hesitate to get in contact with the community!

*   To report a **bug** or make a **feature request** about **core ProperDocs functionality**, open an [**Issue**](https://github.com/ProperDocs/properdocs/issues/) on GitHub.  

*   For **questions** and high-level **discussions**, use [**Discussions**](https://github.com/ProperDocs/properdocs/discussions/) on GitHub.

    Note that typically we will not be familiar with *features* of third-party plugins, so questions about them should probably go to their specific repository.  
    But we definitely want to hear in case there are any compatibility problems versus MkDocs.

*   For **small questions of any kind**, a good option is the **[Discord server](https://discord.gg/CwYAgEPHZd)**.

## Contributing

We welcome contributions from the community.  
Details are described in the [**Contributing Guide**](https://properdocs.org/about/contributing/) - including the development setup, coding guidelines and contribution workflow.

## Code of Conduct

All participants in the ProperDocs project are expected to follow the [**PSF Code of Conduct**](https://www.python.org/psf/conduct/).

## License

ProperDocs is distributed under the [**BSD-2-Clause license**](LICENSE).
