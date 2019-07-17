#!/usr/bin/env python3

"""Module to manage the different known Property Files and parsers."""

import os

from typing import Type

import property_parser
import property_parser_nsw

_PROPERTY_FILE_CLASSES = [
    property_parser_nsw.NswOldPropertyFile,
    property_parser_nsw.NswNewPropertyFile
]


def get_property_file_from_path(
        path: str) -> Type[property_parser.PropertyFile]:
    """Get the correct nsw property file object for the given file path."""
    filename = os.path.basename(path)

    for prop_class in _PROPERTY_FILE_CLASSES:
        if prop_class.name_allowed(filename):
            return prop_class

    raise ValueError(F'{path} is not a Valid Property File')


def file_can_be_parsed(file_path: str) -> bool:
    """Check if the file can be parsed."""
    try:
        get_property_file_from_path(file_path)
    except ValueError:
        return False
    else:
        return True
