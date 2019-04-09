#!/urs/bin/env python3

import pytest

import archive_mgr

SUPPORTED_ARCHIVES = [
    (R'Test.zip'),
    (R'Test.Zip'),
    (R'path_to/Test.zip'),
    (R'path_to\Test.zip'),
    (R'c:\Test.zip'),
    (R'C:\Path\To\Test.Zip')
]
@pytest.mark.parametrize('archive_name', SUPPORTED_ARCHIVES)
def test_file_is_archived(archive_name):
    assert archive_mgr.file_is_archive(archive_name)


NON_SUPPORTED_ARCHIVES = [
    (R'Test.rar'),
    (R'Test.Rar'),
    (R'path_to/Test.rar')
]
@pytest.mark.parametrize('archive_name', NON_SUPPORTED_ARCHIVES)
def test_file_is_archived(archive_name):
    assert not archive_mgr.file_is_archive(archive_name)


def test_extract_invalid_archive():
    with pytest.raises(archive_mgr.ExtractionError):
        archive_mgr.extract(R'File.rar', R'fake_dest_dir')
