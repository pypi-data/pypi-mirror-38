# -*- coding: utf-8 -*-

"""
SeleniumTestability
"""

import codecs
from os.path import abspath, dirname, join
from setuptools import setup, find_packages

def read_file(filename):
    buff = None
    with open(filename,'r',encoding='utf-8') as f:
        buff = f.read()
    return buff

LIBRARY_NAME = 'SeleniumTestability'
CWD = abspath(dirname(__file__))
VERSION_PATH = join(CWD, 'src', LIBRARY_NAME, 'version.py')
exec(compile(open(VERSION_PATH).read(), VERSION_PATH, 'exec'))

LONG_DESCRIPTION = read_file(join(CWD,'README.md'))
REQUIREMENTS = read_file(join(CWD,'requirements.txt'))

CLASSIFIERS = '''
Development Status :: 3 - Alpha
Topic :: Software Development :: Testing
Operating System :: OS Independent
License :: OSI Approved :: Apache Software License
Programming Language :: Python
Programming Language :: Python :: 3
Topic :: Software Development :: Testing
Framework :: Robot Framework
Framework :: Robot Framework :: Library
'''.strip().splitlines()

setup(
    name='robotframework-%s' % LIBRARY_NAME.lower(),
    version=VERSION,
    description='SeleniunTestability library that helps speed up tests with'
                'asyncronous evens',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    url='https://github.com/omenia/robotframework-%s' % LIBRARY_NAME.lower(),
    author='Jani Mikkonen',
    author_email='jani.mikkonen@siili.com',
    license='Apache License 2.0',
    classifiers=CLASSIFIERS,
    install_requires = REQUIREMENTS,
    keywords='robot framework testing automation selenium seleniumlibrary'
             'testability async javascript softwaretesting',
    platforms='any',
    packages=find_packages('src'),
    package_dir={'': 'src'},
)
