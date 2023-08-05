#!/usr/bin/env python
from setuptools import setup
setup(
  name = 'cs.filestate',
  description = 'Trivial FileState class used to watch for file changes.',
  author = 'Cameron Simpson',
  author_email = 'cs@cskk.id.au',
  version = '20181107',
  url = 'https://bitbucket.org/cameron_simpson/css/commits/all',
  classifiers = ['Programming Language :: Python', 'Programming Language :: Python :: 2', 'Programming Language :: Python :: 3', 'Development Status :: 4 - Beta', 'Intended Audience :: Developers', 'Operating System :: OS Independent', 'Topic :: Software Development :: Libraries :: Python Modules', 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'],
  install_requires = [],
  keywords = ['python2', 'python3'],
  long_description = 'Facility to track file state.\n\nThis is used to watch for size or modification time changes,\nor to notice when a file path no longer points at the same file.\n\n## Function `FileState(path, do_lstat=False, missing_ok=False)`\n\nReturn a signature object for a file state derived from os.stat\n(or os.lstat if `do_lstat` is true).\n`path` may also be an int, in which case os.fstat is used.\nThis returns an object with mtime, size, dev and ino attributes\nand can be compared for equality with other signatures.\n`missing_ok`: return None if the target file is missing,\n  otherwise raise. Default False.',
  long_description_content_type = 'text/markdown',
  package_dir = {'': 'lib/python'},
  py_modules = ['cs.filestate'],
)
