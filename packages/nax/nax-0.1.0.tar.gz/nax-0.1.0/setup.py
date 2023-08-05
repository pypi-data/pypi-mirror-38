import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name = 'nax',
    version = '0.1.0',
    author = 'Kris',
    author_email = '31852063+krisfris@users.noreply.github.com',
    description = ('nax name generator'),
    license = 'MIT',
    keywords = '',
    url = 'https://github.com/krisfris/nax',
    packages=find_packages(exclude=['docs', 'tests']),
    include_package_data=True,
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    install_requires=[],
    entry_points = {
       'console_scripts': [
            'nax = nax.__init__:main'
        ]
    }
)

