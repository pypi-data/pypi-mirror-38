"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

from os import path

from setuptools import setup, find_packages

from events_dock.utils import Config

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='events_dock',
    version=Config().get('app.version'),
    description='Application used to control docker events.',
    author='Todor Todorov',
    author_email='todstoychev@gmail.com',
    url='https://github.com/todstoychev/events-dock',
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='docker containers control',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=['docker', 'PyQt5', 'QtAwesome', 'events'],
    package_data={
        '': ['config.ini']
    },
    entry_points={
        'console_scripts': [
            'events-dock=events_dock.__main__:main',
        ],
    }
)
