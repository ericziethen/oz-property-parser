#!/usr/bin/env python3

import pytest

import property_parser


################################
# Tests for Class Property
################################
def test_property_init():
    line = 'This is a fake line'
    prop = property_parser.Property(line)

    assert prop.line == line
    for field in property_parser.PropertyData:
        assert prop[field] == ''


def test_property_parse():
    prop = property_parser.Property('This is a fake line')
    with pytest.raises(NotImplementedError):
        prop.parse()


################################
# Tests for Class PropertyFile
################################

def test_property_file_init():
    file_path = R'file/path'
    prop = property_parser.PropertyFile(file_path)

    assert prop._file_path == file_path
    assert prop._encoding == 'utf8'
    assert prop._properties == []
    assert prop._idx == 0


def test_property_file_name_allowed():
    with pytest.raises(NotImplementedError):
        property_parser.PropertyFile.name_allowed('file_name')


def test_property_file_create_property_from_line():
    prop = property_parser.PropertyFile(R'file/path')
    with pytest.raises(NotImplementedError):
        prop.create_property_from_line('This is a fake line')


def test_property_file_line_of_interest():
    prop = property_parser.PropertyFile(R'file/path')
    assert prop.line_of_interest('This is a fake line')


# TODO Need some stubs to test this paring
#def test_property_file_parse():
