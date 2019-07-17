#!/usr/bin/env python3

import pytest

import property_parser
import property_parser_nsw


################################
# Tests for Class NswOldProperty
################################
def test_nsw_old_property_init():
    line = 'This is a fake line'
    prop = property_parser_nsw.NswOldProperty(line)

    assert prop.line == line
    for field in property_parser.PropertyData:
        assert prop[field] == ''

# TODO Need some stubs to test this paring
#def test_nsw_old_property_parse():


####################################
# Tests for Class NswOldPropertyFile
####################################
def test_nsw_old_property_file_init():
    file_path = R'file/path'
    prop = property_parser_nsw.NswOldPropertyFile(file_path)

    assert prop._file_path == file_path
    assert prop._encoding == 'utf8'
    assert prop._properties == []
    assert prop._idx == 0


OLD_FILE_NAMES_ALLOWED = [
    ('ARCHIVE_SALES_1990.DAT')
]
@pytest.mark.parametrize('name', OLD_FILE_NAMES_ALLOWED)
def test_nsw_old_property_file_name_allowed(name):
    assert property_parser_nsw.NswOldPropertyFile.name_allowed(name)


OLD_FILE_NAMES_NOT_ALLOWED = [
    ('001_SALES_DATA_NNME_15012018.DAT')
]
@pytest.mark.parametrize('name', OLD_FILE_NAMES_NOT_ALLOWED)
def test_nsw_old_property_file_name_allowed_failed(name):
    assert not property_parser_nsw.NswOldPropertyFile.name_allowed(name)


def test_nsw_old_property_file_create_property_from_line():
    prop = property_parser_nsw.NswOldPropertyFile(R'file/path')
    assert isinstance(prop.create_property_from_line('fake_line'), property_parser_nsw.NswOldProperty)


OLD_FILE_LINE_OF_INTEREST = [
    (R'''B;011;VALNET1;0145900000000;292674;;;ELDON ST;ABERDEEN;2336;20/11/1990;14500;LOT 7 SEC 22 DP 758003, LOT 8 SEC 22 DP 758003.;2365;M;;;A;;;;''')
]
@pytest.mark.parametrize('line', OLD_FILE_LINE_OF_INTEREST)
def test_nsw_old_property_file_line_of_interest(line):
    prop = property_parser_nsw.NswOldPropertyFile(R'file/path')
    assert prop.line_of_interest(line)


OLD_FILE_LINE_NOT_OF_INTEREST = [
    (R'''A;RTSALEDATA;001;20180115 01:15;VALNET;'''),
    (R'''C;001;3968570;148;20180115 01:15;928/1209451;'''),
    (R'''D;001;3968570;148;20180115 01:15;P;;;;;;'''),
    (R'''Z;732;148;148;434;'''),
    (R'''A;;VALNET1;20150909 11:33;;'''),
    (R'''Z;105333;105332;;''')
]
@pytest.mark.parametrize('line', OLD_FILE_LINE_NOT_OF_INTEREST)
def test_nsw_old_property_file_line_of_interest(line):
    prop = property_parser_nsw.NswOldPropertyFile(R'file/path')
    assert not prop.line_of_interest(line)


################################
# Tests for Class NswNewProperty
################################
def test_nsw_new_property_init():
    line = 'This is a fake line'
    prop = property_parser_nsw.NswNewProperty(line)

    assert prop.line == line
    for field in property_parser.PropertyData:
        assert prop[field] == ''

# TODO Need some stubs to test this paring
#def test_nsw_new_property_parse():

####################################
# Tests for Class NswNewPropertyFile
####################################
def test_nsw_new_property_file_init():
    file_path = R'file/path'
    prop = property_parser_nsw.NswNewPropertyFile(file_path)

    assert prop._file_path == file_path
    assert prop._encoding == 'utf8'
    assert prop._properties == []
    assert prop._idx == 0


NEW_FILE_NAMES_ALLOWED = [
    ('001_SALES_DATA_NNME_15012018.DAT')
]
@pytest.mark.parametrize('name', NEW_FILE_NAMES_ALLOWED)
def test_nsw_new_property_file_name_allowed(name):
    assert property_parser_nsw.NswNewPropertyFile.name_allowed(name)


NEW_FILE_NAMES_NOT_ALLOWED = [
    ('ARCHIVE_SALES_1990.DAT')
]
@pytest.mark.parametrize('name', NEW_FILE_NAMES_NOT_ALLOWED)
def test_nsw_new_property_file_name_allowed_failed(name):
    assert not property_parser_nsw.NswNewPropertyFile.name_allowed(name)


def test_nsw_new_property_file_create_property_from_line():
    prop = property_parser_nsw.NswNewPropertyFile(R'file/path')
    assert isinstance(prop.create_property_from_line('fake_line'), property_parser_nsw.NswNewProperty)


NEW_FILE_LINE_OF_INTEREST = [
    (R'''B;001;3771736;141;20180115 01:15;;;73 A;KLINE ST;WESTON;2326;802.3;M;20171121;20171219;515000;R2;R;RESIDENCE;;AAN;;0;AN8513;''')
]
@pytest.mark.parametrize('line', NEW_FILE_LINE_OF_INTEREST)
def test_nsw_new_property_file_line_of_interest(line):
    prop = property_parser_nsw.NswNewPropertyFile(R'file/path')
    assert prop.line_of_interest(line)


NEW_FILE_LINE_NOT_OF_INTEREST = [
    (R'''A;RTSALEDATA;001;20180115 01:15;VALNET;'''),
    (R'''C;001;3968570;148;20180115 01:15;928/1209451;'''),
    (R'''D;001;3968570;148;20180115 01:15;P;;;;;;'''),
    (R'''Z;732;148;148;434;'''),
    (R'''A;;VALNET1;20150909 11:33;;'''),
    (R'''Z;105333;105332;;''')
]
@pytest.mark.parametrize('line', NEW_FILE_LINE_NOT_OF_INTEREST)
def test_nsw_new_property_file_line_of_interest(line):
    prop = property_parser_nsw.NswNewPropertyFile(R'file/path')
    assert not prop.line_of_interest(line)
