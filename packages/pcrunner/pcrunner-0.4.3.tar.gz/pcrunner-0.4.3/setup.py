#!/usr/bin/env python
# setup.py
# vim: ai et ts=4 sw=4 sts=4 ft=python fileencoding=utf-8

import sys
from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'PyYAML',
]

test_requirements = [
    'pytest',
    'pytest',
    'tox',
]

# Add Python 2.6-specific dependencies
if sys.version_info[:2] < (2, 7):
    requirements.append('argparse')

# Add Windows-specific dependencies
if sys.platform == 'win32':
    requirements.append('pywin32')

setup(
    metadata_version='2.1',
    name='pcrunner',
    version='0.4.3',
    platform=['Linux', 'Windows'],
    supported_platform=['EL6', 'EL7'],
    summary='A module for running Passive Nagios/Icinga Checks',
    description=readme + '\n\n' + history,
    description_content_type="text/x-rst; charset=UTF-8",
    author='Maarten',
    author_email='Maarten <ikmaarten@gmail.com>',
    project_url='https://github.com/maartenq/pcrunner',
    download_url="https://codeload.github.com/maartenq/pcrunner/zip/master",
    scripts=['scripts/check_dummy.py'],
    packages=[
        'pcrunner',
    ],
    package_dir={'pcrunner': 'pcrunner'},
    entry_points={
        'console_scripts': [
            'pcrunner = pcrunner.main:main',
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="ISC license",
    zip_safe=False,
    keywords='pcrunner',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Documentation :: Sphinx',
        'Topic :: System :: Monitoring',
        'Topic :: System :: Systems Administration',
    ],
    test_suite='tests',
    tests_require=test_requirements,
)
