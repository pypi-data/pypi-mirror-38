from glob import glob
import os
from setuptools import setup, find_packages  # Always prefer setuptools over distutils
from typing import List

import ci_scripts.ci_tools as tools


VDIST_PACKAGES_CONFIG = "packaging/coko_vdist.cnf"

LONG_DESCRIPTION = """Sometimes you have a directory full of files you want to overwrite periodically.

You may not want to edit those files directly but let other users edit a local copy of those files to copy them over original ones.

Problem there is that local copies may have changed their owners or permissions to be edited so those metadata are carried over original directory overwriting it.

This tools let you take an snapshot of your files metadata in a particular directory in order to restore those metadata after files have been restored.
More info in: https://github.com/dante-signal31/coko
"""


def find_folders_with_this_name(dir_name: str)-> str:
    """ Look for folder with given name, searching from current working dir.

    :param dir_name: Folder name to look for.
    :return: Relative path, from current working dir, where folder is.
    """
    for dir, dirs, files in os.walk('.'):
        if dir_name in dirs:
            yield os.path.relpath(os.path.join(dir, dir_name))


def find_man_pages()-> List:
    """ Look for every folder named "man", inside current working dir, and include
    its files relatives paths in a list suitable to be passed to a data_files
    setup.py parameter. This list will set those manpages to be installed to
    "share/man/man<section>" at target box.

    This code was inspired by a really interesting answer to:
    https://github.com/pypa/packaging-problems/issues/72#issuecomment-279162312

    :return: A list with tuples ("share/man/man<section>", local_relative_path_to_manpage)
    """
    data_files = []
    man_sections = {}
    for dir in find_folders_with_this_name('man'):
        for file in os.listdir(dir):
            section = file.split('.')[-1]
            man_sections[section] = man_sections.get(section, []) + [os.path.join(dir, file)]
    for section in man_sections:
        data_files.append(('share/man/man'+section, man_sections[section]))
    return data_files


def find_info_pages()-> List:
    """ Look for every folder named "info", inside current working dir, and include
    its files relatives paths in a list suitable to be passed to a data_files
    setup.py parameter. This list will set those infopages to be installed to
    "share/info" at target box.

    This code was inspired by a really interesting answer to:
    https://github.com/pypa/packaging-problems/issues/72#issuecomment-279162312

    :return: A list with tuples ("share/info", local_relative_path_to_infopage)
    """
    data_files = []
    info_pages = {}
    for dir in find_folders_with_this_name('info'):
        for file in glob(os.path.join(dir, '*.info')):
            info_pages[dir] = info_pages.get(dir, []) + [file]
    for dir in info_pages:
        data_files.append(('share/info', info_pages[dir]))
    return data_files


setup(name="coko",
      version=tools.get_current_version(VDIST_PACKAGES_CONFIG),
      description="This tools let you take an snapshot of your files metadata "
                  "in a particular directory in order to restore those metadata "
                  "after files have been restored.",
      long_description=LONG_DESCRIPTION,
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
      keywords="copy over keeping ownership",
      install_requires=[],
      zip_safe=False,
      packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*",
                                      "tests", "*tests*", "ci_scripts",
                                      "ci_scripts.*", "*.ci_scripts",
                                      "*.ci_scripts.*", "*ci_scripts*",
                                      "ci_scripts*"]),
      data_files=find_man_pages(),
      entry_points={'console_scripts': ['coko=coko.launcher:main', ], }
      )
