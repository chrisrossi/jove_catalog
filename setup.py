##############################################################################
#
# Copyright (c) 2008-2011 Agendaless Consulting and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the BSD-like license at
# http://www.repoze.org/LICENSE.txt.  A copy of the license should accompany
# this distribution.  THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL
# EXPRESS OR IMPLIED WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND
# FITNESS FOR A PARTICULAR PURPOSE
#
##############################################################################

import os
import platform
import sys

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
try:
    README = open(os.path.join(here, 'README.rst')).read()
    CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()
except IOError:
    README = CHANGES = ''

install_requires=[
    'repoze.catalog',
    ]

tests_require = install_requires
if sys.version_info[:2] < (2, 7):
    tests_require = tests_require + ['unittest2']

setup(name='jove_catalog',
      version='0.1a1',
      description=('A local service for Jove which provides search '
                   'capabilities via repoze.catalog.'),
      long_description=README + '\n\n' +  CHANGES,
      classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Framework :: Pylons",
        "License :: Repoze Public License",
        ],
      keywords='search catalog pylons pyramid zodb',
      author="Chris Rossi, Archimedean Company",
      author_email="pylons-devel@googlegroups.com",
      url="http://pylonsproject.org",
      license="BSD-derived (http://www.repoze.org/LICENSE.txt)",
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires = install_requires,
      tests_require = tests_require,
      test_suite="jove_catalog.tests",
      entry_points = """\
          [jove.local_service]
          catalog = jove_catalog.service:CatalogService
      """
      )

