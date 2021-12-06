import logging


# Script that converts xml in iso-8859-1 to xml in utf-8
def convert_xml_iso_8859_1_to_xml_utf_8(full_filename):
    # Checking if file is a .xml
    if not full_filename.endswith('.xml'):
        logging.warning('\tconvert_xml_iso_8859_1_to_xml_utf_8: Not a xml file.')
        logging.warning(f'\tFILENAME:{full_filename}')
        return

    # If it is a .xml we will try to convert it
    try:
        # Getting the file data withe the iso-8859-1 encoding
        file = open(full_filename, 'r', encoding='iso-8859-1')
        file_data = file.read()

        # Rewriting the file with the utf-8 encoding
        destination_file = open(full_filename, 'w', encoding='utf-8')
        destination_file.write(file_data)
        destination_file.close()

    except:
        logging.warning('\tconvert_xml_iso_8859_1_to_xml_utf_8: problem.')
        logging.warning(f'\tFILENAME:{full_filename}')
