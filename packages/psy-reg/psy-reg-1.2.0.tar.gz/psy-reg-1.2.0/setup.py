import os.path as osp
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import sys


def readme():
    with open('README.rst') as f:
        return f.read()


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to pytest")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = ''

    def run_tests(self):
        import shlex
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(shlex.split(self.pytest_args))
        sys.exit(errno)


# read the version from version.py
with open(osp.join('psy_reg', 'version.py')) as f:
    exec(f.read())


setup(name='psy-reg',
      version=__version__,
      description=('Psyplot plugin for visualizing and calculating regression '
                   'plots'),
      long_description=readme(),
      classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering :: Visualization',
        'Topic :: Scientific/Engineering :: GIS',
        'Topic :: Scientific/Engineering',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Operating System :: OS Independent',
      ],
      keywords='visualization netcdf raster cartopy earth-sciences psyplot',
      url='https://github.com/Chilipp/psy-reg',
      author='Philipp Sommer',
      author_email='philipp.sommer@unil.ch',
      license="GPLv2",
      packages=find_packages(exclude=['docs', 'tests*', 'examples']),
      install_requires=[
          'psyplot',
          'psy-simple>1.0.1',
          'statsmodels',
          'scipy',
      ],
      tests_require=['pytest'],
      cmdclass={'test': PyTest},
      entry_points={'psyplot': ['plugin=psy_reg.plugin',
                                'patches=psy_reg.plugin:patches']},
      zip_safe=False)
