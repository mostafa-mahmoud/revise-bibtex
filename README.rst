=============
Revise-bibtex
=============

|
|

A tool that helps revising the references from bibliography,
by normalizing bibtex citations and helping you to find some
common inconsistent/missing information.

Run this in the project directory, which has only one bib and bbl files,
or give these arguments as specified.

|
|

Installation
============

|
|


Run the following command::

   $ python3 setup.py install 

|
|

How to use
==========

|
|

Example::

    $ python3 -m revise_bibtex --bib-file=src.bib --bbl-file=main.bbl --force


For runtime help, run the following command::

    $ python3 -m revise_bibtex --help

