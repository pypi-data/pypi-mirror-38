# -*- coding: utf-8 -*-

"""Utilities for downloading miRBase."""

from bio2bel.downloading import make_df_getter, make_downloader
from .constants import DEFINITIONS_PATH, DEFINITIONS_URL, SPECIES_HEADER, SPECIES_PATH, SPECIES_URL

__all__ = [
    'get_species_df',
    'download_definitions',
]

get_species_df = make_df_getter(
    SPECIES_URL,
    SPECIES_PATH,
    sep='\t',
    names=SPECIES_HEADER,
)

download_definitions = make_downloader(DEFINITIONS_URL, DEFINITIONS_PATH)
