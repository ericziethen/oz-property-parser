#!/usr/bin/env python3

import logging

import property_parser

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


class NswOldProperty(property_parser.Property):
    """Nsw Old Style format Property File."""

    def parse(self) -> bool:
        """Parse the property line."""

        fields = property_parser.split_str(self.line, ';')

        self[property_parser.PropertyData.DISTRICT_CODE] = fields[1]  # TODO - ENUM
        self[property_parser.PropertyData.PROPERTY_ID] = fields[4]
        self[property_parser.PropertyData.UNIT_NUMBER] = fields[5]
        self[property_parser.PropertyData.HOUSE_NUMBER] = fields[6]
        self[property_parser.PropertyData.STREET_NAME] = fields[7]
        self[property_parser.PropertyData.SUBBURB] = fields[8]
        self[property_parser.PropertyData.POST_CODE] = fields[9]

        to_date = property_parser.convert_date_to_internal(
            fields[10], '%d/%M/%Y')
        self[property_parser.PropertyData.CONTRACT_DATE] = fields[10]

        self[property_parser.PropertyData.PURCHASE_PRICE] = fields[11]
        self[property_parser.PropertyData.LAND_DESCRIPTIONS] = fields[12]
        self[property_parser.PropertyData.AREA] = fields[13]
        self[property_parser.PropertyData.AREA_TYPE] = fields[14]
        self[property_parser.PropertyData.DIMENSIONS] = fields[15]
        self[property_parser.PropertyData.ZONE_CODE] = fields[16]  # TODO - ENUM

        return True

class NswOldPropertyFile(property_parser.PropertyFile):
    """Nsw Old Style format Property File."""

    def create_property_from_line(self, line: str) -> NswOldProperty:
        """Create a property object for this class."""
        return NswOldProperty(line)

    @staticmethod
    def name_allowed(file_name_candidate: str) -> bool:
        """Check if the given name is allowed."""
        return (file_name_candidate.upper().startswith('ARCHIVE_SALES_') and
                file_name_candidate.upper().endswith('.DAT'))

    def line_of_interest(self, line):
        """Check if File line is of interest."""
        return line.upper().startswith('B')


def test():
    """Test function for this module."""
    import project_logger
    project_logger.setup_logger(R'#TestFiles\logfile.txt')
    file_path = R'#TestFiles\ARCHIVE_SALES_1990.DAT'

    logger.info('Creating Test Property File')
    prop_file = NswOldPropertyFile(file_path)
    logger.info('Start Parsing')
    prop_file.parse()
    logger.info('Finish Parsing')

    for prop in prop_file:
        #logger.debug(F'{prop}')
        # logger.debug(F'{prop}')

        '''
        prop_line = F'{prop[property_parser.PropertyData.UNIT_NUMBER]}@@@\
            {prop[property_parser.PropertyData.HOUSE_NUMBER]}@@@\
            {prop[property_parser.PropertyData.STREET_NAME]}@@@\
            {prop[property_parser.PropertyData.SUBBURB]}@@@\
            {prop[property_parser.PropertyData.POST_CODE]}@@@'

        '''
        
        prop_line =\
            prop[property_parser.PropertyData.PROPERTY_ID] + ',' +\
            prop[property_parser.PropertyData.UNIT_NUMBER] + ',' +\
            prop[property_parser.PropertyData.HOUSE_NUMBER] + ',' +\
            prop[property_parser.PropertyData.STREET_NAME] + ',' +\
            prop[property_parser.PropertyData.SUBBURB] + ',' +\
            prop[property_parser.PropertyData.POST_CODE]
        print(prop_line)


if __name__ == '__main__':
    test()
