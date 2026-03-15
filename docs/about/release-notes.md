# Release Notes

---

## Upgrading

To upgrade ProperDocs to the latest version, use pip:

```bash
pip install -U properdocs
```

You can determine your currently installed version using `properdocs --version`:

```console
$ properdocs --version
properdocs, version 1.5.0 from /path/to/properdocs (Python 3.10)
```

## Maintenance team

The current and past members of the ProperDocs team.

* [@tomchristie](https://github.com/tomchristie/)
* [@d0ugal](https://github.com/d0ugal/)
* [@waylan](https://github.com/waylan/)
* [@oprypin](https://github.com/oprypin/)
* [@ultrabug](https://github.com/ultrabug/)

## Version 1.6.1 (2024-08-30)

### Fixed

* Fix build error when environment variable `SOURCE_DATE_EPOCH=0` is set. #3795
* Fix build error when `mkdocs_theme.yml` config is empty. #3700
* Support `python -W` and `PYTHONWARNINGS` instead of overriding the configuration. #3809
* Support running with Docker under strict mode, by removing `0.0.0.0` dev server warning. #3784
* Drop unnecessary `changefreq` from `sitemap.xml`. #3629
* Fix JavaScript console error when closing menu dropdown. #3774
* Fix JavaScript console error that occur on repeated clicks. #3730
* Fix JavaScript console error that can occur on dropdown selections. #3694

### Added

* Added translations for Dutch. #3804
* Added and updated translations for Chinese (Simplified). #3684

## Version 1.6.0 (2024-04-20)

### Local preview

*   `mkdocs serve` no longer locks up the browser when more than 5 tabs are open. This is achieved by closing the polling connection whenever a tab becomes inactive. Background tabs will no longer auto-reload either - that will instead happen as soon the tab is opened again. Context: #3391

*   New flag `serve --open` to open the site in a browser.  
    After the first build is finished, this flag will cause the default OS Web browser to be opened at the home page of the local site.  
    Context: #3500

#### Drafts

> DANGER: **Changed from version 1.5.**

**The `exclude_docs` config was split up into two separate concepts.**

The `exclude_docs` config no longer has any special behavior for `mkdocs serve` - it now always completely excludes the listed documents from the site.

If you wish to use the "drafts" functionality like the `exclude_docs` key used to do in MkDocs 1.5, please switch to the **new config key `draft_docs`**.

See [documentation](../user-guide/configuration.md#exclude_docs).

Other changes:

* Reduce warning levels when a "draft" page has a link to a non-existent file. Context: #3449

### Update to deduction of page titles

MkDocs 1.5 had a change in behavior in deducing the page titles from the first heading. Unfortunately this could cause unescaped HTML tags or entities to appear in edge cases.

Now tags are always fully sanitized from the title. Though it still remains the case that [`Page.title`][properdocs.structure.pages.Page.title] is expected to contain HTML entities and is passed directly to the themes.

Images (notably, emojis in some extensions) get preserved in the title only through their `alt` attribute's value.

Context: #3564, #3578

### Themes

* Built-in themes now also support Polish language (#3613)

#### "readthedocs" theme

*   Fix: "readthedocs" theme can now correctly handle deeply nested nav configurations (over 2 levels deep), without confusedly expanding all sections and jumping around vertically. (#3464)

*   Fix: "readthedocs" theme now shows a link to the repository (with a generic logo) even when isn't one of the 3 known hosters. (#3435)

*   "readthedocs" theme now also has translation for the word "theme" in the footer that mistakenly always remained in English. (#3613, #3625)

#### "mkdocs" theme

The "mkdocs" theme got a big update to a newer version of Bootstrap, meaning a slight overhaul of styles. Colors (most notably of admonitions) have much better contrast.

The "mkdocs" theme now has support for dark mode - both automatic (based on the OS/browser setting) and with a manual toggle. Both of these options are **not** enabled by default and need to be configured explicitly.  
See `color_mode`, `user_color_mode_toggle` in [**documentation**](../user-guide/choosing-your-theme.md#mkdocs).

> WARNING: **Possible breaking change.**
>
> jQuery is no longer included into the "mkdocs" theme. If you were relying on it in your scripts, you will need to separately add it first (into `properdocs.yml`) as an extra script:
>
> ```yaml
> extra_javascript:
>   - https://code.jquery.com/jquery-3.7.1.min.js
> ```
>
> Or even better if the script file is copied and included from your docs dir.

Context: #3493, #3649

### Configuration

#### New "`enabled`" setting for all plugins

You may have seen some plugins take up the convention of having a setting `enabled: false` (or usually controlled through an environment variable) to make the plugin do nothing.

Now *every* plugin has this setting. Plugins can still *choose* to implement this config themselves and decide how it behaves (and unless they drop older versions of MkDocs, they still should for now), but now there's always a fallback for every plugin.

See [**documentation**](../user-guide/configuration.md/#enabled-option). Context: #3395

### Validation

#### Validation of hyperlinks between pages

##### Absolute links

> Historically, within Markdown, MkDocs only recognized **relative** links that lead to another physical `*.md` document (or media file). This is a good convention to follow because then the source pages are also freely browsable without MkDocs, for example on GitHub. Whereas absolute links were left unmodified (making them often not work as expected or, more recently, warned against).

If you dislike having to always use relative links, now you can opt into absolute links and have them work correctly.

If you set the setting `validation.links.absolute_links` to the new value `relative_to_docs`, all Markdown links starting with `/` will be understood as being relative to the `docs_dir` root. The links will then be validated for correctness according to all the other rules that were already working for relative links in prior versions of MkDocs. For the HTML output, these links will still be turned relative so that the site still works reliably.

So, now any document (e.g. "dir1/foo.md") can link to the document "dir2/bar.md" as `[link](/dir2/bar.md)`, in addition to the previously only correct way `[link](../dir2/bar.md)`.

You have to enable the setting, though. The default is still to just skip any processing of such links.

See [**documentation**](../user-guide/configuration.md#validation-of-absolute-links). Context: #3485

###### Absolute links within nav

Absolute links within the `nav:` config were also always skipped. It is now possible to also validate them in the same way with `validation.nav.absolute_links`. Though it makes a bit less sense because then the syntax is simply redundant with the syntax that comes without the leading slash.

##### Anchors

There is a new config setting that is recommended to enable warnings for:

```yaml
validation:
  anchors: warn
```

Example of a warning that this can produce:

```text
WARNING -  Doc file 'foo/example.md' contains a link '../bar.md#some-heading', but the doc 'foo/bar.md' does not contain an anchor '#some-heading'.
```

Any of the below methods of declaring an anchor will be detected by MkDocs:

```markdown
## Heading producing an anchor

## Another heading {#custom-anchor-for-heading-using-attr-list}

<a id="raw-anchor"></a>

[](){#markdown-anchor-using-attr-list}
```

Plugins and extensions that insert anchors, in order to be compatible with this, need to be developed as treeprocessors that insert `etree` elements as their mode of operation, rather than raw HTML which is undetectable for this purpose.

If you as a user are dealing with falsely reported missing anchors and there's no way to resolve this, you can choose to disable these messages by setting this option to `ignore` (and they are at INFO level by default anyway).

See [**documentation**](../user-guide/configuration.md#validation). Context: #3463

Other changes:

*   When the `nav` config is not specified at all, the `not_in_nav` setting (originally added in 1.5.0) gains an additional behavior: documents covered by `not_in_nav` will not be part of the automatically deduced navigation. Context: #3443

*   Fix: the `!relative` YAML tag for `markdown_extensions` (originally added in 1.5.0) - it was broken in many typical use cases.

    See [**documentation**](../user-guide/configuration.md#paths-relative-to-the-current-file-or-site). Context: #3466

*   Config validation now exits on first error, to avoid showing bizarre secondary errors. Context: #3437

*   MkDocs used to shorten error messages for unexpected errors such as "file not found", but that is no longer the case, the full error message and stack trace will be possible to see (unless the error has a proper handler, of course). Context: #3445

### Upgrades for plugin developers

#### Plugins can add multiple handlers for the same event type, at multiple priorities

See [`properdocs.plugins.CombinedEvent`][] in [**documentation**](../dev-guide/plugins.md#event-priorities). Context: #3448

#### Enabling true generated files and expanding the [`File`][properdocs.structure.files.File] API

See [**documentation**][properdocs.structure.files.File].

*   There is a new pair of attributes [`File.content_string`][properdocs.structure.files.File.content_string]/[`content_bytes`][properdocs.structure.files.File.content_bytes] that becomes the official API for obtaining the content of a file and is used by MkDocs itself.

    This replaces the old approach where one had to manually read the file located at [`File.abs_src_path`][properdocs.structure.files.File.abs_src_path], although that is still the primary action that these new attributes do under the hood.

*   The content of a `File` can be backed by a string and no longer has to be a real existing file at `abs_src_path`.

    It is possible to **set** the attribute `File.content_string` or `File.content_bytes` and it will take precedence over `abs_src_path`.

    Further, `abs_src_path` is no longer guaranteed to be present and can be `None` instead. MkDocs itself still uses physical files in all cases, but eventually plugins will appear that don't populate this attribute.

*   There is a new constructor [`File.generated()`][properdocs.structure.files.File.generated] that should be used by plugins instead of the `File()` constructor. It is much more convenient because one doesn't need to manually look up the values such as `docs_dir` and `use_directory_urls`. Its signature is one of:

    ```python
    f = File.generated(config: ProperDocsConfig, src_uri: str, content: str | bytes)
    f = File.generated(config: ProperDocsConfig, src_uri: str, abs_src_path: str)
    ```

    This way, it is now extremely easy to add a virtual file even from a hook:

    ```python
    def on_files(files: Files, config: ProperDocsConfig):
        files.append(File.generated(config, 'fake/path.md', content="Hello, world!"))
    ```

    For large content it is still best to use physical files, but one no longer needs to manipulate the path by providing a fake unused `docs_dir`.

*   There is a new attribute [`File.generated_by`][properdocs.structure.files.File.generated_by] that arose by convention - for generated files it should be set to the name of the plugin (the key in the `plugins:` collection) that produced this file. This attribute is populated automatically when using the `File.generated()` constructor.

*   It is possible to set the [`edit_uri`][properdocs.structure.files.File.edit_uri] attribute of a `File`, for example from a plugin or hook, to make it different from the default (equal to `src_uri`), and this will be reflected in the edit link of the document. This can be useful because some pages aren't backed by a real file and are instead created dynamically from some other source file or script. So a hook could set the `edit_uri` to that source file or script accordingly.

*   The `File` object now stores its original `src_dir`, `dest_dir`, `use_directory_urls` values as attributes.

*   Fields of `File` are computed on demand but cached. Only the three above attributes are primary ones, and partly also [`dest_uri`][properdocs.structure.files.File.dest_uri]. This way, it is possible to, for example, overwrite `dest_uri` of a `File`, and `abs_dest_path` will be calculated based on it. However you need to clear the attribute first using `del f.abs_dest_path`, because the values are cached.

*   `File` instances are now hashable (can be used as keys of a `dict`). Two files can no longer be considered "equal" unless it's the exact same instance of `File`.

Other changes:

*   The internal storage of `File` objects inside a `Files` object has been reworked, so any plugins that choose to access `Files._files` will get a deprecation warning.

*   The order of `File` objects inside a `Files` collection is no longer significant when automatically inferring the `nav`. They get forcibly sorted according to the default alphabetic order.

Context: #3451, #3463

### Hooks and debugging

*   Hook files can now import adjacent *.py files using the `import` statement. Previously this was possible to achieve only through a `sys.path` workaround. See the new mention in [documentation](../user-guide/configuration.md#hooks). Context: #3568

*   Verbose `-v` log shows the sequence of plugin events in more detail - shows each invoked plugin one by one, not only the event type. Context: #3444

### Deprecations

*   Python 3.7 is no longer supported, Python 3.12 is officially supported. Context: #3429

*   The theme config file `mkdocs_theme.yml` no longer executes YAML tags. Context: #3465

*   The plugin event `on_page_read_source` is soft-deprecated because there is always a better alternative to it (see the new `File` API or just `on_page_markdown`, depending on the desired interaction).

    When multiple plugins/hooks apply this event handler, they trample over each other, so now there is a warning in that case.

    See [**documentation**](../dev-guide/plugins.md#on_page_read_source). Context: #3503

#### API deprecations

*   It is no longer allowed to set `File.page` to a type other than `Page` or a subclass thereof. Context: #3443 - following the deprecation in version 1.5.3 and #3381.

*   `Theme._vars` is deprecated - use `theme['foo']` instead of `theme._vars['foo']`

*   `utils`: `modified_time()`, `get_html_path()`, `get_url_path()`, `is_html_file()`, `is_template_file()` are removed. `path_to_url()` is deprecated.

*   `LiveReloadServer.watch()` no longer accepts a custom callback.

Context: #3429

### Misc

* The `sitemap.xml.gz` file is slightly more reproducible and no longer changes on every build, but instead only once per day (upon a date change). Context: #3460

Other small improvements; see [commit log](https://github.com/properdocs/properdocs/compare/1.5.3...1.6.0).

## Version 1.5.3 (2023-09-18)

*   Fix `mkdocs serve` sometimes locking up all browser tabs when navigating quickly (#3390)

*   Add many new supported languages for "search" plugin - update lunr-languages to 1.12.0 (#3334)

*   Bugfix (regression in 1.5.0): In "readthedocs" theme the styling of "breadcrumb navigation" was broken for nested pages (#3383)

*   Built-in themes now also support Chinese (Traditional, Taiwan) language (#3154)

*   Plugins can now set `File.page` to their own subclass of `Page`. There is also now a warning if `File.page` is set to anything other than a strict subclass of `Page`. (#3367, #3381)

    Note that just instantiating a `Page` [sets the file automatically](https://github.com/properdocs/properdocs/blob/f94ab3f62d0416d484d81a0c695c8ca86ab3b975/mkdocs/structure/pages.py#L34), so care needs to be taken not to create an unneeded `Page`.

Other small improvements; see [commit log](https://github.com/properdocs/properdocs/compare/1.5.2...1.5.3).

## Version 1.5.2 (2023-08-02)

*   Bugfix (regression in 1.5.0): Restore functionality of `--no-livereload`. (#3320)

*   Bugfix (regression in 1.5.0): The new page title detection would sometimes be unable to drop anchorlinks - fix that. (#3325)

*   Partly bring back pre-1.5 API: `extra_javascript` items will once again be mostly strings, and only sometimes `ExtraScriptValue` (when the extra `script` functionality is used).

    Plugins should be free to append strings to `config.extra_javascript`, but when reading the values, they must still make sure to read it as `str(value)` in case it is an `ExtraScriptValue` item. For querying the attributes such as `.type` you need to check `isinstance` first. Static type checking will guide you in that. (#3324)

See [commit log](https://github.com/properdocs/properdocs/compare/1.5.1...1.5.2).

## Version 1.5.1 (2023-07-28)

*   Bugfix (regression in 1.5.0): Make it possible to treat `ExtraScriptValue` as a path. This lets some plugins still work despite the breaking change.

*   Bugfix (regression in 1.5.0): Prevent errors for special setups that have 3 conflicting files, such as `index.html`, `index.md` *and* `README.md` (#3314)

See [commit log](https://github.com/properdocs/properdocs/compare/1.5.0...1.5.1).

## Version 1.5.0 (2023-07-26)

### New command `mkdocs get-deps`

This command guesses the Python dependencies that a MkDocs site requires in order to build. It simply prints the PyPI packages that need to be installed. In the terminal it can be combined directly with an installation command as follows:

```bash
pip install $(mkdocs get-deps)
```

The idea is that right after running this command, you can directly follow it up with `mkdocs build` and it will almost always "just work", without needing to think which dependencies to install.

The way it works is by scanning `properdocs.yml` for `themes:`, `plugins:`, `markdown_extensions:` items and doing a reverse lookup based on a large list of known projects (catalog, see below).

Of course, you're welcome to use a "virtualenv" with such a command. Also note that for environments that require stability (for example CI) directly installing deps in this way is not a very reliable approach as it precludes dependency pinning.

The command allows overriding which config file is used (instead of `properdocs.yml` in the current directory) as well as which catalog of projects is used (instead of downloading it from the default location). See [`mkdocs get-deps --help`](../user-guide/cli.md#properdocs-get-deps).

Context: #3205

### MkDocs has an official catalog of plugins

Check out <https://github.com/mkdocs/catalog> and add all your general-purpose plugins, themes and extensions there, so that they can be looked up through `mkdocs get-deps`.

This was renamed from "best-of-mkdocs" and received significant updates. In addition to `pip` installation commands, the page now shows the config boilerplate needed to add a plugin.

### Expanded validation of links

#### Validated links in Markdown

> As you may know, within Markdown, MkDocs really only recognizes **relative** links that lead to another physical `*.md` document (or media file). This is a good convention to follow because then the source pages are also freely browsable without MkDocs, for example on GitHub. MkDocs knows that in the output it should turn those `*.md` links into `*.html` as appropriate, and it would also always tell you if such a link doesn't actually lead to an existing file.

However, the checks for links were really loose and had many concessions. For example, links that started with `/` ("absolute") and links that *ended* with `/` were left as is and no warning was shown, which allowed such very fragile links to sneak into site sources: links that happen to work right now but get no validation and links that confusingly need an extra level of `..` with `use_directory_urls` enabled.

Now, in addition to validating relative links, MkDocs will print `INFO` messages for unrecognized types of links (including absolute links). They look like this:

```text
INFO - Doc file 'example.md' contains an absolute link '/foo/bar/', it was left as is. Did you mean 'foo/bar.md'?
```

If you don't want any changes, not even the `INFO` messages, and wish to revert to the silence from MkDocs 1.4, add the following configs to `properdocs.yml` (**not** recommended):

```yaml
validation:
  absolute_links: ignore
  unrecognized_links: ignore
```

If, on the opposite end, you want these to print `WARNING` messages and cause `mkdocs build --strict` to fail, you are recommended to configure these to `warn` instead.

See [**documentation**](../user-guide/configuration.md#validation) for actual recommended settings and more details. Context: #3283

#### Validated links in the nav

Links to documents in the [`nav` configuration](../user-guide/configuration.md#nav) now also have configurable validation, though with no changes to the defaults.

You are welcomed to turn on validation for files that were forgotten and excluded from the nav. Example:

```yaml
validation:
  nav:
    omitted_files: warn
    absolute_links: warn
```

This can make the following message appear with the `WARNING` level (as opposed to `INFO` as the only option previously), thus being caught by `mkdocs --strict`:

```text
INFO - The following pages exist in the docs directory, but are not included in the "nav" configuration: ...
```

See [**documentation**](../user-guide/configuration.md#validation). Context: #3283, #1755

#### Mark docs as intentionally "not in nav"

There is a new config `not_in_nav`. With it, you can mark particular patterns of files as exempt from the above `omitted_files` warning type; no messages will be printed for them anymore. (As a corollary, setting this config to `*` is the same as ignoring `omitted_files` altogether.)

This is useful if you generally like these warnings about files that were forgotten from the nav, but still have some pages that you knowingly excluded from the nav and just want to build and copy them.

The `not_in_nav` config is a set of gitignore-like patterns. See the next section for an explanation of another such config.

See [**documentation**](../user-guide/configuration.md#not_in_nav). Context: #3224, #1888

### Excluded doc files

There is a new config `exclude_docs` that tells MkDocs to ignore certain files under `docs_dir` and *not* copy them to the built `site` as part of the build.

Historically MkDocs would always ignore file names starting with a dot, and that's all. Now this is all configurable: you can un-ignore these and/or ignore more patterns of files.

The `exclude_docs` config follows the [.gitignore pattern format](https://git-scm.com/docs/gitignore#_pattern_format) and is specified as a multiline YAML string. For example:

```yaml
exclude_docs: |
  *.py               # Excludes e.g. docs/hooks/foo.py
  /requirements.txt  # Excludes docs/requirements.txt
```

Validation of links (described above) is also affected by `exclude_docs`. During `mkdocs serve` the messages explain the interaction, whereas during `mkdocs build` excluded files are as good as nonexistent.

As an additional related change, if you have a need to have both `README.md` and `index.md` files in a directory but publish only one of them, you can now use this feature to explicitly ignore one of them and avoid warnings.

See [**documentation**](../user-guide/configuration.md#exclude_docs). Context: #3224

#### Drafts

> DANGER: **Dropped from version 1.6:**
>
> The `exclude_docs` config no longer applies the "drafts" functionality for `mkdocs serve`. This was renamed to [`draft_docs`](../user-guide/configuration.md#draft_docs).

The `exclude_docs` config has another behavior: all excluded Markdown pages will still be previewable in `mkdocs serve` only, just with a "DRAFT" marker on top. Then they will of course be excluded from `mkdocs build` or `gh-deploy`.

If you don't want `mkdocs serve` to have any special behaviors and instead want it to perform completely normal builds, use the new flag `mkdocs serve --clean`.

See [**documentation**](../user-guide/configuration.md#exclude_docs). Context: #3224

### `mkdocs serve` no longer exits after build errors

If there was an error (from the config or a plugin) during a site re-build, `mkdocs serve` used to exit after printing a stack trace. Now it will simply freeze the server until the author edits the files to fix the problem, and then will keep reloading.

But errors on the *first* build still cause `mkdocs serve` to exit, as before.

Context: #3255

### Page titles will be deduced from any style of heading

MkDocs always had the ability to infer the title of a page (if it's not specified in the `nav`) based on the first line of the document, if it had a `<h1>` heading that had to written starting with the exact character `#`. Now any style of Markdown heading is understood (#1886). Due to the previous simplistic parsing, it was also impossible to use `attr_list` attributes in that first heading (#3136). Now that is also fixed.

### Markdown extensions can use paths relative to the current document

This is aimed at extensions such as `pymdownx.snippets` or `markdown_include.include`: you can now specify their include paths to be relative to the currently rendered Markdown document, or relative to the `docs_dir`. Any other extension can of course also make use of the new `!relative` YAML tag.

```yaml
markdown_extensions:
  - pymdownx.snippets:
      base_path: !relative
```

See [**documentation**](../user-guide/configuration.md#paths-relative-to-the-current-file-or-site). Context: #2154, #3258

### `<script>` tags can specify `type="module"` and other attributes

In `extra_javascript`, if you use the `.mjs` file extension or explicitly specify a `type: module` key, the script will be added with the `type="module"` attribute. `defer: true` and `async: true` keys are also available.

See [updated **documentation** for `extra_javascript`](../user-guide/configuration.md#extra_javascript).

**At first this is only supported in built-in themes, other themes need to follow up, see below.**

Context: #3237

### Changes for theme developers (action required!)

Using the construct `{% for script in extra_javascript %}` is now fully obsolete because it cannot allow customizing the attributes of the `<script>` tag. It will keep working but blocks some of MkDocs' features.

Instead, you now need to use `config.extra_javascript` (which was already the case for a while) and couple it with the new `script_tag` filter:

```django
    {%- for script in config.extra_javascript %}
      {{ script | script_tag }}
    {%- endfor %}
```

See [**documentation**](../dev-guide/themes.md#picking-up-css-and-javascript-from-the-config).

### Upgrades for plugin developers

*   Breaking change: `config.extra_javascript` is no longer a plain list of strings, but instead a list of `ExtraScriptValue` items. So you can no longer treat the list values as strings. If you want to keep compatibility with old versions, just always reference the items as `str(item)` instead. And you can still append plain strings to the list if you wish. See information about `<script>` tags above. Context: #3237

*   `File` has a new attribute `inclusion`. Its value is calculated from both the `exclude_docs` and `not_in_nav` configs, and implements their behavior. Plugins can read this value or write to it. New `File` instances by default follow whatever the configs say, but plugins can choose to make this decision explicitly, per file.

*   When creating a `File`, one can now set a `dest_uri` directly, rather than having to update it (and other dependent attributes) after creation. [Context](https://github.com/properdocs/properdocs/commit/d5af6426c52421f1113f6dcc591de1e01bea48bd)

*   A new config option was added - `DictOfItems`. Similarly to `ListOfItems`, it validates a mapping of config options that all have the same type. Keys are arbitrary but always strings. Context: #3242

*   A new function `get_plugin_logger` was added. In order to opt into a standardized way for plugins to log messages, please use the idiom:

    ```python
    log = properdocs.plugins.get_plugin_logger(__name__)
    ...
    log.info("Hello, world")
    ```

    Context: #3245

*   `SubConfig` config option can be conveniently subclassed with a particular type of config specified. For example, `class ExtraScript(SubConfig[ExtraScriptValue]):`. To see how this is useful, search for this class in code. [Context](https://github.com/properdocs/properdocs/commit/73e503990e3e3504bfe1cb627d41a7e97970687e)

*   Bugfix: `SubConfig` had a bug where paths (from `FilesystemObject` options) were not made relative to the main config file as intended, because `config_file_path` was not properly inherited to it. This is now fixed. Context: #3265

*   `Config` members now have a way to avoid clashing with Python's reserved words. This is achieved by stripping a trailing underscore from each member's name.

    Example of adding an `async` boolean option that can be set by the user as `async: true` and read programmatically as `config.async_`:

    ```python
    class ExampleConfig(Config):
        async_ = Type(bool, default=False)
    ```

    Previously making a config key with a reserved name was impossible with new-style schemas. [Context](https://github.com/properdocs/properdocs/commit/1db8e884fa7135a49adf7740add5d875a16a18bc)

*   `Theme` has its attributes properly declared and gained new attributes `theme.locale`, `theme.custom_dir`.

*   Some type annotations were made more precise. For example:

    * The `context` parameter has gained the type `TemplateContext` (`TypedDict`). [Context](https://github.com/properdocs/properdocs/commit/0f793b9984c7e6a1d53ce874e7d17b6d27ebf4b2)
    * The classes `Page`, `Section`, `Link` now have a common base class `StructureItem`. [Context](https://github.com/properdocs/properdocs/commit/01be507e30b05db0a4c44ef05ba62b2098010653)
    * Some methods stopped accepting `Config` and only accept `ProperDocsConfig` as was originally intended. [Context](https://github.com/properdocs/properdocs/commit/c459cd24fc0320333f51525e9cf681d4a8370f50)
    * `config.mdx_configs` got a proper type. Context: #3229

### Theme updates

*   Built-in themes mostly stopped relying on `<script defer>`. This may affect some usages of `extra_javascript`, mainly remove the need for custom handling of "has the page fully loaded yet". Context: #3237

*   "mkdocs" theme now has a styling for `>` blockquotes, previously they were not distinguished at all. Context: #3291

*   "readthedocs" theme was updated to v1.2.0 according to upstream, with improved styles for `<kbd>` and breadcrumb navigation. Context: #3058

*   Both built-in themes had their version of highlight.js updated to 11.8.0, and jQuery updated to 3.6.0.

### Bug fixes

#### Relative paths in the nav can traverse above the root

Regression in 1.2 - relative paths in the nav could no longer traverse above the site's root and were truncated to the root. Although such traversal is discouraged and produces a warning, this was a documented behavior. The behavior is now restored.

Context: #2752, #3010

#### MkDocs can accept the config from stdin

This can be used for config overrides on the fly. See updated section at the bottom of [Configuration Inheritance](../user-guide/configuration.md#configuration-inheritance).

The command to use this is `mkdocs build -f -`. In previous versions doing this led to an error.

[Context](https://github.com/properdocs/properdocs/commit/d5bb15fa108da86a8e53fb7d84109d8f8d9d6453)

### New command line flags

* `mkdocs --no-color build` disables color output and line wrapping. This option is also available through an environment variable `NO_COLOR=true`. Context: #3282
* `mkdocs build --no-strict` overrides the `strict` config to `false`. Context: #3254
* `mkdocs build -f -` (described directly above).
* `mkdocs serve --clean` (described above).
* `mkdocs serve --dirty` is the new name of `mkdocs serve --dirtyreload`.

### Deprecations

*   `extra_javascript` underwent a change that can break plugins in rare cases, and it requires attention from theme developers. See respective entries above.

*   Python-Markdown was unpinned from `<3.4`. That version is known to remove functionality. If you are affected by those removals, you can still choose to pin the version for yourself: `Markdown <3.4`. Context: #3222, #2892

*   `mkdocs.utils.warning_filter` now shows a warning about being deprecated. It does nothing since MkDocs 1.2. Consider `get_plugin_logger` or just logging under `mkdocs.plugins.*` instead. Context: #3008

*   Accessing the `_vars` attribute of a `Theme` is deprecated - just access the keys directly.

*   Accessing the `user_configs` attribute of a `Config` is deprecated. Note: instead of `config.user_configs[*]['theme']['custom_dir']`, please use the new attribute `config.theme.custom_dir`.

Other small improvements; see [commit log](https://github.com/properdocs/properdocs/compare/1.4.3...1.5.0).

## Version 1.4.3 (2023-05-02)

*   Bugfix: for the `hooks` feature, modules no longer fail to load if using some advanced Python features like dataclasses (#3193)

*   Bugfix: Don't create `None` sitemap entries if the page has no populated URL - affects sites that exclude some files from navigation ([`07a297b`](https://github.com/properdocs/properdocs/commit/07a297b3b4de4a1b49469b1497ee34039b9f38fa))

*   "readthedocs" theme:
    * Accessibility: add aria labels to Home logo (#3129) and search inputs (#3046)
    * "readthedocs" theme now supports `hljs_style:` config, same as "mkdocs" theme (#3199)

*   Translations:
    * Built-in themes now also support Indonesian language (#3154)
    * Fixed `zh_CN` translation (#3125)
    * `tr_TR` translation becomes just `tr` - usage should remain unaffected (#3195)

See [commit log](https://github.com/properdocs/properdocs/compare/1.4.2...1.4.3).

## Version 1.4.2 (2022-11-01)

*   Officially support Python 3.11 (#3020)

    NEW: **Tip:** Simply upgrading to Python 3.11 can cut off 10-15% of your site's build time.

*   Support multiple instances of the same plugin (#3027)

    If a plugin is specified multiple times in the list under the `plugins:` config, that will create 2 (or more) instances of the plugin with their own config each.

    Previously this case was unforeseen and, as such, bugged.

    Now even though this works, by default a warning will appear from MkDocs anyway, unless the plugin adds a class variable `supports_multiple_instances = True`.

*   Bugfix (regression in 1.4.1): Don't error when a plugin puts a plain string into `warnings` (#3016)

*   Bugfix: Relative links will always render with a trailing slash (#3022)

    Previously under `use_directory_urls`, links *from* a sub-page *to* the main index page rendered as e.g. `<a href="../..">` even though in all other cases the links look like `<a href="../../">`. This caused unwanted behavior on some combinations of Web browsers and servers. Now this special-case bug was removed.

*   Built-in "mkdocs" theme now also supports Norwegian language (#3024)

*   Plugin-related warnings look more readable (#3016)

See [commit log](https://github.com/properdocs/properdocs/compare/1.4.1...1.4.2).

## Version 1.4.1 (2022-10-15)

*   Support theme-namespaced plugin loading (#2998)

    Plugins' entry points can be named as 'sometheme/someplugin'. That will have the following outcome:

    * If the current theme is 'sometheme', the plugin 'sometheme/someplugin' will always be preferred over 'someplugin'.
    * If the current theme *isn't* 'sometheme', the only way to use this plugin is by specifying `plugins: [sometheme/someplugin]`.

    One can also specify `plugins: ['/someplugin']` instead of `plugins: ['someplugin']` to definitely avoid the theme-namespaced plugin.

*   Bugfix: `mkdocs serve` will work correctly with non-ASCII paths and redirects (#3001)

*   Windows: 'colorama' is now a dependency of MkDocs, to ensure colorful log output (#2987)

*   Plugin-related config options have more reliable validation and error reporting (#2997)

*   Translation sub-commands of `setup.py` were completely dropped. See documentation [[1]](../about/contributing.md#submitting-changes-to-the-builtin-themes) [[2]](../dev-guide/translations.md#updating-the-translation-catalogs) for their new replacements (#2990)

*   The ['mkdocs' package](https://pypi.org/project/mkdocs/#files) (wheel and source) is now produced by Hatch build system and pyproject.toml instead of setup.py (#2988)

Other small improvements; see [commit log](https://github.com/properdocs/properdocs/compare/1.4.0...1.4.1).

## Version 1.4.0 (2022-09-27)

### Feature upgrades

#### Hooks (#2978)

The new `hooks:` config allows you to add plugin-like event handlers from local Python files, without needing to set up and install an actual plugin.

See [**documentation**](../user-guide/configuration.md#hooks).

#### `edit_uri` flexibility (#2927)

There is a new `edit_uri_template:` config.  
It works like `edit_uri` but more generally covers ways to construct an edit URL.  
See [**documentation**](../user-guide/configuration.md#edit_uri_template).

Additionally, the `edit_uri` functionality will now fully work even if `repo_url` is omitted (#2928)

### Upgrades for plugin developers

NOTE: This release has big changes to the implementation of plugins and their configs. But, the intention is to have zero breaking changes in all reasonably common use cases. Or at the very least if a code fix is required, there should always be a way to stay compatible with older MkDocs versions. Please report if this release breaks something.

#### Customize event order for plugin event handlers (#2973)

Plugins can now choose to set a priority value for their event handlers. This can override the old behavior where for each event type, the handlers are called in the order that their plugins appear in the [`plugins` config](../user-guide/configuration.md#plugins).

If this is set, events with higher priority are called first. Events without a chosen priority get a default of 0. Events that have the same priority are ordered as they appear in the config.

Recommended priority values: `100` "first", `50` "early", `0` "default", `-50` "late", `-100` "last".  
As different plugins discover more precise relations to each other, the values should be further tweaked.

See [**documentation**](../dev-guide/plugins.md#event-priorities).

#### New events that persist across builds in `mkdocs serve` (#2972)

The new events are `on_startup` and `on_shutdown`. They run at the very beginning and very end of an `mkdocs` invocation.  
`on_startup` also receives information on how `mkdocs` was invoked (e.g. `serve` `--dirtyreload`).

See [**documentation**](../dev-guide/plugins.md#events).

#### Replace `File.src_path` to not deal with backslashes (#2930)

The property `src_path` uses backslashes on Windows, which doesn't make sense as it's a virtual path.  
To not make a breaking change, there's no change to how *this* property is used, but now you should:

* Use **`File.src_uri`** instead of `File.src_path`
* and **`File.dest_uri`** instead of `File.dest_path`.

These consistently use forward slashes, and are now the definitive source that MkDocs itself uses.

See [source code](https://github.com/properdocs/properdocs/blob/1.4.0/mkdocs/structure/files.py#L151).

As a related tip: you should also stop using `os.path.*` or `pathlib.Path()` to deal with these paths, and instead use `posixpath.*` or `pathlib.PurePosixPath()`

#### MkDocs is type-annotated, ready for use with [mypy](https://mypy.readthedocs.io/) (#2941, #2970)

##### Type annotations for event handler methods (#2931)

MkDocs' plugin event methods now have type annotations. You might have been adding annotations to events already, but now they will be validated to match the original.

See [source code](https://github.com/properdocs/properdocs/blob/1.4.0/mkdocs/plugins.py#L165) and [documentation](../dev-guide/plugins.md#events).

One big update is that now you should annotate method parameters more specifically as `config: defaults.ProperDocsConfig` instead of `config: base.Config`. This not only makes it clear that it is the [main config of MkDocs itself](https://github.com/properdocs/properdocs/blob/1.4.0/mkdocs/config/defaults.py), but also provides type-safe access through attributes of the object (see next section).

See [source code](https://github.com/properdocs/properdocs/blob/1.4.0/mkdocs/config/defaults.py) and [documentation](../dev-guide/plugins.md#on_event_name).

#### Rework ConfigOption schemas as class-based (#2962)

When developing a plugin, the settings that it accepts used to be specified in the `config_scheme` variable on the plugin class.  
This approach is now soft-deprecated, and instead you should specify the config in a sub-class of `base.Config`.

Old example:

```python
from mkdocs import plugins
from mkdocs.config import base, config_options

class MyPlugin(plugins.BasePlugin):
    config_scheme = (
        ('foo', config_options.Type(int)),
        ('bar', config_options.Type(str, default='')),
    )

    def on_page_markdown(self, markdown: str, *, config: base.Config, **kwargs):
        if self.config['foo'] < 5:
            if config['site_url'].startswith('http:'):
                return markdown + self.config['baz']
```

This code snippet actually has many mistakes but it will pass all type checks and silently run and even succeed in some cases.

So, on to the new equivalent example, changed to new-style schema and attribute-based access:  
(Complaints from "mypy" added inline)

```python
from mkdocs import plugins
from mkdocs.config import base, config_options as c

class MyPluginConfig(base.Config):
    foo = c.Optional(c.Type(int))
    bar = c.Type(str, default='')

class MyPlugin(plugins.BasePlugin[MyPluginConfig]):
    def on_page_markdown(self, markdown: str, *, config: defaults.ProperDocsConfig, **kwargs):
        if self.config.foo < 5:  # Error, `foo` might be `None`, need to check first.
            if config.site_url.startswith('http:'):  # Error, MkDocs' `site_url` also might be `None`.
                return markdown + self.config.baz  # Error, no such attribute `baz`!
```

This lets you notice the errors from a static type checker before running the code and fix them as such:

```python
class MyPlugin(plugins.BasePlugin[MyPluginConfig]):
    def on_page_markdown(self, markdown: str, *, config: defaults.ProperDocsConfig, **kwargs):
        if self.config.foo is not None and self.config.foo < 5:  # OK, `int < int` is valid.
            if (config.site_url or '').startswith('http:'):  # OK, `str.startswith(str)` is valid.
                return markdown + self.config.bar  # OK, `str + str` is valid.
```

See [**documentation**](../dev-guide/plugins.md#config_scheme).

Also notice that we had to explicitly mark the config attribute `foo` as `Optional`.  
The new-style config has all attributes marked as required by default, and specifying `required=False` or `required=True` is not allowed!

##### New: `config_options.Optional` (#2962)

Wrapping something into `Optional` is conceptually similar to "I want the default to be `None`" -- and you *have* to express it like that, because writing `default=None` doesn't actually work.

Breaking change: the method `BaseConfigOption.is_required()` was removed. Use `.required` instead. (#2938)  
And even the `required` property should be mostly unused now.  
For class-based configs, there's a new definition for whether an option is "required":

* It has no default, and
* It is not wrapped into `config_options.Optional`.

##### New: `config_options.ListOfItems` (#2938)

Defines a list of items that each must adhere to the same constraint. Kind of like a validated `Type(list)`

Examples how to express a list of integers (with `from mkdocs.config import config_options as c`):

Description | Code entry
----------- | ----------
Required to specify | `foo = c.ListOfItems(c.Type(int))`
Optional, default is [] | `foo = c.ListOfItems(c.Type(int), default=[])`
Optional, default is None | `foo = c.Optional(c.ListOfItems(c.Type(int)))`

See more [examples in **documentation**](../dev-guide/plugins.md#examples-of-config-definitions).

##### Updated: `config_options.SubConfig` (#2807)

`SubConfig` used to silently ignore all validation of its config options. Now you should pass `validate=True` to it or just use new class-based configs where this became the default.

So, it can be used to validate a nested sub-dict with all keys pre-defined and value types strictly validated.

See [examples in **documentation**](../dev-guide/plugins.md#examples-of-config-definitions).

#### Other changes to config options

`URL`'s default is now `None` instead of `''`. This can still be checked for truthiness in the same way - `if config.some_url:` (#2962)

`FilesystemObject` is no longer abstract and can be used directly, standing for "file or directory" with optional existence checking (#2938)

Bug fixes:

* Fix `SubConfig`, `ConfigItems`, `MarkdownExtensions` to not leak values across different instances (#2916, #2290)
* `SubConfig` raises the correct kind of validation error without a stack trace (#2938)
* Fix dot-separated redirect in `config_options.Deprecated(moved_to)` (#2963)

Tweaked logic for handling `ConfigOption.default` (#2938)

Deprecated config option classes: `ConfigItems` (#2983), `OptionallyRequired` (#2962), `RepoURL` (#2927)

### Theme updates

*   Styles of admonitions in "MkDocs" theme (#2981):
    * Update colors to increase contrast
    * Apply admonition styles also to `<details>` tag, to support Markdown extensions that provide it ([pymdownx.details](https://facelessuser.github.io/pymdown-extensions/extensions/details/), [callouts](https://oprypin.github.io/markdown-callouts/#collapsible-blocks))

*   Built-in themes now also support these languages:
    * Russian (#2976)
    * Turkish (Turkey) (#2946)
    * Ukrainian (#2980)

### Future compatibility

*   `extra_css:` and `extra_javascript:` warn if a backslash `\` is passed to them. (#2930, #2984)

*   Show `DeprecationWarning`s as INFO messages. (#2907)

    If any plugin or extension that you use relies on deprecated functionality of other libraries, it is at risk of breaking in the near future. Plugin developers should address these in a timely manner.

*   Avoid a dependency on `importlib_metadata` starting from Python 3.10 (#2959)

*   Drop support for Python 3.6 (#2948)

#### Incompatible changes to public APIs

*   `mkdocs.utils`:
    * `create_media_urls` and `normalize_url` warn if a backslash `\` is passed to them. (#2930)
    * `is_markdown_file` stops accepting case-insensitive variants such as `.MD`, which is how MkDocs build was already operating. (#2912)
    * Hard-deprecated: `modified_time`, `reduce_list`, `get_html_path`, `get_url_path`, `is_html_file`, `is_template_file`. (#2912)

### Miscellaneous

*   If a plugin adds paths to `watch` in `LiveReloadServer`, it can now `unwatch` them. (#2777)

*   Bugfix (regression in 1.2): Support listening on an IPv6 address in `mkdocs serve`. (#2951)

Other small improvements; see [commit log](https://github.com/properdocs/properdocs/compare/1.3.1...1.4.0).

## Version 1.3.1 (2022-07-19)

*   Pin Python-Markdown version to &lt;3.4, thus excluding its latest release that breaks too many external extensions (#2893)

*   When a Markdown extension fails to load, print its name and traceback (#2894)

*   Bugfix for "readthedocs" theme (regression in 1.3.0): add missing space in breadcrumbs (#2810)

*   Bugfix: don't complain when a file "readme.md" (lowercase) exists, it's not recognized otherwise (#2852)

*   Built-in themes now also support these languages:
    * Italian (#2860)

Other small improvements; see [commit log](https://github.com/properdocs/properdocs/compare/1.3.0...1.3.1).

## Version 1.3.0 (2022-03-26)

### Feature upgrades

*   ReadTheDocs theme updated from v0.4.1 to v1.0.0 according to upstream (#2585)

    The most notable changes:

    * New option `logo`: Rather than displaying the `site_name` in the title, one can specify a path to an image to display instead.
    * New option `anonymize_ip` for Google Analytics.
    * Dependencies were upgraded: jQuery upgraded to 3.6.0, Modernizr.js dropped, and others.

    See [documentation of config options for the theme](../user-guide/choosing-your-theme.md#readthedocs)

*   Built-in themes now also support these languages:
    * German (#2633)
    * Persian (Farsi) (#2787)

*   Support custom directories to watch when running `mkdocs serve` (#2642)

    MkDocs by default watches the *docs* directory and the config file. Now there is a way to add more directories to watch for changes, either via the YAML `watch` key or the command line flag `--watch`.

    Normally MkDocs never reaches into any other directories (so this feature shouldn't be necessary), but some plugins and extensions may do so.

    See [documentation](https://properdocs.org/user-guide/configuration/#watch).

*   New `--no-history` option for `gh_deploy` (#2594)

    Allows to discard the history of commits when deploying, and instead replace it with one root commit

### Bug fixes

*   An XSS vulnerability when using the search function in built-in themes was fixed (#2791)

*   Setting the `edit_uri` option no longer erroneously adds a trailing slash to `repo_url` (#2733)

### Miscellaneous

*   Breaking change: the `pages` config option that was deprecated for a very long time now causes an error when used (#2652)

    To fix the error, just change from `pages` to `nav`.

*   Performance optimization: during startup of MkDocs, code and dependencies of other commands will not be imported (#2714)

    The most visible effect of this is that dependencies of `mkdocs serve` will not be imported when `mkdocs build` is used.

*   Recursively validate `nav` (#2680)

    Validation of the nested `nav` structure has been reworked to report errors early and reliably. Some [edge cases](https://github.com/properdocs/properdocs/blob/b7272150bbc9bf8f66c878f6517742de3528972b/mkdocs/tests/config/config_options_tests.py#L783) have been declared invalid.

Other small improvements; see [commit log](https://github.com/properdocs/properdocs/compare/1.2.3...1.3.0).

## Version 1.2.4 (2022-03-26)

*   Compatibility with Jinja2 3.1.0 (#2800)

    Due to a breaking change in Jinja2, MkDocs would crash with the message
    `AttributeError: module 'jinja2' has no attribute 'contextfilter'`

## Version 1.2.3 (2021-10-12)

*   Built-in themes now also support these languages:
    * Simplified Chinese (#2497)
    * Japanese (#2525)
    * Brazilian Portuguese (#2535)
    * Spanish (#2545, previously #2396)

*   Third-party plugins will take precedence over built-in plugins with the same name (#2591)

*   Bugfix: Fix ability to load translations for some languages: core support (#2565) and search plugin support with fallbacks (#2602)

*   Bugfix (regression in 1.2): Prevent directory traversal in the dev server (#2604)

*   Bugfix (regression in 1.2): Prevent webserver warnings from being treated as a build failure in strict mode (#2607)

*   Bugfix: Correctly print colorful messages in the terminal on Windows (#2606)

*   Bugfix: Python version 3.10 was displayed incorrectly in `--version` (#2618)

Other small improvements; see [commit log](https://github.com/properdocs/properdocs/compare/1.2.2...1.2.3).

## Version 1.2.2 (2021-07-18)

*   Bugfix (regression in 1.2): Fix serving files/paths with Unicode characters (#2464)

*   Bugfix (regression in 1.2): Revert livereload file watching to use polling observer (#2477)

    This had to be done to reasonably support usages that span virtual filesystems such as non-native Docker and network mounts.

    This goes back to the polling approach, very similar to that was always used prior, meaning most of the same downsides with latency and CPU usage.

*   Revert from 1.2: Remove the requirement of a `site_url` config and the restriction on `use_directory_urls` (#2490)

*   Bugfix (regression in 1.2): Don't require trailing slash in the URL when serving a directory index in `mkdocs serve` server (#2507)

    Instead of showing a 404 error, detect if it's a directory and redirect to a path with a trailing slash added, like before.

*   Bugfix: Fix `gh_deploy` with config-file in the current directory (#2481)

*   Bugfix: Fix reversed breadcrumbs in "readthedocs" theme (#2179)

*   Allow "mkdocs.yaml" as the file name when '--config' is not passed (#2478)

*   Stop treating ";" as a special character in URLs: urlparse -> urlsplit (#2502)

*   Improve build performance for sites with many pages (partly already done in 1.2) (#2407)

## Version 1.2.1 (2021-06-09)

* Bugfix (regression in 1.2): Ensure 'gh-deploy' always pushes.

## Version 1.2 (2021-06-04)

### Major Additions to Version 1.2

#### Support added for Theme Localization (#2299)

The `mkdocs` and `readthedocs` themes now support language localization using
the `theme.locale` parameter, which defaults to `en` (English). The only other
supported languages in this release are `fr` (French) and `es` (Spanish). For
details on using the provided translations, see the [user
guide](../user-guide/localizing-your-theme.md). Note that translation will not
happen by default. Users must first install the necessary dependencies with
the following command:

```bash
pip install 'mkdocs[i18n]'
```

Translation contributions are welcome and detailed in the [Translation
Guide](../dev-guide/translations.md).

Developers of third party themes may want to review the relevant section of
the [Theme Development
Guide](../dev-guide/themes.md#supporting-theme-localizationtranslation).

Contributors who are updating the templates to the built-in themes should
review the [Contributing
Guide](contributing.md#submitting-changes-to-the-builtin-themes).

The `lang` setting of the `search` plugin now defaults to the language
specified in `theme.locale`.

#### Support added for Environment Variables in the configuration file (#1954)

Environments variables may now be specified in the configuration file with the
`!ENV` tag. The value of the variable will be parsed by the YAML parser and
converted to the appropriate type.

```yaml
somekey: !ENV VAR_NAME
otherkey: !ENV [VAR_NAME, FALLBACK_VAR, 'default value']
```

See [Environment Variables](../user-guide/configuration.md#environment-variables)
in the Configuration documentation for details.

#### Support added for Configuration Inheritance (#2218)

A configuration file may now inherit from a parent configuration file. In the
primary file set the `INHERIT` key to the relative path of the parent file.

```yaml
INHERIT: path/to/base.yml
```

The two files will then be deep merged. See
[Configuration Inheritance](../user-guide/configuration.md#configuration-inheritance)
for details.

#### Update `gh-deploy` command (#2170)

The vendored (and modified) copy of ghp_import has been replaced with a
dependency on the upstream library. As of version 1.0.0, [ghp-import] includes a
Python API which makes it possible to call directly.

MkDocs can now benefit from recent bug fixes and new features, including the following:

* A `.nojekyll` file is automatically included when deploying to GitHub Pages.
* The `--shell` flag is now available, which reportedly works better on Windows.
* Git author and committer environment variables should be respected (#1383).

[ghp-import]: https://github.com/c-w/ghp-import/

#### Rework auto-reload and HTTP server for `mkdocs serve` (#2385)

`mkdocs serve` now uses a new underlying server + file watcher implementation,
based on [http.server] from standard library and [watchdog]. It provides similar
functionality to the previously used [livereload] library (which is now dropped
from dependencies, along with [tornado]).

This makes reloads more responsive and consistent in terms of timing. Multiple
rapid file changes no longer cause the site to repeatedly rebuild (issue #2061).

Almost every aspect of the server is slightly different, but actual visible
changes are minor. The logging outputs are only *similar* to the old ones.
Degradations in behavior are not expected, and should be reported if found.

[http.server]: https://docs.python.org/3/library/http.server.html
[watchdog]: https://pypi.org/project/watchdog/
[livereload]: https://pypi.org/project/livereload/
[tornado]: https://pypi.org/project/tornado/

##### Offset the local site root according to the sub-path of the `site_url` (#2424)

When using `mkdocs serve` and having the `site_url` specified as e.g.
`http://example.org/sub/path/`, now the root of the locally served site
becomes `http://127.0.0.1:8000/sub/path/` and all document paths are offset
accordingly.

#### A `build_error` event was added (#2103)

Plugin developers can now use the `on_build_error` hook
to execute code when an exception is raised while building the site.

See [`on_build_error`](../dev-guide/plugins.md#on_build_error)
in the Plugins documentation for details.

#### Three new exceptions: BuildError PluginError and Abort (#2103)

MkDocs now has tree new exceptions defined in `mkdocs.exceptions`:
`BuildError`, `PluginError`, and `Abort`:

* `PluginError` can be raised from a plugin to stop the build and log an error message *without traceback*.
* `BuildError` should not be used by third-party plugins developers and is reserved for internal use only.
* `Abort` is used internally to abort the build and display an error without a traceback.

See [`Handling errors`](../dev-guide/plugins.md#handling-errors)
in the Plugins documentation for details.

#### Search Indexing Strategy configuration

Users can now specify which strategy they wish to use when indexing
their site for search. A user can select between the following options:

* **full**: Adds page title, section headings, and full page text to the search index.
* **sections**: Adds page titles and section headings only to the search index.
* **titles**: Adds only the page titles to the search index.

See [`Search Indexing`](../user-guide/configuration.md#indexing) in the
configuration documentation for details.

### Backward Incompatible Changes in 1.2

*   The [site_url](../user-guide/configuration.md#site_url) configuration option
    is now **required**. If it is not set, a warning will be issued. In a future
    release an error will be raised (#2189).

    The [use_directory_urls](../user-guide/configuration.md#use_directory_urls)
    configuration option will be forced to `false` if
    [site_url](../user-guide/configuration.md#site_url) is set to an empty
    string. In that case, if `use_directory_urls` is not explicitly set to
    `false`, a warning will be issued (#2189).

    NOTE: This was reverted in release 1.2.2

*   The `google_analytics` configuration option is deprecated as Google appears to
    be phasing it out in favor of its new Google Analytics 4 property. See the
    documentation for your theme for alternatives which can be configured as part
    of your theme configuration. For example, the [mkdocs][mkdocs-theme] and
    [readthedocs][rtd-theme] themes have each added a new `theme.analytics.gtag`
    configuration option which uses the new Google Analytics 4 property. See
    Google's documentation on how to [Upgrade to a Google Analytics 4
    property][ga4]. Then set  `theme.analytics.gtag` to the "G-" ID and delete the
    `google_analytics` configuration option which contains a "UA-" ID. So long
    as the old "UA-" ID and new "G-" ID are properly linked in your Google
    account, and you are using the "G-" ID, the data will be made available in
    both the old and new formats by Google Analytics. See #2252.

*   A theme's files are now excluded from the list of watched files by default
    when using the `--livereload` server. This new default behavior is what most
    users need and provides better performance when editing site content.
    Theme developers can enable the old behavior with the `--watch-theme`
    option. (#2092).

*   The `mkdocs` theme now removes the sidebar when printing a page. This frees
    up horizontal space for better rendering of content like tables (#2193).

*   The `mkdocs.config.DEFAULT_SCHEMA` global variable has been replaced with the
    function `mkdocs.config.defaults.get_schema()`, which ensures that each
    instance of the configuration is unique (#2289).

*   The `mkdocs.utils.warning_filter` is deprecated and now does nothing. Plugins
    should remove any reference to is as it may be deleted in a future release.
    To ensure any warnings get counted, simply log them to the `mkdocs` log (i.e.:
    `mkdocs.plugins.pluginname`).

*   The `on_serve` event (which receives the `server` object and the `builder`
    function) is affected by the server rewrite. `server` is now a
    `mkdocs.livereload.LiveReloadServer` instead of `livereload.server.Server`.
    The typical action that plugins can do with these is to call
    `server.watch(some_dir, builder)`, which basically adds that directory to
    watched directories, causing the site to be rebuilt on file changes. That
    still works, but passing any other function to `watch` is deprecated and shows
    a warning. This 2nd parameter is already optional, and will accept only this
    exact `builder` function just for compatibility.

*   The `python` method of the `plugins.search.prebuild_index` configuration
    option is pending deprecation as of version 1.2. It is expected that in
    version 1.3 it will raise a warning if used and in version 1.4 it will raise
    an error. Users are encouraged to use an alternate method to generate a
    prebuilt index for search.

*   The `lunr` and `lunr[languages]` dependencies are no longer installed by
    default. The dependencies are only needed for the rare user who pre-builds the
    search index and uses the `python` option, which is now pending deprecation.
    If you use this feature, then you will need to manually install `lunr` and
    `lunr[languages]`. A warning is issued if the dependencies are needed but not
    installed.

[mkdocs-theme]: ../user-guide/choosing-your-theme.md#mkdocs
[rtd-theme]: ../user-guide/choosing-your-theme.md#readthedocs
[ga4]: https://support.google.com/analytics/answer/9744165?hl=en

### Other Changes and Additions to Version 1.2

* Bugfix: Properly process navigation child items in `_get_by_type` when filtering for sections (#2203).
* Official support for Python 3.9 has been added and support for Python 3.5 has been dropped.
* Bugfix: Fixes an issue that would result in a partially cut-off navigation item in the ReadTheDocs theme (#2297).
* Structure Files object now has a `remove` method to help plugin developers manipulate the Files tree. The corresponding `src_paths` has become a property to accommodate this possible dynamic behavior. See #2305.
* Updated highlight.js to 10.5.0. See #2313.
* Bugfix: Search plugin now works with Japanese language. See #2178.
* Documentation has been refactored (#1629).
* Restore styling of tables in the `readthedocs` theme (#2028).
* Ensure `site_url` ends with a slash (#1785).
* Correct documentation of `pages` template context variable (#1736).
* The `lunr` dependency has been updated to 0.5.9, and `lunr.js` to the corresponding 2.3.9 version (#2306).
* Color is now used in log messages to identify errors, warnings and debug messages.
* Bugfix: Identify homepage when `use_directory_urls` is `False` (#2362).

## Older versions

Older versions (of MkDocs) can be found at <https://www.mkdocs.org/about/release-notes/>
