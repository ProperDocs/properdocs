from __future__ import annotations

import io
import logging
import shutil
import sys
import tempfile
from os.path import isdir, isfile, join
from typing import TYPE_CHECKING, BinaryIO, Callable
from urllib.parse import urlsplit

from properdocs.commands.build import build
from properdocs.config import load_config
from properdocs.livereload import LiveReloadServer, _serve_url

if TYPE_CHECKING:
    from properdocs.config.defaults import ProperDocsConfig

log = logging.getLogger(__name__)


def serve(
    config_file: str | BinaryIO | None = None,
    livereload: bool = True,
    build_type: str | None = None,
    watch_theme: bool = False,
    watch: list[str] = [],
    *,
    open_in_browser: bool = False,
    **kwargs,
) -> None:
    """
    Start the ProperDocs development server.

    By default it will serve the documentation on http://localhost:8000/ and
    it will rebuild the documentation and refresh the page automatically
    whenever a file is edited.
    """
    # Create a temporary build directory, and set some options to serve it
    site_dir = tempfile.mkdtemp(prefix='properdocs_')

    get_config_file: Callable[[], str | BinaryIO | None]
    if config_file is None or isinstance(config_file, str):
        get_config_file = lambda: config_file
    elif sys.stdin and config_file is sys.stdin.buffer:
        # Stdin must be read only once, can't be reopened later.
        config_file_content = sys.stdin.buffer.read()
        get_config_file = lambda: io.BytesIO(config_file_content)
    else:
        # If closed file descriptor, reopen it through the file path instead.
        get_config_file = lambda: (
            config_file.name if getattr(config_file, 'closed', False) else config_file
        )

    def get_config():
        config = load_config(
            config_file=get_config_file(),
            site_dir=site_dir,
            **kwargs,
        )
        config.site_dir = site_dir  # Overwrite it afterwards, so normal validation still kicks in.
        config.watch.extend(watch)
        return config

    is_clean = build_type == 'clean'
    is_dirty = build_type == 'dirty'

    config = get_config()
    config.plugins.on_startup(command=('build' if is_clean else 'serve'), dirty=is_dirty)

    host, port = config.dev_addr
    mount_path = urlsplit(config.site_url or '/').path
    config.site_url = serve_url = _serve_url(host, port, mount_path)

    def builder(config: ProperDocsConfig | None = None):
        log.info("Building documentation...")
        if config is None:
            config = get_config()
            config.site_url = serve_url

        build(config, serve_url=None if is_clean else serve_url, dirty=is_dirty)

    server = LiveReloadServer(
        builder=builder, host=host, port=port, root=site_dir, mount_path=mount_path
    )

    def error_handler(code) -> bytes | None:
        if code in (404, 500):
            error_page = join(site_dir, f'{code}.html')
            if isfile(error_page):
                with open(error_page, 'rb') as f:
                    return f.read()
        return None

    server.error_handler = error_handler

    try:
        # Perform the initial build
        builder(config)

        if livereload:
            # Watch the documentation files, the config file and the theme files.
            server.watch(config.docs_dir)
            if config.config_file_path:
                server.watch(config.config_file_path)

            if watch_theme:
                for d in config.theme.dirs:
                    server.watch(d)

            # Run `serve` plugin events.
            server = config.plugins.on_serve(server, config=config, builder=builder)

            for item in config.watch:
                server.watch(item)

        try:
            server.serve(open_in_browser=open_in_browser)
        except KeyboardInterrupt:
            log.info("Shutting down...")
        finally:
            server.shutdown()
    finally:
        config.plugins.on_shutdown()
        if isdir(site_dir):
            shutil.rmtree(site_dir)
