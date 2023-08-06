"""
CARPI DAEMON COMMONS
(C) 2018, Raphael "rGunti" Guntersweiler
Licensed under MIT
"""

from setuptools import setup

with open('README.md', 'r') as f:
    long_description = f.read()

setup(name='carpi-daemoncommons',
      version='0.2.0',
      description='A library providing utilities for writing Python daemons.',
      long_description=long_description,
      url='https://github.com/rGunti/CarPi-DaemonCommons',
      keywords='carpi daemon',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.6'
      ],
      author='Raphael "rGunti" Guntersweiler',
      author_email='raphael@rgunti.ch',
      license='MIT',
      packages=['daemoncommons'],
      install_requires=[
          'carpi-commons',
          'wheel'
      ],
      zip_safe=False,
      include_package_data=True)
