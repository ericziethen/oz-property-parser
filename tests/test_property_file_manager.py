#!/usr/bin/env python3

import pytest

import property_file_manager
import property_parser_nsw

################################
# Module Function Tests
################################
PROPERTY_FILE_CLASS_IDENTIFIED = [
    ('004_SALES_DATA_NNME_15012018.DAT', property_parser_nsw.NswNewPropertyFile),
    ('ARCHIVE_SALES_1990.DAT', property_parser_nsw.NswOldPropertyFile)
]
@pytest.mark.parametrize('file_name, property_class', PROPERTY_FILE_CLASS_IDENTIFIED)
def test_get_property_file_from_path(file_name, property_class):
    result = property_file_manager.get_property_file_from_path(file_name)

    assert result is not None
    assert result == property_class


PROPERTY_FILE_CLASS_NOT_IDENTIFIED = [
    ('INVALID')
]
@pytest.mark.parametrize('file_name', PROPERTY_FILE_CLASS_NOT_IDENTIFIED)
def test_get_property_file_from_path_invalid(file_name):
    with pytest.raises(ValueError):
        property_file_manager.get_property_file_from_path(file_name)
