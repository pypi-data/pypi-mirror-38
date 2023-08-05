# coding: utf-8
import os
from setuptools import setup, find_packages
import spreadsheet as package

NAME = 'incolumepy.spreadsheet'
NAMESPACE = NAME.split('.')[:0]
DESCRIPTION = "pacote de iteração com google sheets"
KEYWORDS = 'python incolumepy'
AUTHOR = '@britodfbr'
AUTHOR_EMAIL = 'contato@incolume.com.br'
URL = 'http://www.incolume.com.br'
PROJECT_URLS = {
    'Documentation': 'https://gitlab.com/development-incolume/incolumepy.exceptions/wikis/home',
    'Funding': None,
    'Say Thanks!': None,
    'Source': 'https://gitlab.com/development-incolume/incolumepy.exceptions',
    'Git': 'https://gitlab.com/development-incolume/incolumepy.exceptions.git',
    'Tracker': 'https://gitlab.com/development-incolume/incolumepy.exceptions/issues',
    'Oficial': 'https://pypi.org/project/incolumepy.exceptions/',
}
LICENSE = 'BSD'
CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',
    'Operating System :: OS Independent',
    'Natural Language :: Portuguese (Brazilian)',
    "Programming Language :: Python",
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Topic :: Utilities'
]


with open('README.md')as f:
    readme = f.read()
with open(os.path.join("docs", "HISTORY.rst")) as f:
    history = f.read()
with open(os.path.join('docs', 'EXAMPLES.rst')) as f:
    example = f.read()
with open('CONTRIBUTING.md') as f:
    contibutors = f.read()
with open('CHANGELOG') as f:
    changes = f.read()

VERSION = package.__version__
LONG_DESCRIPTION = '\n\n'.join((
    readme,
    history,
    example,
    contibutors,
    changes))

setup(name=NAME,
      version=VERSION,
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,

      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=CLASSIFIERS,
      keywords=KEYWORDS,
      author=AUTHOR,
      author_email=AUTHOR_EMAIL,
      url=URL,
      project_urls=PROJECT_URLS,
      license=LICENSE,
      namespace_packages=NAMESPACE,
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      test_suite='nose.collector',
      tests_require='nose',
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'pytest',
          'nose',
      ],
      entry_points={
          'console_scripts': [
              'checkinterval = incolumepy.checkinterval.Check:Check.main',
              'interval = incolumepy.checkinterval.Check:Check.interval'
          ],
          'gui_scripts': [
              'baz = my_package_gui:start_func',
          ],
      },

      # entry_points="""
      # -*- Entry points: -*-

      # [distutils.setup_keywords]
      # paster_plugins = setuptools.dist:assert_string_list

      # [egg_info.writers]
      # paster_plugins.txt = setuptools.command.egg_info:write_arg
      # """,
      # paster_plugins = [''],
      )
