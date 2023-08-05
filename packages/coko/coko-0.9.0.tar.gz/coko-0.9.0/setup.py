from setuptools import setup, find_packages  # Always prefer setuptools over distutils

long_description = """Sometimes you have a directory full of files you want to overwrite periodically.

You may not want to edit those files directly but let other users edit a local copy of those files to copy them over original ones.

Problem there is that local copies may have changed their owners or permissions to be edited so those metadata are carried over original directory overwriting it.

This tools let you take an snapshot of your files metadata in a particular directory in order to restore those metadata after files have been restored.
More info in: https://github.com/dante-signal31/coko
"""

setup(name="coko",
      version="0.9.0",
      description="This tools let you take an snapshot of your files metadata "
                  "in a particular directory in order to restore those metadata "
                  "after files have been restored.",
      long_description=long_description,
      author="Dante Signal31",
      author_email="dante.signal31@gmail.com",
      license="BSD-3",
      url="https://github.com/dante-signal31/coko",
      download_url="https://github.com/dante-signal31/coko/releases",
      classifiers=['Development Status :: 4 - Beta',
                   'Intended Audience :: Developers',
                   'Intended Audience :: Information Technology',
                   'Intended Audience :: Science/Research',
                   'Intended Audience :: System Administrators',
                   'Intended Audience :: Telecommunications Industry',
                   'Intended Audience :: Other Audience',
                   'Topic :: System',
                   'Topic :: Security',
                   'License :: OSI Approved :: BSD License',
                   'Operating System :: POSIX :: Linux',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.7'],
      keywords="copy over keeping ownersHIP",
      install_requires=[],
      zip_safe=False,
      # TODO: This exclude is not working when building wheels, tests package
      # is still included in packages. It's a bug in pip:
      #     https://bitbucket.org/pypa/wheel/issue/99/cannot-exclude-directory
      # Until it is fixed, the workaround is to compile wheel package in two
      # steps:
      #     python setup.py sdist
      #     pip wheel --no-index --no-deps --wheel-dir dist dist/*.tar.gz
      packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*",
                                      "tests", "*tests*"]),
      entry_points={'console_scripts': ['coko=coko.launcher:main', ], }
      )
