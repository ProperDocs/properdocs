from __future__ import annotations

import logging
import os

config_text = 'site_name: My Docs\n'
index_text = """# Welcome to ProperDocs

For full documentation visit [properdocs.org](https://properdocs.org).

## Commands

* `properdocs new [dir-name]` - Create a new project.
* `properdocs serve` - Start the live-reloading docs server.
* `properdocs build` - Build the documentation site.
* `properdocs -h` - Print help message and exit.

## Project layout

    properdocs.yml # The configuration file.
    docs/
        index.md   # The documentation homepage.
        ...        # Other markdown pages, images and other files.
"""

log = logging.getLogger(__name__)


def new(output_dir: str) -> None:
    docs_dir = os.path.join(output_dir, 'docs')
    config_path = os.path.join(output_dir, 'properdocs.yml')
    index_path = os.path.join(docs_dir, 'index.md')

    if os.path.exists(config_path):
        log.info('Project already exists.')
        return

    if not os.path.exists(output_dir):
        log.info(f'Creating project directory: {output_dir}')
        os.mkdir(output_dir)

    log.info(f'Writing config file: {config_path}')
    with open(config_path, 'w', encoding='utf-8') as f:
        f.write(config_text)

    if os.path.exists(index_path):
        return

    log.info(f'Writing initial docs: {index_path}')
    if not os.path.exists(docs_dir):
        os.mkdir(docs_dir)
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(index_text)
