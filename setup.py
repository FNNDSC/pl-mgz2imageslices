from os import path
from setuptools import setup

with open(path.join(path.dirname(path.abspath(__file__)), 'README.rst')) as f:
    readme = f.read()

setup(
    name             = 'mgz2imageslices',
    version          = '1.0.2',
    description      = 'An app to convert 3d mgz files to 2s slices of readable formats like PNG/JPEG',
    long_description = readme,
    author           = 'Arushi Vyas',
    author_email     = 'dev@babyMRI.org',
    url              = 'https://github.com/FNNDSC/pl-mgz2imageslices',
    packages         = ['mgz2imageslices'],
    install_requires = ['chrisapp'],
    test_suite       = 'nose.collector',
    tests_require    = ['nose'],
    license          = 'MIT',
    zip_safe         = False,
    python_requires  = '>=3.8',
    entry_points     = {
        'console_scripts': [
            'mgz2imageslices = mgz2imageslices.__main__:main'
            ]
        }
)
