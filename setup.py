# setup

from setuptools import setup

setup(name='tapl',
      version='0.1',
      description='Implementations from Types and Programming Languages',
      url='https://github.com/frutiger/tapl',
      author='Masud Rahman',
      license='MIT',
      packages=['tapl', 'tapl/arith'],
      entry_points={
          'console_scripts': ['arith=tapl.__main__:main'],
      })

