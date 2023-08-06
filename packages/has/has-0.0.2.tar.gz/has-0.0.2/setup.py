from setuptools import setup
from has.has import __version__

setup(
    name='has',
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
