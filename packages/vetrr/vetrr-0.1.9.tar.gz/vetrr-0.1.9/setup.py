from setuptools import setup, find_packages

import os
import glob


def get_scripts():
    """ Grab all the scripts in the bin directory.  """
    scripts = []
    if os.path.isdir('bin'):
        scripts = [fname for fname in glob.glob(os.path.join('bin', '*'))
                   if not os.path.basename(fname).endswith('.rst')]
    return scripts


scripts = get_scripts()

setup(name='vetrr',
      version='0.1.9',
      description='vet redrock outputs',
      url='http://github.com/mattcwilde/vetrr',
      author='Matthew Wilde',
      author_email='mattcwilde@gmail.com',
      license='MIT',
      # packages=['vetrr'],
      packages=find_packages(exclude=['contrib']),  # Required
      scripts=scripts,
      dependency_links=['https://github.com/linetools/linetools'],
      install_requires=[
        'matplotlib',
        'pyYAML',
        'astropy',
        'future',
        'numpy'
        ],
      zip_safe=True)
