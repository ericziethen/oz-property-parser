#!/usr/bin/env python3

"""Module to handle Generic Property Log parsing."""

import collections
import datetime
import enum
import logging
import os

from typing import List

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
    ZONE = 'Zone'
    ZONE_TYPE = 'Zone Class'

    # pylint: enable=invalid-name


class Property():
    """Property Line base class."""

    def __init__(self, line):
        """Initialize Property Line."""
        self.line = line

        self._fields = collections.defaultdict(str)

    def parse(self) -> bool:
        """Parse the property line."""
        raise NotImplementedError

    def get_field_dic(self):
        """Get a list of all the fields as dictionaries."""
        return self._fields

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

    def get_lines_as_list(self):
        """Get a list of all the properties."""
        data_list = []

        # Prepare the result
        for property_file in self:
            data_list.append(property_file.get_field_dic())

        return data_list

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


def convert_date_to_internal(date_str: str, date_format: str):
    """Convert the given date to the internal format."""
    return datetime.datetime.strptime(
        date_str, date_format).strftime('%Y/%M/%d')


def convert_time_to_internal(time_str: str, time_format: str):
    """Convert the given time to the internal format."""
    return datetime.datetime.strptime(
        time_str, time_format).time().strftime('%H:%M:%S,%f')[:-3]


def split_str(text: str, sep: str):
    """Split the gives string by the given separator."""
    split_list = [x.strip() for x in text.split(sep)]
    return split_list
