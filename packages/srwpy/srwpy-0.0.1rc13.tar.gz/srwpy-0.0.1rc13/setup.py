import os
import sys
from setuptools import setup, find_packages, Extension
import versioneer


# NOTE: This file must remain Python 2 compatible for the foreseeable future,
# to ensure that we error out properly for people with outdated setuptools
# and/or pip.
min_version = (2, 7)
if sys.version_info < min_version:
    error = """
srwpy does not support Python {0}.{1}.
Python {2}.{3} and above is required. Check your Python version like so:

python3 --version

This may be due to an out-of-date pip. Make sure you have pip >= 9.0.1.
Upgrade pip like so:

pip install --upgrade pip
""".format(*sys.version_info[:2], *min_version)
    sys.exit(error)

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.rst'), encoding='utf-8') as readme_file:
    readme = readme_file.read()

with open(os.path.join(here, 'requirements.txt')) as requirements_file:
    # Parse requirements.txt, ignoring any commented-out lines.
    requirements = [line for line in requirements_file.read().splitlines()
                    if not line.startswith('#')]

srwlpy = Extension(
    'srwlpy',
    include_dirs=['core/src/lib'],
    libraries=['srw', 'm', 'fftw'],
    library_dirs=['core/gcc'],
    sources=['core/src/clients/python/srwlpy.cpp'])

setup(
    name='srwpy',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description="Synchrotron Radiation Workshop",
    long_description=readme,
    author="NSLS-II, Brookhaven National Lab",
    author_email='mrakitin@bnl.gov',
    url='https://github.com/srwpy/srwpy',
    packages=find_packages(exclude=['docs', 'tests']),
    entry_points={
        'console_scripts': [
            # 'some.module:some_function',
            ],
        },
    include_package_data=True,
    package_data={
        'srwpy': [
            # When adding files here, remember to update MANIFEST.in as well,
            # or else they will not be included in the distribution on PyPI!
            # 'path/to/data_file',
            '*.so'
            ]
        },
    install_requires=requirements,
    license="BSD (3-clause)",
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Operating System :: POSIX',
        'Operating System :: MacOS',
    ],
    ext_modules=[srwlpy],
)
