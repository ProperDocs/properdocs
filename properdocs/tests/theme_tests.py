import dataclasses
import os
import unittest
from unittest import mock

import properdocs
from properdocs.localization import parse_locale
from properdocs.tests.base import tempdir
from properdocs.theme import Theme

abs_path = os.path.abspath(os.path.dirname(__file__))
properdocs_dir = os.path.abspath(os.path.dirname(properdocs.__file__))
properdocs_templates_dir = os.path.join(properdocs_dir, 'templates')


@dataclasses.dataclass
class ThemeDir:
    theme: str

    def __eq__(self, other):
        return os.path.basename(other) == f'properdocs_theme_{self.theme}'


class ThemeTests(unittest.TestCase):
    def test_simple_theme(self):
        theme = Theme(name='mkdocs')
        self.assertEqual(
            [ThemeDir('mkdocs'), properdocs_templates_dir],
            theme.dirs,
        )
        self.assertEqual(theme.static_templates, {'404.html', 'sitemap.xml'})
        self.assertEqual(
            dict(theme),
            {
                'name': 'mkdocs',
                'color_mode': 'light',
                'user_color_mode_toggle': False,
                'locale': parse_locale('en'),
                'include_search_page': False,
                'search_index_only': False,
                'analytics': {'gtag': None},
                'highlightjs': True,
                'hljs_style': 'github',
                'hljs_style_dark': 'github-dark',
                'hljs_languages': [],
                'navigation_depth': 2,
                'nav_style': 'primary',
                'shortcuts': {'help': 191, 'next': 78, 'previous': 80, 'search': 83},
            },
        )

    @tempdir()
    def test_custom_dir(self, custom):
        theme = Theme(name='mkdocs', custom_dir=custom)
        self.assertEqual(
            [
                custom,
                ThemeDir('mkdocs'),
                properdocs_templates_dir,
            ],
            theme.dirs,
        )

    @tempdir()
    def test_custom_dir_only(self, custom):
        theme = Theme(name=None, custom_dir=custom)
        self.assertEqual(
            theme.dirs,
            [custom, properdocs_templates_dir],
        )

    def static_templates(self):
        theme = Theme(name='mkdocs', static_templates='foo.html')
        self.assertEqual(
            theme.static_templates,
            {'404.html', 'sitemap.xml', 'foo.html'},
        )

    def test_vars(self):
        theme = Theme(name='mkdocs', foo='bar', baz=True)
        self.assertEqual(theme['foo'], 'bar')
        self.assertEqual(theme['baz'], True)
        self.assertTrue('new' not in theme)
        with self.assertRaises(KeyError):
            theme['new']
        theme['new'] = 42
        self.assertTrue('new' in theme)
        self.assertEqual(theme['new'], 42)

    @mock.patch('yaml.load', return_value={})
    def test_no_theme_config(self, m):
        theme = Theme(name='mkdocs')
        self.assertEqual(m.call_count, 1)
        self.assertEqual(theme.static_templates, {'sitemap.xml'})

    def test_inherited_theme(self):
        m = mock.Mock(
            side_effect=[
                {'extends': 'readthedocs', 'static_templates': ['child.html']},
                {'static_templates': ['parent.html']},
            ]
        )
        with mock.patch('yaml.load', m) as m:
            theme = Theme(name='mkdocs')
            self.assertEqual(m.call_count, 2)
            self.assertEqual(
                [
                    ThemeDir('mkdocs'),
                    ThemeDir('readthedocs'),
                    properdocs_templates_dir,
                ],
                theme.dirs,
            )
            self.assertEqual(theme.static_templates, {'sitemap.xml', 'child.html', 'parent.html'})

    def test_empty_config_file(self):
        # Test for themes with *empty* mkdocs_theme.yml.
        # See https://github.com/mkdocs/mkdocs/issues/3699
        m = mock.Mock(
            # yaml.load returns "None" for an empty file
            side_effect=[None]
        )
        with mock.patch('yaml.load', m) as m:
            theme = Theme(name='mkdocs')
            # Should only have the default name and locale __vars set in
            # Theme.__init__()
            self.assertEqual(
                dict(theme),
                {
                    'name': 'mkdocs',
                    'locale': parse_locale('en'),
                },
            )
