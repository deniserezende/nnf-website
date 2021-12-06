import xml.etree.ElementTree as ET
import logging


def parse_xml_file(full_filename, tree):
    # Trying to parse the file
    try:
        tree = ET.parse(full_filename)
        return tree
    # If failed to parse the file
    except NameError:
        # Report
        logging.warning('\tparse_xml_file: xml file not well-formed.')
        logging.warning(f'\tFILENAME:{full_filename}')
        return None


def get_nnf_id(tree):
    # Getting the root of the tree of the xml file
    root = tree.getroot()

    # Getting the xml http used to scale down the tree
    xml_http = root.tag[:-len('nfeProc')]

    # Scaling down the tree NFe - infNFe - ide - nNF
    NFe = root.find(xml_http + 'NFe')
    if NFe is None:
        logging.warning('\tget_nnf_id: NFe not found.')
        return None

    infNFe = NFe.find(xml_http + 'infNFe')
    if infNFe is None:
        logging.warning('\tget_nnf_id: infNFe not found.')
        return None

    ide = infNFe.find(xml_http + 'ide')
    if ide is None:
        logging.warning('\tget_nnf_id: ide not found.')
        return None

    nNF = ide.find(xml_http + 'nNF')
    if nNF is None:
        logging.warning('\tget_nnf_id: nNF not found.')
        return None
    else:
        # Found nNF id
        nNF_id = int(nNF.text, 10)
        return nNF_id


def get_missing_nnf_ids_based_on_a_single_series(nNF_numbers_list):
    missing_nNF_numbers_list = []
    nNF_numbers_list.sort()
    # Generating a list of missing nNF ids based on a single series
    # Numbers missing between the smallest and the largest are added
    # to the missing nNF list
    for count, current_nNF_number in enumerate(nNF_numbers_list[1:], start=1):
        if current_nNF_number - nNF_numbers_list[count - 1] > 1:
            for missing_nNF in range(nNF_numbers_list[count - 1] + 1, current_nNF_number):
                missing_nNF_numbers_list.append(missing_nNF)
    return missing_nNF_numbers_list