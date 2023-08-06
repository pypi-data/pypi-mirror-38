# -*- coding: utf-8 -*-
from setuptools import setup

setup(name='seletivo-lattes',
      version='1.0.2',
      description='A simple script to get LATTES CV from a list of candidates in the CNPq Database',
      url='http://github.com/storopoli/seletivo-lattes',
      author='Jose Eduardo Storopoli',
      author_email='thestoropoli@gmail.com',
      license='MIT',
      packages=['seletivo-lattes'],
      install_requires=[
          'pandas',
          'requests',
          'bs4'
      ],
      zip_safe=False)
