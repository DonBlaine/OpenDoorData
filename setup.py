import os
import pip

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages
    
#use requirements.txt to get necessary installs
with open(r"requirements.txt") as f:
    required = f.read().splitlines()
    
setup(
  name='Open Door Data',
  version='0.1.0',
  description='UCD summer research project',
  url='git@git.ucd.ie:coolhanddon/summerproject.git',
  license='MIT',
  author='UCD summer research project',
  long_description=open('README.md').read(),
  packages=find_packages(exclude=['tests*']),
  install_requires = required,
  include_package_data=True,
  )

