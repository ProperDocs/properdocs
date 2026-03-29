#!/usr/bin/env python

import dataclasses
import os
import unittest

import properdocs
from properdocs import config
from properdocs.config import config_options as c
from properdocs.config import defaults
from properdocs.config.base import ValidationError
from properdocs.exceptions import ConfigurationError
from properdocs.localization import parse_locale
from properdocs.tests.base import dedent, tempdir


@dataclasses.dataclass
class ThemeDir:
    theme: str

    def __eq__(self, other):
        return os.path.basename(other) == f'properdocs_theme_{self.theme}'


class ConfigTests(unittest.TestCase):
    def test_missing_config_file(self):
        with self.assertRaises(ConfigurationError):
            config.load_config(config_file='bad_filename.yaml')

    def test_missing_site_name(self):
        conf = defaults.ProperDocsConfig()
        conf.load_dict({'theme': 'mkdocs'})
        errors, warnings = conf.validate()
        self.assertEqual(
            errors, [('site_name', ValidationError("Required configuration not provided."))]
        )
        self.assertEqual(warnings, [])

    def test_missing_theme(self):
        conf = defaults.ProperDocsConfig(config_file_path='a.yml')
        conf.load_dict({'site_name': 'Example'})
        with self.assertLogs('properdocs') as cm:
            errors, warnings = conf.validate()
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])
        self.assertEqual(
            cm.output,
            [
                "WARNING:properdocs.config.config_options:Please select a theme explicitly in 'a.yml'. Defaulted to 'theme: mkdocs', but this may change in the future."
            ],
        )

    def test_nonexistant_config(self):
        with self.assertRaises(ConfigurationError):
            config.load_config(config_file='/path/that/is/not/real')

    @tempdir()
    def test_invalid_config(self, temp_path):
        file_contents = dedent(
            """
            - ['index.md', 'Introduction']
            - ['index.md', 'Introduction']
            - ['index.md', 'Introduction']
            """
        )
        config_path = os.path.join(temp_path, 'foo.yml')
        with open(config_path, 'w', encoding='utf-8') as config_file:
            config_file.write(file_contents)

        with self.assertRaises(ConfigurationError):
            config.load_config(config_file=open(config_file.name, 'rb'))

    @tempdir()
    def test_config_option(self, temp_path):
        """
        Users can explicitly set the config file using the '--config' option.
        Allows users to specify a config other than the default `properdocs.yml`.
        """
        expected_result = {
            'site_name': 'Example',
            'nav': [{'Introduction': 'index.md'}],
        }
        file_contents = dedent(
            """
            site_name: Example
            theme: mkdocs
            nav:
            - 'Introduction': 'index.md'
            """
        )
        config_path = os.path.join(temp_path, 'properdocs.yml')
        with open(config_path, 'w', encoding='utf-8') as config_file:
            config_file.write(file_contents)
        os.mkdir(os.path.join(temp_path, 'docs'))

        result = config.load_config(config_file=config_file.name)
        self.assertEqual(result['site_name'], expected_result['site_name'])
        self.assertEqual(result['nav'], expected_result['nav'])

    @tempdir()
    @tempdir()
    def test_theme(self, mytheme, custom):
        configs = [
            {},  # default theme
            {"theme": "readthedocs"},  # builtin theme
            {"theme": {'name': 'readthedocs'}},  # builtin as complex
            {"theme": {'name': None, 'custom_dir': mytheme}},  # custom only as complex
            {
                "theme": {'name': 'readthedocs', 'custom_dir': custom}
            },  # builtin and custom as complex
            {  # user defined variables
                'theme': {
                    'name': 'mkdocs',
                    'locale': 'fr',
                    'static_templates': ['foo.html'],
                    'show_sidebar': False,
                    'some_var': 'bar',
                }
            },
        ]

        properdocs_dir = os.path.abspath(os.path.dirname(properdocs.__file__))
        properdocs_templates_dir = os.path.join(properdocs_dir, 'templates')

        results = (
            {
                'dirs': [ThemeDir('mkdocs'), properdocs_templates_dir],
                'static_templates': ['404.html', 'sitemap.xml'],
                'vars': {
                    'name': 'mkdocs',
                    'color_mode': 'light',
                    'user_color_mode_toggle': False,
                    'locale': parse_locale('en'),
                    'include_search_page': False,
                    'search_index_only': False,
                    'analytics': {'gtag': None},
                    'highlightjs': True,
                    'hljs_style': 'github',
                    'hljs_languages': [],
                    'hljs_style_dark': 'github-dark',
                    'navigation_depth': 2,
                    'nav_style': 'primary',
                    'shortcuts': {'help': 191, 'next': 78, 'previous': 80, 'search': 83},
                },
            },
            {
                'dirs': [ThemeDir('readthedocs'), properdocs_templates_dir],
                'static_templates': ['404.html', 'sitemap.xml'],
                'vars': {
                    'name': 'readthedocs',
                    'locale': parse_locale('en'),
                    'include_search_page': True,
                    'search_index_only': False,
                    'analytics': {'anonymize_ip': False, 'gtag': None},
                    'highlightjs': True,
                    'hljs_languages': [],
                    'hljs_style': 'github',
                    'include_homepage_in_sidebar': True,
                    'prev_next_buttons_location': 'bottom',
                    'navigation_depth': 4,
                    'sticky_navigation': True,
                    'logo': None,
                    'titles_only': False,
                    'collapse_navigation': True,
                },
            },
            {
                'dirs': [ThemeDir('readthedocs'), properdocs_templates_dir],
                'static_templates': ['404.html', 'sitemap.xml'],
                'vars': {
                    'name': 'readthedocs',
                    'locale': parse_locale('en'),
                    'include_search_page': True,
                    'search_index_only': False,
                    'analytics': {'anonymize_ip': False, 'gtag': None},
                    'highlightjs': True,
                    'hljs_languages': [],
                    'hljs_style': 'github',
                    'include_homepage_in_sidebar': True,
                    'prev_next_buttons_location': 'bottom',
                    'navigation_depth': 4,
                    'sticky_navigation': True,
                    'logo': None,
                    'titles_only': False,
                    'collapse_navigation': True,
                },
            },
            {
                'dirs': [mytheme, properdocs_templates_dir],
                'static_templates': ['sitemap.xml'],
                'vars': {'name': None, 'locale': parse_locale('en')},
            },
            {
                'dirs': [custom, ThemeDir('readthedocs'), properdocs_templates_dir],
                'static_templates': ['404.html', 'sitemap.xml'],
                'vars': {
                    'name': 'readthedocs',
                    'locale': parse_locale('en'),
                    'include_search_page': True,
                    'search_index_only': False,
                    'analytics': {'anonymize_ip': False, 'gtag': None},
                    'highlightjs': True,
                    'hljs_languages': [],
                    'hljs_style': 'github',
                    'include_homepage_in_sidebar': True,
                    'prev_next_buttons_location': 'bottom',
                    'navigation_depth': 4,
                    'sticky_navigation': True,
                    'logo': None,
                    'titles_only': False,
                    'collapse_navigation': True,
                },
            },
            {
                'dirs': [ThemeDir('mkdocs'), properdocs_templates_dir],
                'static_templates': ['404.html', 'sitemap.xml', 'foo.html'],
                'vars': {
                    'name': 'mkdocs',
                    'color_mode': 'light',
                    'user_color_mode_toggle': False,
                    'locale': parse_locale('fr'),
                    'show_sidebar': False,
                    'some_var': 'bar',
                    'include_search_page': False,
                    'search_index_only': False,
                    'analytics': {'gtag': None},
                    'highlightjs': True,
                    'hljs_style': 'github',
                    'hljs_languages': [],
                    'hljs_style_dark': 'github-dark',
                    'navigation_depth': 2,
                    'nav_style': 'primary',
                    'shortcuts': {'help': 191, 'next': 78, 'previous': 80, 'search': 83},
                },
            },
        )

        for config_contents, result in zip(configs, results):
            with self.subTest(config_contents):
                conf = config.Config(schema=(('theme', c.Theme(default='mkdocs')),))
                conf.load_dict(config_contents)
                errors, warnings = conf.validate()
                self.assertEqual(errors, [])
                self.assertEqual(warnings, [])
                self.assertEqual(result['dirs'], conf['theme'].dirs)
                self.assertEqual(set(result['static_templates']), conf['theme'].static_templates)
                self.assertEqual(result['vars'], dict(conf['theme']))

    def test_empty_nav(self):
        conf = defaults.ProperDocsConfig(
            config_file_path=os.path.join(os.path.abspath('.'), 'properdocs.yml')
        )
        conf.load_dict({'site_name': 'Example', 'theme': 'mkdocs'})
        conf.validate()
        self.assertEqual(conf['nav'], None)

    def test_error_on_pages(self):
        conf = defaults.ProperDocsConfig()
        conf.load_dict(
            {
                'site_name': 'Example',
                'theme': 'mkdocs',
                'pages': ['index.md', 'about.md'],
            }
        )
        errors, warnings = conf.validate()
        exp_error = (
            "The configuration option 'pages' was removed from ProperDocs. Use 'nav' instead."
        )
        self.assertEqual(errors, [('pages', ValidationError(exp_error))])
        self.assertEqual(warnings, [])

    def test_doc_dir_in_site_dir(self):
        test_configs = (
            {'docs_dir': os.path.join('site', 'docs'), 'site_dir': 'site'},
            {'docs_dir': 'docs', 'site_dir': '.'},
            {'docs_dir': '.', 'site_dir': '.'},
            {'docs_dir': 'docs', 'site_dir': ''},
            {'docs_dir': '', 'site_dir': ''},
            {'docs_dir': 'docs', 'site_dir': 'docs'},
        )

        for test_config in test_configs:
            with self.subTest(test_config):
                # Same as the default schema, but don't verify the docs_dir exists.
                conf = config.Config(
                    schema=(
                        ('docs_dir', c.Dir(default='docs')),
                        ('site_dir', c.SiteDir(default='site')),
                    ),
                    config_file_path=os.path.join(os.path.abspath('..'), 'properdocs.yml'),
                )
                conf.load_dict(test_config)

                errors, warnings = conf.validate()

                self.assertEqual(len(errors), 1)
                self.assertEqual(warnings, [])
