import sys

from setuptools import find_packages, setup

version = __import__('dictionaryapi').__version__

with open('README.rst', encoding='utf-8') as fp:
    readme = fp.read()

setup(
    name="DictionaryAPI",
    version=version,
    python_requires='==2.7,>=3.4',
    license='GPLv3+',
    description='The Merriam-Webster Dictionary API',
    long_description=readme,
    author='tcztzy',
    author_email='tcztzy@gmail.com',
    url='https://dictionaryapi.com',
    packages=find_packages(exclude=['dictionaryapi.bin']),
    install_requires=['requests'],
    scripts=['dictionaryapi/bin/dictionaryapi.py'],
    entry_points={'console_scripts': [
        'dictionaryapi = dictionaryapi'
    ]},
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'Intended Audience :: Education',
        'License :: Free for non-commercial use',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Natural Language :: English',
        'Natural Language :: Spanish',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Education',
        'Topic :: Utilities',
    ],
    project_urls={
        'Source': 'https://github.com/dictionaryapi/dictionaryapi'
    }
)
