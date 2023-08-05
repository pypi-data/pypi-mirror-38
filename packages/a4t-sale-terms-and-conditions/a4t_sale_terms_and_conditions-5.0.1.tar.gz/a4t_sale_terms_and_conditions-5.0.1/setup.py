#!/usr/bin/env python3
# This file is part of Adiczion's Tryton Module.
# The COPYRIGHT and LICENSE files at the top level of this repository
# contains the full copyright notices and license terms.
import io
import os
import re
from configparser import ConfigParser
from setuptools import setup

PREFIX = {
    'terms_and_conditions': 'a4t'
    }


def read(fname):
    return io.open(
        os.path.join(os.path.dirname(__file__), fname),
        'r', encoding='utf-8').read()


def get_require_version(name):
    if minor_version % 2:
        require = '%s >= %s.%s.dev0, < %s.%s'
    else:
        require = '%s >= %s.%s, < %s.%s'
    require %= (name, major_version, minor_version,
        major_version, minor_version + 1)
    return require


config = ConfigParser()
config.read_file(open('tryton.cfg'))
info = dict(config.items('tryton'))
for key in ('depends', 'extras_depend', 'xml'):
    if key in info:
        info[key] = info[key].strip().splitlines()
version = info.get('version', '0.0.1')
major_version, minor_version, _ = version.split('.', 2)
major_version = int(major_version)
minor_version = int(minor_version)
name = 'a4t_sale_terms_and_conditions'

requires = []
for dep in info.get('depends', []):
    if not re.match(r'(ir|res)(\W|$)', dep):
        prefix = PREFIX.get(dep, 'trytond')
        requires.append(get_require_version('{}_{}'.format(prefix, dep)))
requires.append(get_require_version('trytond'))
tests_require = [get_require_version('proteus')]
dependency_links = []
if minor_version % 2:
    dependency_links.append('https://trydevpi.tryton.org/')

setup(name=name,
    version=version,
    author='Adiczion (Christophe CRIER)',
    author_email='support@adiczion.net',
    url='http://adiczion.com/',
    download_url='https://gitlab.com/ate_modules/a4t-sale_terms_and_conditions',
    keywords='tryton sale Terms & Conditions',
    package_dir={'trytond.modules.sale_terms_and_conditions': '.'},
    packages=[
        'trytond.modules.sale_terms_and_conditions',
        'trytond.modules.sale_terms_and_conditions.tests',
        ],
    package_data={
        'trytond.modules.sale_terms_and_conditions': (info.get('xml', [])
            + ['tryton.cfg', 'view/*.xml', 'locale/*.po', '*.fodt',
                'tests/*.rst']),
        },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Plugins',
        'Framework :: Tryton',
        'Intended Audience :: Developers',
        'Intended Audience :: Financial and Insurance Industry',
        'Intended Audience :: Legal Industry',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Natural Language :: English',
        'Natural Language :: French',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Office/Business',
        'Topic :: Office/Business :: Financial :: Accounting',
        ],
    license='GPL-3',
    python_requires='>=3.4',
    install_requires=requires,
    dependency_links=dependency_links,
    zip_safe=False,
    entry_points="""
    [trytond.modules]
    sale_terms_and_conditions = trytond.modules.sale_terms_and_conditions
    """,
    test_suite='tests',
    test_loader='trytond.test_loader:Loader',
    tests_require=tests_require,
    )
