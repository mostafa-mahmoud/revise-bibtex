#!/usr/bin/env python3
from setuptools import setup

VERSION = __import__('revise_bibtex').__version__

install_requires = [
    'bibtexparser',
    'pyperclip',
    'sklearn',
    'pylcs',
]

setup(name='revise_bibtex',
      version=VERSION,
      description='Normalize bibtex citations and helps you to find some common inconsistent/missing information.',
      author='Mostafa M. Mohamed',
      author_email='mostafa.amin93@gmail.com',
      long_description=('\n%s' % open('README.rst', 'r').read()),
      url='https://github.com/mostafa-mahmoud/revise-bibtex',
      license='MIT',
      packages=['revise_bibtex'],
      install_requires=install_requires,
      classifiers=[
          'Development Status :: 4 - Beta',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 3.6',
      ],
)
