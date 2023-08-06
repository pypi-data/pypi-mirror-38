# coding: utf-8

"""This module has the parser for miRBase."""

import gzip
from typing import Dict, Iterable, List

from tqdm import tqdm


def parse_definitions(path: str) -> List[Dict]:
    """Parse miRNA data from filepath and convert it to dictionary.

    The structure of dictionary is {ID:[AC,DE,[[miRNA],[miRNA]]]}

    :param path: The path to the miRBase file
    """
    with (gzip.open(path, 'r') if path.endswith('.gz') else open(path)) as file:
        return process_definitions_lines(file)


def process_definitions_lines(lines: Iterable[str]) -> List[Dict]:
    """Process the lines of the definitions file."""
    groups = []

    for line in lines:
        if line.startswith('ID'):
            listnew = []
            groups.append(listnew)

        groups[-1].append(line)

    # print(groups[0][0][5:18])
    rv = []
    for group in tqdm(groups, desc='parsing'):
        name = group[0][5:23].strip()
        identifier = group[2][3:-2].strip()
        description = group[4][3:-1].strip()

        entry_data = {
            'name': name,
            'description': description,
            'identifier': identifier
        }

        mature_mirna_lines = [
            i
            for i, element in enumerate(group)
            if 'FT   miRNA    ' in element
        ]

        entry_data['products'] = [
            {
                'location': group[index][10:-1].strip(),
                'accession': group[index + 1][33:-2],
                'product': group[index + 2][31:-2],
            }
            for index in mature_mirna_lines
        ]

        entry_data['xrefs'] = [
            {
                'database': '',
                'identifier': '',
            }
        ]  # TODO @lingling93

        rv.append(entry_data)

    return rv
