#!/usr/bin/env python3

import logging

import property_parser
import property_definitions_nsw as nsw_def

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


class NswOldProperty(property_parser.Property):
    """Nsw Old Style format Property File."""

    def parse(self) -> bool:
        """Parse the property line."""

        fields = property_parser.split_str(self.line, ';')

        district = nsw_def.get_district_from_code(fields[1])
        self[property_parser.PropertyData.DISTRICT_CODE] = district

        self[property_parser.PropertyData.PROPERTY_ID] = fields[4]
        self[property_parser.PropertyData.UNIT_NUMBER] = fields[5]
        self[property_parser.PropertyData.HOUSE_NUMBER] = fields[6]
        self[property_parser.PropertyData.STREET_NAME] = fields[7]
        self[property_parser.PropertyData.SUBBURB] = fields[8]
        self[property_parser.PropertyData.POST_CODE] = fields[9]

        to_date = property_parser.convert_date_to_internal(
            fields[10], '%d/%M/%Y')
        self[property_parser.PropertyData.CONTRACT_DATE] = to_date

        self[property_parser.PropertyData.PURCHASE_PRICE] = fields[11]
        self[property_parser.PropertyData.LAND_DESCRIPTIONS] = fields[12]
        self[property_parser.PropertyData.AREA] = fields[13]
        self[property_parser.PropertyData.AREA_TYPE] = fields[14]
        self[property_parser.PropertyData.DIMENSIONS] = fields[15]

        zone_code = fields[16]
        self[property_parser.PropertyData.ZONE_CODE] = fields[16]
        self[property_parser.PropertyData.ZONE] =\
            nsw_def.get_zone_from_old_code(zone_code)

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


class NswNewProperty(property_parser.Property):
    """Nsw New Style format Property File."""

    def parse(self) -> bool:
        """Parse the property line."""

        fields = property_parser.split_str(self.line, ';')

        district = nsw_def.get_district_from_code(fields[1])
        self[property_parser.PropertyData.DISTRICT_CODE] = district
        self[property_parser.PropertyData.PROPERTY_ID] = fields[2]
        self[property_parser.PropertyData.UNIT_NUMBER] = fields[6]
        self[property_parser.PropertyData.HOUSE_NUMBER] = fields[7]
        self[property_parser.PropertyData.STREET_NAME] = fields[8]
        self[property_parser.PropertyData.SUBBURB] = fields[9]
        self[property_parser.PropertyData.POST_CODE] = fields[10]
        self[property_parser.PropertyData.AREA] = fields[11]
        self[property_parser.PropertyData.AREA_TYPE] = fields[12]

        to_date = property_parser.convert_date_to_internal(
            fields[13], '%Y%M%d')
        self[property_parser.PropertyData.CONTRACT_DATE] = to_date

        to_date = property_parser.convert_date_to_internal(
            fields[14], '%Y%M%d')
        self[property_parser.PropertyData.SETTLEMENT_DATE] = to_date

        self[property_parser.PropertyData.PURCHASE_PRICE] = fields[15]

        zone_code = fields[16]
        self[property_parser.PropertyData.ZONE_CODE] = zone_code
        self[property_parser.PropertyData.ZONE] =\
            nsw_def.get_zone_from_new_code(zone_code)
        self[property_parser.PropertyData.ZONE_TYPE] =\
            nsw_def.get_type_from_new_zone_code(zone_code)

        self[property_parser.PropertyData.NATURE_OF_PROPERTY] = fields[17]
        self[property_parser.PropertyData.PRIMARY_PURPOSE] = fields[18]
        self[property_parser.PropertyData.LOT_NUMBER] = fields[19]

        return True


class NswNewPropertyFile(property_parser.PropertyFile):
    """Nsw New Style format Property File."""

    def create_property_from_line(self, line: str) -> NswNewProperty:
        """Create a property object for this class."""
        return NswNewProperty(line)

    @staticmethod
    def name_allowed(file_name_candidate: str) -> bool:
        """Check if the given name is allowed."""
        return ('_SALES_DATA_NNME_' in file_name_candidate.upper() and
                file_name_candidate.upper().endswith('.DAT'))

    def line_of_interest(self, line):
        """Check if File line is of interest."""
        return line.upper().startswith('B')


def test_old_property():
    """Test Old Property Format."""
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


def test_new_property():
    """Test New Property Format."""
    file_path = R'#TestFiles\090_SALES_DATA_NNME_04022019.DAT'

    logger.info('Creating Test Property File')
    prop_file = NswNewPropertyFile(file_path)
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


def test():
    """Test function for this module."""
    import project_logger
    project_logger.setup_logger(R'#TestFiles\logfile.txt')

    test_new_property()


if __name__ == '__main__':
    test()
