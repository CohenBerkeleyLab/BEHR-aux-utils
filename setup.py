#!/usr/bin/env python

from distutils.core import setup

setup(name='BEHR-Aux-Utils',
      version='0.1',
      description='Auxiliary utilities for the BEHR algorithm',
      author='Josh Laughner',
      author_email='jlaughner@berkeley.edu',
      url='https://github.com/CohenBerkeleyLab/BEHR-aux-utils',
      packages=['behr_aux_utils'],
      scripts=['behr_aux_utils/cleanup_behr_input_files.py']
      )
