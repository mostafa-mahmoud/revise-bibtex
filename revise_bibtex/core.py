#!/usr/bin/env python3
import argparse
import os
import re
import urllib.parse

import bibtexparser
import pyperclip

from .logger import logger
from .utils import (
    print_entry_dict_as_bib, trim, non_capitalized_words,
    remove_umlauts, us_state_abbrev, isclose
)


required_keys = {
    "inproceedings": ['title', 'publisher', 'address', 'booktitle', 'pages', 'year', 'author'],
    "article": ['author', 'journal', 'pages', 'publisher', 'year', 'title'],
    "book": ['title', 'author', 'year', 'publisher'],
    "inbook": ['title', 'author', 'year', 'publisher', 'chapter'],
    "misc": ['title', 'author', 'year', 'url', 'eprint'],
    "phdthesis": ['title', 'author', 'school', 'year'],
    "masterthesis": ['title', 'author', 'school', 'year'],
}


def get_bib_items_ids(bbl_path):
    regex = re.compile(r'\\bibitem{(.*?)}')
    with open(bbl_path, 'r') as fl:
        bib_file_text = fl.read()

    return regex.findall(bib_file_text)


def validate_title(entry):
    if 'title' not in entry.keys():
        return 'title key not found'
    title = entry['title']

    title = trim(title)
    bad_words = non_capitalized_words(title)
    counts = len(bad_words)
    title = '{%s}' % title

    entry['title'] = title
    if counts > 2:
        pass
        # return 'Several uncapitalized words (%d) in title %s: %s' % (counts, title, bad_words)


def validate_address(entry):
    if 'address' in entry.keys() and entry['ENTRYTYPE'] == 'inproceedings':
        states = list(us_state_abbrev.keys())
        abbrv = list(us_state_abbrev.values())
        address = entry['address']
        components = [w.strip() for w in address.split(',')]
        if len(components) == 3:
            if components[2] != 'USA':
                return 'address\' last component should be USA if they are 3 components, got %s' % components[2]
            if components[1] not in states + abbrv:
                return 'address component[1] should be a US state, got: %s' % components[1]
        elif len(components) != 2:
            return 'address components should be 2 or 3'
        if components[1] in states:
            components[1] = us_state_abbrev[components[1]]
        if components[1] in abbrv and len(components) == 2:
            components.append('USA')
        address = ', '.join(components)
        entry['address'] = address


def validate_author(entry):
    if 'author' not in entry.keys():
        return 'authors key not found'
    author = entry['author']

    author = trim(author)
    author = remove_umlauts(author)
    authors = author.split(' and ')
    for a in authors:
        names = []
        for name in a.split(','):
            names.extend(name.strip().split())
        names = [x for x in names if x]
        initials_only = sum([len(x) == 1 or (len(x) == 2 and x[-1] == '.') for x in names])
        if 'et al.' in a or 'others' in a:
            return f'Unnamed authors "{a}"'
        if len(names) == 1:
            return f'only one name "{a}"'
        if initials_only + 1 >= len(names):
            return 'author with initials only (%d): "%s""' % (initials_only, a)

    entry['author'] = author
    return


def validate_arxiv(entry):
    if entry['ENTRYTYPE'] == 'misc' and 'archiveprefix' in entry.keys() and entry['archiveprefix'] == 'arXiv':
        del entry['archiveprefix']
        entry['publisher'] = 'arXiv'
        return 'arXiv preprint, try to find a peer-reviewed version'


def validate_pages(entry):
    if 'pages' in entry.keys():
        pages = entry['pages']
        pages = pages.replace(' ', '')
        pages = pages.replace('--', '-')
        pages = pages.replace('-', '--')
        entry['pages'] = pages


def validate_doi(entry):
    doi_static = "https://doi.org/"
    if 'doi' and 'url' in entry.keys():
        entry.pop('url')
    if 'doi' in entry.keys() and entry['doi'].startswith(doi_static):
        entry['doi'] = entry['doi'][len(doi_static):]
    if 'url' in entry.keys():
        if entry['url'].startswith(doi_static):
            entry['doi'] = entry['url'][len(doi_static):]
            entry.pop('url')
        else:
            return 'URL is available but not DOI, check please'


