# -*- coding: utf-8 -*-

"""Test constants for Bio2BEL miRBase."""

import os

from bio2bel.testing import AbstractTemporaryCacheClassMixin
from bio2bel_mirbase import Manager

HERE = os.path.dirname(os.path.realpath(__file__))

TEST_SPECIES_PATH = os.path.join(HERE, 'test_species.tsv')
TEST_DEFINITONS_PATH = os.path.join(HERE, 'mirbase_test_data.dat')


class TemporaryCacheClass(AbstractTemporaryCacheClassMixin):
    """A test case containing a temporary database and a Bio2BEL miRBase manager."""

    Manager = Manager
    manager: Manager

    @classmethod
    def populate(cls):
        """Populate the mock database."""
        cls.manager.populate(
            species_path=TEST_SPECIES_PATH,
            definitions_path=TEST_DEFINITONS_PATH,
        )
