from setuptools import setup, find_packages
# import os, sys, glob, fnmatch

setup(name="pootielang",
      version='0.0.1',
      description="pootie-tang inspired language",
      long_description=""" """,
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'Intended Audience :: Religion',
          'Intended Audience :: End Users/Desktop',
          'License :: OSI Approved :: MIT License',
          'Operating System :: Microsoft :: Windows',
          'Operating System :: POSIX :: Linux',
          'Programming Language :: Python :: 3',
          'Topic :: Software Development :: Libraries :: Python Modules'],
      keywords='Pootie, Bammies, Sepatown',
      author='Derric Williams',
      author_email='derricw@gmail.com',
      url='https://github.com/derricw/pootielang',
      license='MIT',
      packages=find_packages(),
      zip_safe=True,
      install_requires=[''],
      entry_points={'console_scripts': ['tang = pootielang.cli:main']},
      )
