#!/usr/bin/env python3

"""Manage the Database."""

import logging

from contextlib import contextmanager

import sqlalchemy

from sqlalchemy import (Boolean, Column, Integer, String, ForeignKey, Table,
                        UniqueConstraint, create_engine, Unicode)

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.interfaces import PoolListener

from sqlalchemy.orm import relationship, sessionmaker, mapper

Base = declarative_base()  # pylint: disable=invalid-name

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


class ScannedFile(Base):
    """Represent the already scanned files."""

    # pylint: disable=too-few-public-methods

    __tablename__ = 'scanned_file'

    # Use ID, keeps the foreign key size smalle
    id = Column(Integer, primary_key=True)  # pylint: disable=invalid-name
    full_path = Column(String)
    processed = Column(Boolean)
    size_bytes = Column(String)
    checksum = Column(String)

    extracted_from_id = Column(Integer, ForeignKey('scanned_file.id'))
    extracted_from = relationship("ScannedFile", remote_side=[id])

    UniqueConstraint('size_bytes', 'checksum', name='uix_1')


class SalesData():  # pylint: disable=too-few-public-methods
    """Sales Data DB."""


class SqliteForeignKeysListener(PoolListener):
    """Class to setup Foreign Keys."""

    def connect(self, dbapi_con, con_record):
        """Connect the key listener."""
        dbapi_con.execute('pragma foreign_keys=ON')


class SqliteDb():
    """SQLAlchemy Sqlite database connection."""

    def __init__(self, db_path):
        """Initialize the Sqlite Database."""
        self.connection_string = 'sqlite:///' + db_path
        self._session_func = None
        self._engine = None

    def __enter__(self):
        self._engine = create_engine(
            self.connection_string,
            # echo=True,
            listeners=[SqliteForeignKeysListener()])  # Enforce Foreign Keys

        self._session_func = sessionmaker(bind=self._engine)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def create(self, sales_data_columns):
        """Create this SQL Database."""
        sales_table = Table(
            'SalesData', Base.metadata,
            Column('id', Integer, primary_key=True),
            *(Column(col, Unicode(255)) for col in sales_data_columns))
        mapper(SalesData, sales_table)

        Base.metadata.create_all(self._engine)

    @contextmanager
    def session_scope(self):
        """Provide a transactional scope around a series of operations."""
        session = self._session_func()
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()


class DataManager():
    """Manager for combined commits."""

    def __init__(self, session, commit_max=10000):
        """Initialize Datamanager."""
        logger.info('DataManager.__init__()')
        self._commit_max = commit_max
        self._property_count = 0
        self._property_list = []
        self._session = session
        self._commit_count = 0
        self._property_total = 0

    def __enter__(self):
        logger.info('DataManager.__enter__()')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.commit()
        logger.debug(F'Added Properties: {self._property_total}')
        logger.debug(F'Commits: {self._commit_count}')

    def add_scanned_file(self, scanned_file: ScannedFile) -> None:
        """Add a scanned file entry."""
        self._session.add(scanned_file)
        self._session.flush()

    def find_scanned_file(self, size: int,
                          checksum: int) -> sqlalchemy.orm.query.Query:
        """Find a scanned file."""
        return self._session.query(ScannedFile).filter_by(
            size_bytes=size, checksum=checksum).first()

    def add_property_list(self, property_list) -> None:
        """Add a list of properties to Datamanager."""
        count = len(property_list)
        self._property_list += property_list
        self._property_count += count
        self._property_total += count

        if self._property_count >= self._commit_max:
            self.commit()

    def commit(self):
        """Commit the data of Datamanager."""
        logger.info('DataManager.commit()')
        if self._property_count > 0:
            logger.info(F'Property Count: {self._property_count}')
            insert_bulk_sales_data(self._session, self._property_list)
            self._session.commit()
            self._property_count = 0
            self._commit_count += 1
            del self._property_list[:]
            logger.info((F'Properties Added: {self._property_total:20}'
                         F', Commits: {self._commit_count:10}'))


def insert_bulk_sales_data(session, data_dic):
    """Insert bulk data into this session."""
    session.bulk_insert_mappings(SalesData, data_dic)
