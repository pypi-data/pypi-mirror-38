#!/usr/bin/env python

"""
setup.py

===============================================================================

    Copyright (C) 2015-2018 Rudolf Cardinal (rudolf@pobox.com).

    This file is part of CRATE.

    CRATE is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    CRATE is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with CRATE. If not, see <http://www.gnu.org/licenses/>.

===============================================================================

CRATE setup file

To use:

    python setup.py sdist --extras

    twine upload dist/*

To install in development mode:

    pip install -e .

More reasoning is in the setup.py file for CamCOPS.
"""
# https://packaging.python.org/en/latest/distributing/#working-in-development-mode  # noqa
# http://python-packaging-user-guide.readthedocs.org/en/latest/distributing/
# http://jtushman.github.io/blog/2013/06/17/sharing-code-across-applications-with-python/  # noqa

import argparse
from setuptools import find_packages, setup
from codecs import open
import fnmatch
import os
import platform
from pprint import pformat
import shutil
import sys
from typing import List

from crate_anon.version import CRATE_VERSION


# =============================================================================
# Helper functions
# =============================================================================

# Files not to bundle
SKIP_PATTERNS = ['*.pyc', '~*']


def add_all_files(root_dir: str,
                  filelist: List[str],
                  absolute: bool = False,
                  include_n_parents: int = 0,
                  verbose: bool = True,
                  skip_patterns: List[str] = None) -> None:
    skip_patterns = skip_patterns or SKIP_PATTERNS
    if absolute:
        base_dir = root_dir
    else:
        base_dir = os.path.abspath(
            os.path.join(root_dir, *(['..'] * include_n_parents)))
    for dir_, subdirs, files in os.walk(root_dir, topdown=True):
        if absolute:
            final_dir = dir_
        else:
            final_dir = os.path.relpath(dir_, base_dir)
        for filename in files:
            _, ext = os.path.splitext(filename)
            final_filename = os.path.join(final_dir, filename)
            if any(fnmatch.fnmatch(final_filename, pattern)
                   for pattern in skip_patterns):
                if verbose:
                    print("Skipping: {}".format(final_filename))
                continue
            if verbose:
                print("Adding: {}".format(final_filename))
            filelist.append(final_filename)


# =============================================================================
# Constants
# =============================================================================

# Arguments
EXTRAS_ARG = 'extras'

# Directories
THIS_DIR = os.path.abspath(os.path.dirname(__file__))  # .../crate
CRATE_ROOT_DIR = os.path.join(THIS_DIR, "crate_anon")  # .../crate/crate_anon/
# DOC_ROOT_DIR = os.path.join(CRATE_ROOT_DIR, "docs")
DOC_ROOT_DIR = os.path.join(THIS_DIR, "docs")
DOC_HTML_DIR = os.path.join(DOC_ROOT_DIR, "build", "html")
EGG_DIR = os.path.join(THIS_DIR, "crate_anon.egg-info")

# Files
DOCMAKER = os.path.join(DOC_ROOT_DIR, "rebuild_docs.py")
MANIFEST_FILE = os.path.join(THIS_DIR, 'MANIFEST.in')  # we will write this
PIP_REQ_FILE = os.path.join(THIS_DIR, 'requirements.txt')

# OS; setup.py is executed on the destination system at install time, so:
RUNNING_WINDOWS = platform.system() == 'Windows'

