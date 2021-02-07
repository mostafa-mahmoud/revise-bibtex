=============
Revise-bibtex
=============

A tool that helps revising the references from bibliography,
by normalizing bibtex citations and helping you to find some
common inconsistent/missing information.

Run this in the project directory, which has only one bib and bbl files,
or give these arguments as specified.

Installation
============

Run the following command::

   $ python3 setup.py install 

How to use
==========

To use the tool, you need your bib file and bbl file. bbl file can be skipped, however this is not recommended.
Example::

    $ python3 -m revise_bibtex --bib-file=src.bib --bbl-file=main.bbl


For runtime help, run the following command::

    $ python3 -m revise_bibtex --help


How to get bbl files
====================

#. Typically you find the bbl file next to the bib file, when you compile your latex project using `pdflatex` command.

#. For overleaf, you can find it among the log files, check:

   `https://www.overleaf.com/learn/latex/Questions/The_journal_says_%22don't_use_BibTeX;_paste_the_contents_of_the_.bbl_file_into_the_.tex_file%22._How_do_I_do_this_on_Overleaf%3F`