def validate_entry(entry, force, force_doi=False):

    warnings = [
        validate_title(entry),
        validate_author(entry),
        validate_arxiv(entry),
        validate_pages(entry),
        validate_address(entry),
    ]
    if force_doi:
        warnings.append(validate_doi(entry))

    necessary_keys = required_keys.get(entry['ENTRYTYPE'], [])
    year = entry.get('year', 'YEAR')
    if 'year' not in entry.keys():
        warnings.append("Year is empty")
    publisher = entry.get('publisher', '')
    if not necessary_keys:
        warnings.append('Unknown entry type "%s"' % entry['ENTRYTYPE'])
    else:
        for key in necessary_keys:
            if key not in entry.keys():
                entry[key] = ''
            if not entry[key] and key != 'url':
                warnings.append('"%s" is empty' % key)
            if year in entry[key] and key not in ['year', 'title', 'doi', 'url']:
                warnings.append('Year "%s": is found in "%s": "%s"' % (year, key, entry[key]))
            if publisher and key !='publisher' and publisher in entry[key]:
                warnings.append('Publisher "%s" is found in "%s": "%s"' % (publisher, key, entry[key]))
            if 'proc.' in entry[key].lower():
                warnings.append('"proc." found in "%s": "%s"' % (key, entry[key]))

        pairs = list(entry.items())
        for key, value in pairs:
            if not value or (force and key not in necessary_keys + ['ENTRYTYPE', 'ID']):
                del entry[key]
    warnings = [x for x in warnings if x]
    return warnings


def validate_bibs(bib_path, bbl_path, out_bib_file=None, force=True,
                  skip=False, verbose=False, no_logs=False, force_doi=False,
                  braces=True):

    if not no_logs:
        from .logger import add_log_file
        add_log_file()

    if bib_path is None or not os.path.isfile(bib_path):
        logger.error("Invalid path for bib file \"%s\"", bib_path, highlight=1)
        return

    is_there_bbl = False
    if bbl_path is None:
        logger.critical("bbl_path is not provided, it is very recommended to provide one", highlight=1)
    elif not os.path.isfile(bbl_path):
        logger.error("Invalid path for bbl file \"%s\"", bbl_path, highlight=1)
    else:
        is_there_bbl = True

    if out_bib_file is not None and bib_path == out_bib_file:
        logger.error("Input and output files should be different, %s" % bib_path, highlight=1)
        return

    with open(bib_path, 'r') as fl:
        bibtex = bibtexparser.load(fl)
        logger.info('loaded "%s" ...', bib_path)

    if is_there_bbl:
        all_ids = get_bib_items_ids(bbl_path)
        logger.info('%d bibitems are to be found...', len(all_ids), highlight=4)
    else:
        all_ids = [entry['ID'] for entry in bibtex.entries]

    ids = []
    filtered_entries = []
    cnt = 0

    for entry in bibtex.entries:
        if entry['ID'] not in all_ids:
            if verbose:
                logger.info('skipping %s, because it is not in the bbl file, '
                            'it is probably not cited..', entry['ID'])
            continue
        note = entry.get('note', None)
        ids.append(entry['ID'])
        filtered_entries.append(entry)
        warnings = validate_entry(entry, force, force_doi=force_doi)
        if warnings:
            for w in warnings:
                logger.warning(w, highlight=3)
            print_entry_dict_as_bib(entry, braces=braces)
            pyperclip.copy(entry['title'].replace('{', '').replace('}', ''))
            # logger.info('%d/%d done..' % (cnt, len(bibtex.entries)))
            logger.info('%d/%d done..\n', cnt, len(all_ids))
            # logger.print('\n\n')
            if not skip:
                search_title = urllib.parse.quote(entry['title'].replace('{', '').replace('}', ''))
                logger.print('https://scholar.google.com/scholar?q=' + search_title)
                logger.print('https://ieeexplore.ieee.org/search/searchresult.jsp?newsearch=true&queryText=' + search_title)
                print('\n[Paper title is copied to clipboard... press enter to continue..]\n')
                input()
        elif verbose:
            logger.info('%d/%d done..' % (cnt, len(all_ids)))
            logger.info("Looks good...", highlight=2)
            print_entry_dict_as_bib(entry, logger.print, braces=braces)
        # entry['volume'] = "{}"
        # entry['number'] = "{}"
        if note is not None:
            entry['note'] = note
        cnt += 1
    logger.info('%d/%d done..', cnt, len(all_ids))
    not_seen = set(all_ids) - set(ids)

    bibtex.entries = filtered_entries
    bibtex.add_missing_from_crossref()
    for i in range(len(bibtex.entries)):
        entry_i = bibtex.entries[i]
        for j in range(i):
            entry_j = bibtex.entries[j]
            if isclose(entry_i['title'], entry_j['title']):
                logger.warning('%s and %s seem to be the same citation, with different IDs',
                               entry_i['ID'], entry_j['ID'], highlight=2)

    if len(all_ids) != len(bibtex.entries):
        logger.critical(
            "Some bib-items that are in your paper are not parsed correctly. "
            "The following IDs are not found: %s", ','.join([f'"{x}"' for x in not_seen]), highlight=1)
    else:
        logger.info('%d bibitems processed in total, these should match '
                    'the number of citations in your paper', len(all_ids), highlight=2)

    if out_bib_file is not None:
        with open(out_bib_file, 'w') as fl:
            bibtexparser.dump(bibtex, fl)
            logger.info('%s saved...', out_bib_file)
