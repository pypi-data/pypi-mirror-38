from setuptools import setup
from has.has import __version__
from os import path

# Read the contents of the README file
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='has',
    long_description=long_description,
    long_description_content_type='text/markdown',
    version=__version__,
    description='Hash array snapshot',
    url='https://gitlab.com/timcogan/hash_array_snapshot',
    author='Tim Cogan',
    author_email='timothycogan@gmail.com',
    license='Apache',
    packages=['has'],
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'has=has.has:main',
        ],
    },
)
