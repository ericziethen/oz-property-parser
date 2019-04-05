#!/usr/env/bin python3

"""Main program to run the property data extractor."""

import argparse
import csv
import logging
import os
import sys


from typing import List, Optional

import property_file_manager
import property_parser
import project_logger

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


def parse_args() -> argparse.Namespace:
    """Set up command line arguments for Transdump."""
    parser = argparse.ArgumentParser()
    parser.add_argument('searchDir',
                        help='Base search Dir for property Files')
    return parser.parse_args()


def validate_args(args: argparse.Namespace) -> None:
    """Validate the command line arguments."""
    if (not os.path.isdir(args.searchDir)) or (not os.path.exists(args.searchDir)):
        raise ValueError(F'"{args.searchDir}" is not a vaid directory')


def get_csv_keys() -> List[str]:
    """Create a list of csv keys."""
    key_list = []
    ignore_keys = [
    ]

    for field in property_parser.PropertyData:
        if field not in ignore_keys:
            key_list.append(field.value)

    logger.debug(F'Created Key List: {key_list}')

    return key_list


def write_property_to_csv(csv_path: str, property_file: property_parser.PropertyFile) -> None:
    """Write the parsed log file to a csv file."""
    write_header = not os.path.exists(csv_path)

    # Get the data to write (List of Dics to write)
    csv_data = property_file.get_lines_as_list()
    #logger.debug(F'CSV_DATA: {csv_data}')

    logger.info(F'Writing/Appending to: "{csv_path}"')
    with open(csv_path, 'a', encoding='utf-8') as csv_file:
        dict_writer = csv.DictWriter(csv_file, delimiter=',',
                                     lineterminator='\n',
                                     extrasaction='ignore',
                                     fieldnames=get_csv_keys())
        if write_header:
            logger.info(F'Writing Header Row')
            dict_writer.writeheader()
        logger.info(F'Writing {len(csv_data)} entries')
        dict_writer.writerows(csv_data)


def parse_path(path: str):
    """Parse the path for Property files."""
    logger.info(F'Parse Property files in "{path}"')

    for root, _, files in os.walk(path):
        for filename in files:
            file_path = os.path.join(root, filename)
            logger.info(F'Checking file "{file_path}"')
            property_file = property_file_manager.get_nsw_property_file_from_path(file_path)

            if property_file is not None:
                logger.info('Parse Log File')
                property_file.parse()

                '''
                property_name = property_file.__class__.__name__
                csv_path = os.path.join(
                    path, F'ParseResult_{property_name}.csv')
                '''
                csv_path = os.path.join(
                    path, F'ParseResult_Properties.csv')
                
                write_property_to_csv(csv_path, property_file)
                logger.info('Parsing complete')
            else:
                logger.info("Don't parse, cannot identify as valid Property file.")


def main():
    """Run the log parser."""

    # Parse command line arguments
    args = parse_args()
    validate_args(args)

    # Setup the logger
    project_logger.setup_logger(
        os.path.join(args.searchDir, R'property_parser.log'))

    logger.info(F'Command Line Arguments: "{args}"')

    # Process Log Dir
    parse_path(args.searchDir)

if __name__ == '__main__':
    main()