# Get the long description from the README file
with open(os.path.join(THIS_DIR, 'README.rst'), encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()

# Package dependencies
INSTALL_REQUIRES = [
    'amqp==2.3.2',  # amqp is used by Celery  # noqa
    'arrow==0.12.1',  # better datetime
    'beautifulsoup4==4.6.0',
    'cardinal_pythonlib==1.0.33',
    'celery==4.0.1',  # 4.0.1 is the highest that'll accept kombu 4.0.1 and thus amqp 2.1.3  # noqa
    'chardet==3.0.4',  # character encoding detection for cardinal_pythonlib  # noqa
    'cherrypy==16.0.2',  # Cross-platform web server
    'colorlog==3.1.4',  # colour in logs
    'distro==1.3.0',  # replaces platform.linux_distribution
    'django==2.1.2',
    'django-debug-toolbar==1.10.1',
    # 'django-debug-toolbar-template-profiler==1.0.1',  # removed 2017-01-30: division by zero when rendering time is zero  # noqa
    'django-extensions==2.0.7',
    'django-picklefield==1.0.0',  # NO LONGER USED - dangerous to use pickle - but kept for migrations  # noqa
    # 'django-silk==0.5.7',
    'django-sslserver==0.20',
    'flashtext==2.7',
    'flower==0.9.2',  # debug Celery; web server; only runs explicitly
    'gunicorn==19.8.1',  # UNIX only, though will install under Windows
    'kombu==4.1.0',  # requires VC++ under Windows # 'mmh3==2.2',  # MurmurHash, for fast non-cryptographic hashing  # noqa
    'openpyxl==2.5.4',  # for ONSPD
    'pendulum==2.0.2',  # dates/times
    'pdfkit==0.6.1',
    'prettytable==0.7.2',
    'psutil==5.4.6',  # process management
    'pygments==2.2.0',  # syntax highlighting
    # REMOVED in version 0.18.42; needs Visual C++ under Windows  # 'pyhashxx==0.1.3',  # fast non-cryptographic hashing  # noqa
    'pyparsing==2.2.0',  # generic grammar parser
    'PyPDF2==1.26.0',
    # 'pytz==2016.10',
    'python-dateutil==2.6.0',
    # 'python-docx==0.8.5',  # needs lxml, which has Visual C++ dependencies under Windows  # noqa
    # ... https://python-docx.readthedocs.org/en/latest/user/install.html
    'regex==2018.6.21',
    'semver==2.8.0',  # comparing semantic versions
    'sortedcontainers==2.0.4',
    'SQLAlchemy==1.2.8',  # database access
    'sqlparse==0.2.4',
    'typing==3.6.4',  # part of stdlib in Python 3.5, but not 3.4
    'unidecode==1.0.22',  # for removing accents
    'Werkzeug==0.14.1',
    'xlrd==1.1.0',  # for ONSPD

    # ---------------------------------------------------------------------
    # For database connections (see manual): install manually
    # ---------------------------------------------------------------------
    # MySQL: one of:
    #   'PyMySQL',
    #   'mysqlclient',
    # SQL Server / ODBC route:
    #   'django-pyodbc-azure',
    #   'pyodbc',  # has C prerequisites
    #   'pypyodbc==1.3.3',
    # SQL Server / Embedded FreeTDS route:
    #   'django-pymssql',
    #   'django-mssql',
    #   'pymssql',
    # PostgreSQL:
    #   'psycopg2',  # has prerequisites (e.g. pg_config executable)

]

if RUNNING_WINDOWS:
    INSTALL_REQUIRES += [
        # Windows-specific stuff
        'pypiwin32==223',
    ]

DEVELOPMENT_ONLY_REQUIRES = [
    'sphinx==1.7.5',  # documentation
]


# =============================================================================
# Helper functions
# =============================================================================

def deltree(path: str, verbose: bool = False) -> None:
    if verbose:
        print("Deleting directory: {}".format(path))
    shutil.rmtree(path, ignore_errors=True)


def add_all_files(root_dir: str,
                  filelist: List[str],
                  absolute: bool = False,
                  relative_to: str = "",
                  include_n_parents: int = 0,
                  verbose: bool = False,
                  skip_patterns: List[str] = None) -> None:
    skip_patterns = skip_patterns or SKIP_PATTERNS
    if absolute or relative_to:
        base_dir = root_dir
    else:
        base_dir = os.path.abspath(
            os.path.join(root_dir, *(['..'] * include_n_parents)))
    for dir_, subdirs, files in os.walk(root_dir, topdown=True):
        if absolute or relative_to:
            final_dir = dir_
        else:
            final_dir = os.path.relpath(dir_, base_dir)
        for filename in files:
            _, ext = os.path.splitext(filename)
            final_filename = os.path.join(final_dir, filename)
            if relative_to:
                final_filename = os.path.relpath(final_filename, relative_to)
            if any(fnmatch.fnmatch(final_filename, pattern)
                   for pattern in skip_patterns):
                if verbose:
                    print("Skipping: {}".format(final_filename))
                continue
            if verbose:
                print("Adding: {}".format(final_filename))
            filelist.append(final_filename)


# =============================================================================
# There's a nasty caching effect. So remove the old ".egg_info" directory
# =============================================================================
# http://blog.codekills.net/2011/07/15/lies,-more-lies-and-python-packaging-documentation-on--package_data-/  # noqa

deltree(EGG_DIR, verbose=True)


# =============================================================================
# If we run this with "python setup.py sdist --extras", we *BUILD* the package
# and do all the extras. (When the end user installs it, that argument will be
# absent.)
# =============================================================================

parser = argparse.ArgumentParser()
parser.add_argument(
    '--' + EXTRAS_ARG, action='store_true',
    help=(
        "USE THIS TO CREATE PACKAGES (e.g. 'python setup.py sdist --{}. "
        "Copies extra info in.".format(EXTRAS_ARG)
    )
)
our_args, leftover_args = parser.parse_known_args()
sys.argv[1:] = leftover_args

extra_files = []  # type: List[str]

SKIP_PATTERNS = ["*.pyc"]

if getattr(our_args, EXTRAS_ARG):
    # Here's where we do the extra stuff.

    # -------------------------------------------------------------------------
    # Add extra files
    # -------------------------------------------------------------------------

    add_all_files(os.path.join(CRATE_ROOT_DIR, 'crateweb/consent/templates'),
                  extra_files, relative_to=THIS_DIR,
                  skip_patterns=SKIP_PATTERNS)
    add_all_files(os.path.join(CRATE_ROOT_DIR, 'crateweb/research/templates'),
                  extra_files, relative_to=THIS_DIR,
                  skip_patterns=SKIP_PATTERNS)
    add_all_files(os.path.join(CRATE_ROOT_DIR, 'crateweb/static'),
                  extra_files, relative_to=THIS_DIR,
                  skip_patterns=SKIP_PATTERNS)
    add_all_files(os.path.join(CRATE_ROOT_DIR, 'crateweb/templates'),
                  extra_files, relative_to=THIS_DIR,
                  skip_patterns=SKIP_PATTERNS)
    add_all_files(os.path.join(CRATE_ROOT_DIR, 'crateweb/userprofile/templates'),
                  extra_files, relative_to=THIS_DIR,
                  skip_patterns=SKIP_PATTERNS)
    add_all_files(os.path.join(CRATE_ROOT_DIR, 'crate_anon/nlp_manager'),
                  extra_files, relative_to=THIS_DIR,
                  skip_patterns=SKIP_PATTERNS)
    add_all_files(os.path.join(CRATE_ROOT_DIR, 'testdocs_for_text_extraction'),
                  extra_files, relative_to=THIS_DIR,
                  skip_patterns=SKIP_PATTERNS)

    extra_files.sort()
    print("EXTRA_FILES: \n{}".format(pformat(extra_files)))

    # -------------------------------------------------------------------------
    # Write the manifest (ensures files get into the source distribution).
    # -------------------------------------------------------------------------
    extra_files.sort()
    print("EXTRA_FILES: \n{}".format(pformat(extra_files)))
    manifest_lines = ['include ' + x for x in extra_files]
    with open(MANIFEST_FILE, 'wt') as manifest:
        manifest.writelines([
            "# This is an AUTOCREATED file, MANIFEST.in; see setup.py and DO "
            "NOT EDIT BY HAND"])
        manifest.write("\n\n" + "\n".join(manifest_lines) + "\n")

    # -------------------------------------------------------------------------
    # Write requirements.txt (helps PyCharm)
    # -------------------------------------------------------------------------
    with open(PIP_REQ_FILE, "w") as req_file:
        for line in INSTALL_REQUIRES:
            req_file.write(line + "\n")


# =============================================================================
# setup args
# =============================================================================

setup(
    name='crate-anon',  # 'crate' is taken

    version=CRATE_VERSION,

    description='CRATE: clinical records anonymisation and text extraction',
    long_description=LONG_DESCRIPTION,

    # The project's main homepage.
    # url='https://github.com/RudolfCardinal/crate',
    url="https://egret.psychol.cam.ac.uk/crate",

    # Author details
    author='Rudolf Cardinal',
    author_email='rudolf@pobox.com',

    # Choose your license
    license='GNU General Public License v3 or later (GPLv3+)',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        'Intended Audience :: Science/Research',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',  # noqa

        'Natural Language :: English',

        'Operating System :: OS Independent',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3 :: Only',

        'Topic :: System :: Hardware',
        'Topic :: System :: Networking',
    ],

    keywords='anonymisation',

    packages=find_packages(),  # finds all the .py files in subdirectories

    package_data={
        'crate_anon': extra_files,
    },

    include_package_data=True,  # use MANIFEST.in during install?
    # https://stackoverflow.com/questions/7522250/how-to-include-package-data-with-setuptools-distribute  # noqa

    install_requires=INSTALL_REQUIRES,

    entry_points={
        'console_scripts': [
            # Format is 'script=module:function".

            # Documentation

            'crate_docs=crate_anon.tools.launch_docs:main',
            'crate_help=crate_anon.tools.launch_docs:main',  # synonym

            # Preprocessing

            'crate_postcodes=crate_anon.preprocess.postcodes:main',
            'crate_preprocess_pcmis=crate_anon.preprocess.preprocess_pcmis:main',  # noqa
            'crate_preprocess_rio=crate_anon.preprocess.preprocess_rio:main',

            # Anonymisation

            'crate_anonymise=crate_anon.anonymise.anonymise_cli:main',
            'crate_anonymise_multiprocess=crate_anon.anonymise.launch_multiprocess_anonymiser:main',  # noqa
            'crate_fetch_wordlists=crate_anon.anonymise.fetch_wordlists:main',
            'crate_make_demo_database=crate_anon.anonymise.make_demo_database:main',  # noqa
            'crate_test_anonymisation=crate_anon.anonymise.test_anonymisation:main',  # noqa
            'crate_test_extract_text=crate_anon.anonymise.test_extract_text:main',  # noqa

            # NLP

            'crate_nlp=crate_anon.nlp_manager.nlp_manager:main',
            'crate_nlp_build_gate_java_interface=crate_anon.nlp_manager.build_gate_java_interface:main',  # noqa
            'crate_nlp_build_medex_itself=crate_anon.nlp_manager.build_medex_itself:main',  # noqa
            'crate_nlp_build_medex_java_interface=crate_anon.nlp_manager.build_medex_java_interface:main',  # noqa
            'crate_nlp_multiprocess=crate_anon.nlp_manager.launch_multiprocess_nlp:main',  # noqa

            # Web site

            'crate_django_manage=crate_anon.crateweb.manage:main',  # will cope with argv  # noqa
            'crate_generate_new_django_secret_key=cardinal_pythonlib.django.tools.generate_new_django_secret_key:main',  # noqa
            'crate_celery_status=crate_anon.tools.celery_status:main',
            'crate_launch_celery=crate_anon.tools.launch_celery:main',
            'crate_launch_cherrypy_server=crate_anon.tools.launch_cherrypy_server:main',  # noqa
            # ... a separate script with ":main" rather than
            # "crate_anon.crateweb.manage:runcpserver" so that we can launch
            # the "runcpserver" function from our Windows service, and have it
            # deal with the CherryPy special environment variable
            'crate_launch_django_server=crate_anon.crateweb.manage:runserver',
            'crate_launch_flower=crate_anon.tools.launch_flower:main',
            'crate_print_demo_crateweb_config=crate_anon.tools.print_crateweb_demo_config:main',  # noqa
            'crate_windows_service=crate_anon.tools.winservice:main',

            # Miscellaneous, from cardinal_pythonlib

            'crate_estimate_mysql_memory_usage=cardinal_pythonlib.tools.estimate_mysql_memory_usage:main',  # noqa
            'crate_list_all_extensions=cardinal_pythonlib.tools.list_all_extensions:main',  # noqa
            'crate_merge_csv=cardinal_pythonlib.tools.merge_csv:main',

        ],
    },
)
