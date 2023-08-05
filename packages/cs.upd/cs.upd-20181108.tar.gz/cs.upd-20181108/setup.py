#!/usr/bin/env python
from setuptools import setup
setup(
  name = 'cs.upd',
  description = 'Single line status updates with minimal update sequences.',
  author = 'Cameron Simpson',
  author_email = 'cs@cskk.id.au',
  version = '20181108',
  url = 'https://bitbucket.org/cameron_simpson/css/commits/all',
  classifiers = ['Programming Language :: Python', 'Programming Language :: Python :: 2', 'Programming Language :: Python :: 3', 'Development Status :: 4 - Beta', 'Intended Audience :: Developers', 'Operating System :: OS Independent', 'Topic :: Software Development :: Libraries :: Python Modules', 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'],
  install_requires = ['cs.lex', 'cs.tty'],
  keywords = ['python2', 'python3'],
  long_description = "Single line status updates with minimal update sequences.\n\nThis is available as an output mode in cs.logutils.\n\nExample:\n\n    upd = Upd(sys.stdout)\n    ...\n    upd.out('status line text: position = %d', position_value)\n    ...\n    upd.nl('an informational line')\n    ...\n    upd.out('new status text')\n\n## Function `cleanupAtExit()`\n\nCleanup function called at programme exit to clear the status line.\n\n## Class `Upd`\n\nA class for maintaining a regularly updated status line.\n\n## Function `upd_for(stream)`\n\nFactory for Upd singletons keyed by the id of their backend.",
  long_description_content_type = 'text/markdown',
  package_dir = {'': 'lib/python'},
  py_modules = ['cs.upd'],
)
