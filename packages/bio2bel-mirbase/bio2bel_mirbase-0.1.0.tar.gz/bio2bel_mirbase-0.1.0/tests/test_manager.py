# -*- coding: utf-8 -*-

"""Tests for Bio2BEL miRBase."""

import unittest

from bio2bel_mirbase import get_version
from bio2bel_mirbase.models import Sequence, Species
from tests.constants import TemporaryCacheClass


class TestMeta(unittest.TestCase):
    """Test metadata from Bio2BEL miRBase."""

    def test_get_version(self):
        """Test the get_version function."""
        self.assertIsInstance(get_version(), str)


class TestPopulate(TemporaryCacheClass):
    """Test the populated database."""

    def test_count(self):
        """Test the counts in the database."""
        self.assertEqual(2, self.manager.count_sequences())

    def test_lookup_species(self):
        """Test getting a species from the database."""
        model = self.manager.get_species_by_taxonomy_id('6239')
        self.assertIsNotNone(model)
        self.assertIsInstance(model, Species)
        self.assertEqual('cel', model.organism)
        self.assertEqual('CEL', model.division)
        self.assertEqual('Caenorhabditis elegans', model.name)
        self.assertEqual('6239', model.taxonomy_id)

    def test_lookup_sequence(self):
        """Test getting a sequence from the database."""
        models = [
            self.manager.get_sequence_by_name('cel-let-7'),
            self.manager.get_sequence_by_mirbase_id('MI0000001'),
        ]

        for model in models:
            self.assertIsNotNone(model)
            self.assertIsInstance(model, Sequence)
            self.assertEqual('MI0000001', model.mirbase_id)
            self.assertEqual('cel-let-7', model.name)
            self.assertEqual('Caenorhabditis elegans let-7 stem-loop', model.description)
