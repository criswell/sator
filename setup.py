#!/usr/bin/env python

from distutils.core import setup

scripts = ['sator']

packages = [ 'satorlib' ]

setup(name='Sator',
      version='0.0.1',
      description='A reverse SSH manager',
      author='Sam Hart',
      author_email='hartsn@gmail.com',
      url='https://bitbucket.org/criswell/sator',
      license='GNU GPLv3+',
      scripts=scripts,
      packages=packages,
     )
