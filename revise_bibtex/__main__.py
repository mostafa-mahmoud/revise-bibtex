#!/usr/bin/env python3
import argparse
import os

from revise_bibtex import validate_bibs


help_msg = """
bib-revise
==========

Normalize bibtex citations and helps you to find some
common inconsistent/missing information.

Run this in the project directory, which has only one bib and bbl files,
or give these arguments as specified.

Example:

    $ python3 -m revise_bibtex references.bib --bbl-file output.bbl

Options:
"""


if __name__ == '__main__':
    parser = argparse.ArgumentParser(help_msg)
    files_here = os.listdir()

    parser.add_argument('bib_file', help='path to bib file')
    parser.add_argument('--bbl-file', help='path to bbl file')
    parser.add_argument('--out-bib-file', help='path to output bbl file')
    parser.add_argument(
        '--force-all-keys', action='store_true',
        help='Force adding all keys originally in the bib file'
    )
    parser.add_argument('--skip', action='store_true',
                        help='Skip the one-by-one check')
    parser.add_argument('--verbose', action='store_true',
                        help='Print also the good/skipped references')
    parser.add_argument('--no-logs', action='store_true',
                        help="don't dump the bib_comments.log file")
    parser.add_argument('--force-doi', action='store_true',
                        help="force checking DOIs entry")
    parser.add_argument(
        '--single-brace', action='store_true',
        help="print the bibTeX with single brace only in titles."
    )
    # parser.add_argument(
    #     '--no-braces', action='store_true',
    #     help="print the bibTeX with quotations instead of braces"
    # )

    args = parser.parse_args()
    validate_bibs(
        args.bib_file, args.bbl_file, out_bib_file=args.out_bib_file,
        force=not args.force_all_keys, skip=args.skip, verbose=args.verbose,
        no_logs=args.no_logs, force_doi=args.force_doi,
        single_brace=args.single_brace
    )
