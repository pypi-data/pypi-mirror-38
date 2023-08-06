# -*- coding: utf-8 -*-

"""SQLAlchemy database models."""

from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import backref, relationship

import pybel.dsl
from .constants import MODULE_NAME

__all__ = [
    'Sequence',
    'MatureSequence',
    'Species',
    'Base',
]

Base: DeclarativeMeta = declarative_base()

SEQUENCE_TABLE_NAME = f'{MODULE_NAME}_sequence'
SEQUENCE_XREF_TABLE_NAME = f'{MODULE_NAME}_sequence_xref'
SPECIES_TABLE_NAME = f'{MODULE_NAME}_species'
MATURE_TABLE_NAME = f'{MODULE_NAME}_mature'


class Species(Base):
    """Represents a taxonomy."""

    __tablename__ = SPECIES_TABLE_NAME

    id = Column(Integer, primary_key=True)

    organism = Column(String(16), unique=True, index=True, doc='Three letter species code')
    division = Column(String(16), unique=True, index=True, doc='Three letter species code')
    name = Column(Text, unique=True, index=True, doc='Three letter species code')
    tree = Column(Text)
    taxonomy_id = Column(String(32), doc='NCBI taxonomy identifier')


class Sequence(Base):
    """Represents an miRBase sequence.

    See https://www.ebi.ac.uk/miriam/main/datatypes/MIR:00000078
    """

    __tablename__ = SEQUENCE_TABLE_NAME

    id = Column(Integer, primary_key=True)

    mirbase_id = Column(String(255), nullable=False, unique=True, index=True,
                        doc=r'miRBase sequence matching ``MI\d{7}``')

    name = Column(String(255), nullable=False, unique=True, index=True)
    description = Column(Text, nullable=False)

    species_id = Column(ForeignKey(f'{Species.__tablename__}.id'))
    species = relationship(Species)

    def __repr__(self):  # noqa: D105
        return str(self.mirbase_id)

    def as_pybel(self) -> pybel.dsl.MicroRna:
        """Serialize this entity as a PyBEL microRNA."""
        return pybel.dsl.MicroRna(
            namespace='mirbase',
            name=self.name,
            identifier=self.mirbase_id,
        )


class SequenceXrefs(Base):
    """Represents cross-references for sequences."""

    __tablename__ = SEQUENCE_XREF_TABLE_NAME

    id = Column(Integer, primary_key=True)

    sequence_id = Column(ForeignKey(f'{Sequence.__tablename__}.id'))
    sequence = relationship(Sequence, backref=backref('xrefs'))

    database = Column(String(255), nullable=False, index=True)
    database_id = Column(String(255), nullable=False, index=True)


class MatureSequence(Base):
    """Represents a miRBase mature sequence.

    See: https://www.ebi.ac.uk/miriam/main/datatypes/MIR:00000235

    Regular Expression:
    """

    __tablename__ = MATURE_TABLE_NAME

    id = Column(Integer, primary_key=True)

    mirbase_mature_id = Column(String(255), nullable=False, unique=True, index=True,
                               doc=r'miRBase mature sequence matching ``MIMAT\d{7}``')

    name = Column(String(255), nullable=False, index=True)

    start = Column(Integer)
    stop = Column(Integer)

    sequence_id = Column(ForeignKey(f'{Sequence.__tablename__}.id'))
    sequence = relationship(Sequence, backref=backref('mature_sequences'))

    def as_pybel(self) -> pybel.dsl.MicroRna:
        """Serialize this entity as a PyBEL microRNA."""
        return pybel.dsl.MicroRna(
            namespace='mirbase.mature',
            name=self.name,
            identifier=self.mirbase_mature_id,
        )
