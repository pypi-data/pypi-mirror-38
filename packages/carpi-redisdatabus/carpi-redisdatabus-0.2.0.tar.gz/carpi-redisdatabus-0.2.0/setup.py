"""
CARPI REDIS DATA BUS
(C) 2018, Raphael "rGunti" Guntersweiler
Licensed under MIT
"""

from setuptools import setup

with open('README.md', 'r') as f:
    long_description = f.read()

setup(name='carpi-redisdatabus',
      version='0.2.0',
      description='Redis Data Bus (inspired by CAN-BUS, developed for CarPi)',
      long_description=long_description,
      url='https://github.com/rGunti/CarPi-RedisDataBus',
      keywords='carpi redis data bus',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.6'
      ],
      author='Raphael "rGunti" Guntersweiler',
      author_email='raphael@rgunti.ch',
      license='MIT',
      packages=['redisdatabus'],
      install_requires=[
          'carpi-commons',
          'redis',
          'tzlocal',
          'pytz',
          'wheel'
      ],
      zip_safe=False,
      include_package_data=True)
