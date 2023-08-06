"""
CARPI REDIS DATA BUS
(C) 2018, Raphael "rGunti" Guntersweiler
Licensed under MIT
"""

from setuptools import setup

with open('README.md', 'r') as f:
    long_description = f.read()

setup(name='carpi-gpsdaemon',
      version='0.1.1',
      description='GPS daemon written in Python transmitting from GPSD to a Redis Data Bus',
      long_description=long_description,
      url='https://github.com/rGunti/CarPi-GPSDaemon',
      keywords='carpi gps daemon',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.6'
      ],
      author='Raphael "rGunti" Guntersweiler',
      author_email='raphael@rgunti.ch',
      license='MIT',
      packages=['gpsdaemon'],
      install_requires=[
          'wheel',
          'carpi-redisdatabus',
          'carpi-daemoncommons'
      ],
      zip_safe=False,
      include_package_data=True)
