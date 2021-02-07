#!/usr/bin/env python3
import os
import argparse

from revise_bibtex import validate_bibs


help_msg = """
bib-revise
==========

Normalize bibtex citations and helps you to find some
common inconsistent/missing information.

Run this in the project directory, which has only one bib and bbl files,
or give these arguments as specified.

Example:

    $ python3 -m revise_bibtex --bib-file=src.bib --bbl-file=main.bbl --force

Options:
"""


if __name__ == '__main__':

    parser = argparse.ArgumentParser(help_msg)
    files_here = os.listdir()

    bib_files = [f for f in files_here if f.endswith('.bib')]
    bbl_files = [f for f in files_here if f.endswith('.bbl')]

    if len(bib_files) == 1 and len(bbl_files) == 1:
        parser.add_argument('--bib-file', type=str, help='path to bib file',
                            dest='bib_file', default=bib_files[0])
        parser.add_argument('--bbl-file', type=str, help='path to bbl file',
                            dest='bbl_file', default=bbl_files[0])
    else:
        parser.add_argument('--bib-file', type=str, help='path to bib file',
                            dest='bib_file')
        parser.add_argument('--bbl-file', type=str, help='path to bbl file',
                            dest='bbl_file')

    parser.add_argument('--out-bib-file', type=str, dest='out_bib_file',
                        default=None, help='path to output bbl file')
    parser.add_argument('--force', action='store_true', dest='force',
                        help='Force only the necessary keys')
    parser.add_argument('--skip', action='store_true', dest='skip',
                        help='Skip the one-by-one check')
    parser.add_argument('--verbose', action='store_true', dest='verbose',
                        help='Print also the good/skipped references')


    args = parser.parse_args()
    if args.bib_file is None or args.bbl_file is None:
        print('Please enter both "bib_file" and "bbl_file" paths arguments')
    else:
        validate_bibs(args.bib_file, args.bbl_file, args.out_bib_file,
                  args.force, args.skip, args.verbose)

