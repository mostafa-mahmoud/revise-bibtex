import pylcs
from sklearn.feature_extraction import stop_words


def warn(*args, highlight=1):
     print('\033[%dm%s\033[39m' % (30 + highlight, ' '.join(args)))


def print_entry_dict_as_bib(entry, print_fn=None):
    keys = list(entry.keys())
    ordered_keys = ['ENTRYTYPE', 'ID', 'title']
    if 'author' in entry.keys():
        ordered_keys.append('author')
    remaining_keys = [k for k in keys if k not in ordered_keys]
    keys = ordered_keys + remaining_keys
    merged = ',\n'.join(['    %s={%s}' % (k, entry[k]) for k in keys[2:]])

    if print_fn is None:
        print("@%s{%s,\n%s\n}\n\n" % (entry['ENTRYTYPE'], entry['ID'], merged))
    else:
        print_fn("@%s{%s,\n%s\n}\n\n", entry['ENTRYTYPE'], entry['ID'], merged)


us_state_abbrev = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'American Samoa': 'AS',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'District of Columbia': 'DC',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Guam': 'GU',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Northern Mariana Islands':'MP',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Puerto Rico': 'PR',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virgin Islands': 'VI',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY'
}

def trim(string):
    string = string.strip()
    string = string.replace('\n', ' ')
    while '  ' in string:
        string = string.replace('  ', ' ')
    string = string.replace('{', '').replace('}', '')
    return string


def remove_umlauts(string):
    # TODO: Add more patterns
    patterns = {
        "ä": '\\"a',
        "ü": '\\"u',
        "ö": '\\"o',
        "Ä": '\\"A',
        "Ü": '\\"U',
        "Ö": '\\"O',
        "é": "\\'e",
        "ă": "\\ua",
        "á": "\\'a",
        "ò": "\\`{o}",
        "ó": "\\'{o}",
        "ô": "\\^{o}",
        "ö": '\\"{o}',
        "ő": "\\H{o}",
        "õ": "\\~{o}",
        "ç": "\\c{c}",
        "ą": "\\k{a}",
        "ł": "\\l{} ",
        "ō": "\\={o}",
        "ȯ": "\\.{o}",
        "ụ": "\\d{u}",
        "å": "\\r{a}",
        "ŏ": "\\u{o}",
        "š": "\\v{s}",
        "ø": "\\o{}",
        "ı": "{\\i}",
        "o͡o": "\\t{oo}",
    }
    #ă
    for k, v in patterns.items():
        string = string.replace(k, v)
    return string


def isclose(a, b):
    return pylcs.lcs(a.lower(), b.lower()) / max(len(a), len(b)) > 0.95


def non_capitalized_words(title):
    words = []
    for word in [word.strip().replace('"', '').replace(",", '').replace(":", '')
                 for word in title.split()
                 if word.lower() not in stop_words.ENGLISH_STOP_WORDS]:
        words.extend(word.split('-'))
    non_capitalized = list(filter(
        lambda x: (x != x.capitalize() and x != x.upper() and
            x.lower() not in stop_words.ENGLISH_STOP_WORDS), words))
    return non_capitalized
