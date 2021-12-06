import sys
import os
import datetime
import logging
import zipfile
import glob
import xml.etree.ElementTree as ET

start = datetime.datetime.now()

if __name__ == "__main__":
    for i, arg in enumerate(sys.argv):
        if arg == "-p":
            # folder_path = sys.argv[i + 1]
            # HERE: Added this last to unzip a file
            zip_path = sys.argv[i+1]
            if zip_path.endswith(".zip"):
                break
            else:
                print("Not a zip file.")
                logging.error('\tNot a zip file.')
                logging.error(f'\tZip path={zip_path}')
                sys.exit()

folder_path = zip_path[:-4]
logging.info(f"Folder Path = [{folder_path}]")

with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(folder_path)

if os.path.exists(folder_path):
    # HERE: Trying to searching for file in directories recursively
    # Creates a list of all the filenames that endwith .xml
    folder_files = glob.glob(folder_path + "/**/*.xml", recursive = True)
    logging.info(f"Folder path search = [{folder_files}]")

    os.chdir(folder_path)
    logging.info(f"Current Path = [{os.getcwd()}]")
else:
    logging.error('\tFolder path does not exist.')
    logging.error(f'\tPath={folder_path}')
    sys.exit()

amount_of_not_xml_files = 0
amount_of_xml_files_not_well_formed = 0
nNF_numbers_list = []
for file in folder_files:
    full_filename = file

    # Checking if file is a .xml
    if not file.endswith('.xml'):
        amount_of_not_xml_files += 1
        logging.warning('Not a xml file.')
        logging.warning(f'\tFILENAME:{full_filename}')
        continue

    try:
        tree = ET.parse(full_filename)
        root = tree.getroot()
        # Getting the xml http used to scale down the tree
        xml_http = root.tag[:-len('nfeProc')]
    except:
        logging.error('xml file not well-formed.')
        logging.warning(f'\tFILENAME:{full_filename}')
        amount_of_xml_files_not_well_formed += 1
        continue

    # Scaling down the tree NFe - infNFe - ide - nNF
    NFe = root.find(xml_http + 'NFe')
    if NFe is None:
        logging.warning('\tNFe not found.')
        logging.warning(f'\tFILENAME:{full_filename}')
        continue

    infNFe = NFe.find(xml_http + 'infNFe')
    if infNFe is None:
        logging.warning('infNFe not found.')
        logging.warning(f'\tFILENAME:{full_filename}')
        continue

    ide = infNFe.find(xml_http + 'ide')
    if ide is None:
        logging.warning('ide not found.')
        logging.warning(f'\tFILENAME:{full_filename}')
        continue

    nNF = ide.find(xml_http + 'nNF')
    if nNF is None:
        logging.warning('nNF not found.')
        logging.warning(f'\tFILENAME:{full_filename}')
        continue
    else:
        # Found nNF id
        nNF_id = int(nNF.text, 10)
        nNF_numbers_list.append(nNF_id)

missing_nNF_numbers_list = []
smallest_nNF = None
largest_nNF = None
# Checking if list is empty
if nNF_numbers_list:
    nNF_numbers_list.sort()
    smallest_nNF = nNF_numbers_list[0]
    largest_nNF = nNF_numbers_list[-1]
    for count, current_nNF_number in enumerate(nNF_numbers_list[1:], start=1):
        if current_nNF_number - nNF_numbers_list[count - 1] > 1:
            for missing_nNF in range(nNF_numbers_list[count - 1] + 1, current_nNF_number):
                missing_nNF_numbers_list.append(missing_nNF)

print(nNF_numbers_list)

end = datetime.datetime.now()

amount_of_xml_files = len(folder_files)
amount_valid_xml = len(nNF_numbers_list)
amount_invalid_xml = amount_of_xml_files - amount_valid_xml
logging.warning(f'\tAmount of xml files: {amount_of_xml_files}')
logging.warning(f'\tAmount of valid xml files: {amount_valid_xml}')
logging.warning(f'\tAmount of invalid xml files: {amount_invalid_xml}')
logging.warning(f'\tAmount of xml files not well-formed: {amount_of_xml_files_not_well_formed}')

print(f'\n\nTempo de execução:\t{str(end - start)}')
print(f'\n\nPrimeira nota fiscal: {smallest_nNF}')
print(f'Última nota fiscal: {largest_nNF}')
print(f'Notas fiscais faltantes: {missing_nNF_numbers_list}')
print(f'Quantidade de Notas fiscais faltantes: {len(missing_nNF_numbers_list)}\n\n')
