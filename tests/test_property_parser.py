#!/usr/bin/env python3

import pytest

import property_parser

################################
# Tests for Enum PropertyData
################################
def test_ensure_enum_correct():
    for field in property_parser.PropertyData:
        assert isinstance(field.value, str)
        assert ' ' not in field.value

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
    with pytest.raises(NotImplementedError):
        prop.line_of_interest('This is a fake line')


# TODO Need some stubs to test this paring
#def test_property_file_parse():


################################
# Module Function Tests
################################
TIME_CONVERSION = [
    ('23:30:01,123', '23:30:01,123456', '%H:%M:%S,%f'),
    ('23:30:01,000', '23:30:01', '%H:%M:%S')
]
@pytest.mark.parametrize('expected_time, time, time_format', TIME_CONVERSION)
def test_convert_date_to_internal(expected_time, time, time_format):
    assert expected_time == property_parser.convert_time_to_internal(time, time_format)


DATE_CONVERSION = [
    ('2018/10/21', '2018/10/21', '%Y/%M/%d'),
    ('2018/10/21', '10/21/2018', '%M/%d/%Y'),
    ('2018/01/02', '02-01-2018', '%d-%M-%Y')
]
@pytest.mark.parametrize('expected_date, date, date_format', DATE_CONVERSION)
def test_convert_time_to_internal(expected_date, date, date_format):
    assert expected_date == property_parser.convert_date_to_internal(date, date_format)

SPLIT_STR = [
    (['Test'], 'Test', ','),
    (['Test, List'], 'Test, List', ';'),
    (['Test', 'List'], 'Test, List', ',')
]
@pytest.mark.parametrize('expected_list, text, separator', SPLIT_STR)
def test_split_str(expected_list, text, separator):
    assert expected_list == property_parser.split_str(text, separator)
