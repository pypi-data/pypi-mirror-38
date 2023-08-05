from setuptools import setup
from os import path
from re import findall


def get_version(filename):
    with open(filename) as f:
        metadata = dict(findall(r"__([a-z]+)__ = '([^']+)'", f.read()))
    return metadata['version']


here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pygnore',
    version=get_version(path.join(here, 'pygnore/__init__.py')),
    description='Client for gitignore.io',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/flipee/pygnore',
    author='flipee',
    author_email='filipe.nascimento01@fatec.sp.gov.br',
    license='MIT',
    packages=['pygnore'],
    install_requires=[
        'cachetools',
    ],
    extras_require={
        'dev': [
            'black',
            'flake8-bugbear',
            'flake8-mypy'
        ],
        'test': [
            'coveralls',
            'flake8',
            'tox-venv',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    keywords='pygnore gitignore development',
)
