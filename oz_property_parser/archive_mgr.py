#!/usr/bin/env python3

"""Module to manage archives."""

import logging
import os
import zipfile

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


class ExtractionError(Exception):
    """Generic exception to indicate exception failes."""


def _unzip(file_path: str, dest_dir: str) -> None:
    """Unzip the given file to the given dir."""
    try:
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(dest_dir)
    except (ValueError, zipfile.BadZipFile) as error:
        raise ExtractionError(F'Failed to unzip Archive with error "{error}"')


_ZIP_FILE_MAPPING = {
    # Extension: (Zip, Unzip)
    'zip': (None, _unzip)
}


def file_is_archive(file_path: str) -> bool:
    """Check if the file is a supported archive file."""
    ext = file_path.split(os.extsep)[-1]
    return ext.lower() in _ZIP_FILE_MAPPING.keys()


def extract(file_path: str, dest_dir: str) -> None:
    """Extract the given file to the given dir."""
    ext = file_path.split(os.extsep)[-1].lower()
    try:
        archive_tuple = _ZIP_FILE_MAPPING[ext]
    except KeyError:
        raise ExtractionError(F'Extraction not supported for "{file_path}"')
    else:
        extract_func = archive_tuple[1]
        if extract_func:
            extract_func(file_path, dest_dir)
        else:
            raise NotImplementedError('Extract for "{ext}" not implemented')


def test() -> None:
    """Test function."""


if __name__ == '__main__':
    test()
