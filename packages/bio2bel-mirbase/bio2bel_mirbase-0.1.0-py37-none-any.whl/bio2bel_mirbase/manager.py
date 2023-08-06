# -*- coding: utf-8 -*-

"""Bio2BEL miRBase manager."""

import logging
from typing import Dict, List, Mapping, Optional

from tqdm import tqdm

from bio2bel import AbstractManager
from bio2bel.manager.bel_manager import BELManagerMixin
from bio2bel.manager.flask_manager import FlaskMixin
from bio2bel.manager.namespace_manager import BELNamespaceManagerMixin
from pybel import BELGraph
from pybel.dsl import mirna
from pybel.manager.models import Namespace, NamespaceEntry
from .constants import MODULE_NAME
from .download import download_definitions, get_species_df
from .models import Base, MatureSequence, Sequence, Species
from .parser import parse_definitions

__all__ = [
    'Manager',
]

log = logging.getLogger(__name__)


class Manager(AbstractManager, BELNamespaceManagerMixin, BELManagerMixin, FlaskMixin):
    """A manager for Bio2BEL miRBase."""

    _base = Base
    module_name = MODULE_NAME
    flask_admin_models = [Sequence, MatureSequence, Species]

    namespace_model = Sequence
    identifiers_recommended = 'miRBase'
    identifiers_pattern = r'MI\d{7}'
    identifiers_miriam = 'MIR:00000078'
    identifiers_namespace = 'mirbase'
    identifiers_url = 'http://identifiers.org/mirbase/'

    def count_sequences(self) -> int:
        """Count the sequences in the database."""
        return self._count_model(Sequence)

    def count_mature_sequences(self) -> int:
        """Count the mature sequences in the database."""
        return self._count_model(MatureSequence)

    def count_species(self) -> int:
        """Count the species in the database."""
        return self._count_model(Species)

    def summarize(self) -> Mapping[str, int]:
        """Summarize the contents of the database."""
        return dict(
            sequences=self.count_sequences(),
            mature_sequences=self.count_mature_sequences(),
            species=self.count_species()
        )

    def is_populated(self) -> bool:
        """Check if the database is populated."""
        return 0 < self.count_sequences()

    def get_species_by_taxonomy_id(self, taxonomy_id: str) -> Optional[Species]:
        """Get a species by its NCBI taxonomy identifier, if it exists."""
        return self.session.query(Species).filter(Species.taxonomy_id == taxonomy_id).one_or_none()

    def get_sequence_by_mirbase_id(self, mirbase_id: str) -> Optional[Sequence]:
        """Get a sequence by its miRBase identifier, if it exists."""
        return self.session.query(Sequence).filter(Sequence.mirbase_id == mirbase_id).one_or_none()

    def get_sequence_by_name(self, name: str) -> Optional[Sequence]:
        """Get a sequence by name, if it exists."""
        return self.session.query(Sequence).filter(Sequence.name == name).one_or_none()

    def populate(self, species_path: Optional[str] = None, definitions_path: Optional[str] = None,
                 force_download: bool = False) -> None:
        """Populate the database."""
        self._populate_species(path=species_path, force_download=force_download)
        self._populate_definitions(path=definitions_path, force_download=force_download)

    def _populate_species(self, path: Optional[str] = None, force_download: bool = False):
        """Populate the species in the database."""
        species_df = get_species_df(path, force_download=force_download)
        species_df.to_sql(Species.__tablename__, con=self.engine, if_exists='append', index=False)
        self.session.commit()

    def _populate_definitions(self, path: Optional[str] = None, force_download: bool = False):
        if path is None:
            path = download_definitions(force_download=force_download)
        definitions = parse_definitions(path)
        self._populate_definitions_helper(definitions)

    def _populate_definitions_helper(self, definitions_list: List[Dict]) -> None:
        mature_sequences = {}

        for entry in tqdm(definitions_list, desc='definitions'):
            sequence = Sequence(
                mirbase_id=entry['identifier'],
                name=entry['name'],
                description=entry['description'],
            )

            for product in entry.get('products', []):
                mirbase_mature_id = product['accession']

                mature_sequence = mature_sequences.get(mirbase_mature_id)
                if mature_sequence is None:
                    start, stop = map(int, product['location'].split('..'))

                    mature_sequences[mirbase_mature_id] = mature_sequence = MatureSequence(
                        name=product['product'],
                        mirbase_mature_id=mirbase_mature_id,
                        start=start,
                        stop=stop,
                    )

                sequence.mature_sequences.append(mature_sequence)

            self.session.add(sequence)
        self.session.commit()

    def _create_namespace_entry_from_model(self, sequence: Sequence, namespace: Namespace) -> NamespaceEntry:
        return NamespaceEntry(
            name=sequence.name,
            identifier=sequence.mirbase_id,
            encoding='GM',
            namespace=namespace,
        )

    @staticmethod
    def _get_identifier(sequence: Sequence) -> str:
        return sequence.mirbase_id

    def to_bel(self) -> BELGraph:
        """Convert miRBase to BEL."""
        result = BELGraph()

        for sequence in self._get_query(Sequence):
            mirbase_node = sequence.as_pybel()

            for xref in sequence.xrefs:
                xref_node = mirna(
                    namespace=xref.database,
                    identifier=xref.database_id,
                )

                result.add_equivalence(mirbase_node, xref_node)

        return result
