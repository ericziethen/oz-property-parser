#!/usr/bin/env python3

"""Module to manage the different known Property Files and parsers."""

import os

import property_parser
import property_parser_nsw


def get_property_file_from_path(path: str) -> property_parser.PropertyFile:
    """Get the correct nsw property file object for the given file path."""
    filename = os.path.basename(path)
    if property_parser_nsw.NswOldPropertyFile.name_allowed(filename):
        return property_parser_nsw.NswOldPropertyFile(path)
    if property_parser_nsw.NswNewPropertyFile.name_allowed(filename):
        return property_parser_nsw.NswNewPropertyFile(path)

    raise ValueError(F'{path} is not a Valid NSW Property File')