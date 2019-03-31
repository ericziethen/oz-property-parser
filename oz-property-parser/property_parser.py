#!/usr/bin/env python3

"""Module to handle Generic Property Log parsing."""

import enum
import logging
import os

from typing import Dict, List

import project_logger

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


@enum.unique
class PropertyData(enum.Enum):
    """Enum to break down a log line."""

    # Disable Enum variable name warning temporarily
    # pylint: disable=invalid-name

    # Property Details
    PROPERTY_ID = 'Property ID'
    AREA = 'Area'
    AREA_TYPE = 'Area Type'
    DIMENSIONS = 'Dimensions'
    LAND_DESCRIPTIONS = 'Land Descriptions'
    LOT_NUMBER = 'Lot Number'

    # Address Details
    DISTRICT_CODE = 'DIstrict Code'
    UNIT_NUMBER = 'Unit Number'
    HOUSE_NUMBER = 'House Number'
    STREET_NAME = 'Street Name'
    SUBBURB = 'Subburb'
    POST_CODE = 'Post Code'

    # Sales Details
    CONTRACT_DATE = 'Contract Date'
    SETTLEMENT_DATE = ' Settlement Date'
    PURCHASE_PRICE = 'Purchase Price'

    # Misc
    NATURE_OF_PROPERTY = 'Nature pof Property'
    PRIMARY_PURPOSE = 'Primary Purpose'
    ZONE_CODE = 'Zone Code'

    # pylint: enable=invalid-name


class Property():
    """Property Line base class."""

    def __init__(self, line):
        """Initialize Property Line."""
        self.line = line
        self._fields: Dict[PropertyData, str] = {}

        # Give each possible field blank values
        for key in PropertyData:
            self[key] = ''

    def parse(self):
        """Parse the property line."""
        raise NotImplementedError

    def __setitem__(self, key: PropertyData, value):
        self._fields[self.__keytransform__(key)] = value

    def __getitem__(self, key: PropertyData):
        return self._fields[self.__keytransform__(key)]

    def __iter__(self):
        return iter(self._fields)

    def __len__(self):
        return len(self._fields)

    def __str__(self):
        return str(self._fields)

    def __keytransform__(self, key: PropertyData):
        return key.value

    def __delitem__(self, key: PropertyData):
        del self._fields[self.__keytransform__(key)]


class PropertyFile():
    """Property File base class."""

    def __init__(self, file_path: str):
        """Initialize the generic property file."""
        self._file_path = file_path
        self._encoding = 'utf8'
        self._properties: List[Property] = []
        self._idx = 0

    @property
    def _file_name(self) -> str:
        """Get the file name."""
        return os.path.basename(self._file_path)

    @staticmethod
    def name_allowed(file_name_candidate: str) -> bool:
        """Check if the given name is allowed."""
        raise NotImplementedError

    def create_property_from_line(self, line: str) -> Property:
        """Create a property object for this class."""
        raise NotImplementedError

    def line_of_interest(self, line):
        """Check if File line is of interest."""
        raise NotImplementedError

    def parse(self) -> None:
        """Parse the property file."""
        with open(self._file_path, 'r', encoding=self._encoding) as prop_file:
            for raw_line in prop_file:
                line = raw_line.strip()
                if self.line_of_interest(line):
                    # For now let's assume we only need a single line for each
                    # property. New NSW entries have multiple lines per
                    # property but only 1 has data we are interested in
                    # single line makes parsing a lot simpler for now
                    prop = self.create_property_from_line(line)
                    if prop.parse():
                        self._properties.append(prop)
                    else:
                        raise ValueError(F'Failed Parsing Line: "{line}"')

    def __iter__(self):
        self._idx = 0
        return self

    def __next__(self):
        try:
            item = self._properties[self._idx]
        except IndexError:
            raise StopIteration()
        self._idx += 1
        return item

    def __len__(self):
        return len(self._properties)

    def __getitem__(self, idx):
        return self._properties[idx]


def test():
    """Test Function."""
    project_logger.setup_logger(R'..\#TestFiles\logfile.txt')
    file_path = R'..\#TestFiles\ARCHIVE_SALES_1990.DAT'

    logger.info('Creating Test Property File')
    prop_file = PropertyFile(file_path)
    logger.info('Start Parsing')
    prop_file.parse()
    logger.info('Finish Parsing')

    for prop in prop_file:
        logger.debug(F'{prop}')


if __name__ == '__main__':
    test()
