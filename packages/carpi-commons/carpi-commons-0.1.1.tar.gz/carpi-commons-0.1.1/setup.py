"""
CARPI COMMONS
(C) 2018, Raphael "rGunti" Guntersweiler
Licensed under MIT
"""

from setuptools import setup

with open('README.md', 'r') as f:
    long_description = f.read()

setup(name='carpi-commons',
      version='0.1.1',
      description='A library providing utilities for writing CarPi programs and services.',
      long_description=long_description,
      url='https://github.com/rGunti/CarPi-Commons',
      keywords='carpi commons',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.6'
      ],
      author='Raphael "rGunti" Guntersweiler',
      author_email='raphael@rgunti.ch',
      license='MIT',
      packages=['carpicommons'],
      install_requires=[
          'wheel'
      ],
      zip_safe=False,
      include_package_data=True)
