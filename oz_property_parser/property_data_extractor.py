#!/usr/env/bin python3

"""Main program to run the property data extractor."""

import argparse
import csv
import logging
import os
import shutil

from typing import List

import archive_mgr
import property_file_manager as prop_mgr
import property_parser
import project_logger

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


def parse_args() -> argparse.Namespace:
    """Set up command line arguments for Transdump."""
    parser = argparse.ArgumentParser()
    parser.add_argument('dir',
                        help='Base search Dir for property Files')
    return parser.parse_args()


def validate_args(args: argparse.Namespace) -> None:
    """Validate the command line arguments."""
    if (not os.path.exists(args.dir)) or (not os.path.isdir(args.dir)):
        raise ValueError(F'"{args.dir}" is not a vaid directory')


def get_csv_keys() -> List[str]:
    """Create a list of csv keys."""
    key_list = []
    ignore_keys: List[property_parser.PropertyData] = []

    for field in property_parser.PropertyData:
        if field not in ignore_keys:
            key_list.append(field.value)

    logger.debug(F'Created Key List: {key_list}')

    return key_list


def write_property_to_csv(csv_path: str,
                          property_file: property_parser.PropertyFile) -> None:
    """Write the parsed log file to a csv file."""
    write_header = not os.path.exists(csv_path)

    # Get the data to write (List of Dics to write)
    csv_data = property_file.get_lines_as_list()

    logger.info(F'Writing/Appending to: "{csv_path}"')
    with open(csv_path, 'a', encoding='utf-8') as csv_file:
        dict_writer = csv.DictWriter(csv_file, delimiter=',',
                                     lineterminator='\n',
                                     extrasaction='ignore',
                                     fieldnames=get_csv_keys())
        if write_header:
            logger.debug(F'Writing Header Row')
            dict_writer.writeheader()
        logger.debug(F'Writing {len(csv_data)} entries')
        dict_writer.writerows(csv_data)


def parse_path(path: str, csv_path: str) -> None:
    """Parse the path for Property files."""
    logger.info(F'Parse Property files in "{path}"')

    for root, _, files in os.walk(path):
        for filename in files:
            file_path = os.path.join(root, filename)
            logger.info(F'Process "{file_path}"')

            # Check file for extraction
            if archive_mgr.file_is_archive(file_path):
                dest_dir = os.path.join(root, 'EXTRACT_' + filename)
                logger.info(F'Extracting "{file_path}" to "{dest_dir}"')
                try:
                    archive_mgr.extract(file_path, dest_dir)
                except archive_mgr.ExtractionError as error:
                    logger.exception('Extraction Error: "{error}"')
                else:
                    # Check the Extracted folder for Files as well
                    parse_path(dest_dir, csv_path)

                    # Delete the created folder again
                    logger.debug(F'Deleting Extration directory "{dest_dir}"')
                    try:
                        shutil.rmtree(dest_dir)
                    except OSError as error:
                        logger.exception(
                            F'Deletion Failed to delete "{dest_dir}", Error: "{error}"')
                    else:
                        logger.debug('Deletion Succeeded')

            else:
                # Process the file as property file
                try:
                    property_file = prop_mgr.get_property_file_from_path(
                        file_path)
                except ValueError as error:
                    logger.error(F'Failed to Identify Property File: {error}')
                else:
                    logger.info('Parse Log File')
                    property_file.parse()

                    write_property_to_csv(csv_path, property_file)
                    logger.info('Parsing complete')


def main() -> None:
    """Run the log parser."""
    # Parse command line arguments
    args = parse_args()
    validate_args(args)

    # Setup the logger
    project_logger.setup_logger(
        os.path.join(args.dir, R'property_parser.log'))

    logger.info(F'Command Line Arguments: "{args}"')

    # Process Log Dir
    parse_path(args.dir, os.path.join(args.dir, F'ParseResult_Properties.csv'))


if __name__ == '__main__':
    main()
