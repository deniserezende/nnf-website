import sys
import os
import datetime
import logging
import zipfile
import glob
import change_xml_encoding
import nNF_script_functions

start = datetime.datetime.now()

# Getting data from the commandline -p [zipfile path]
if __name__ == "__main__":
    for i, arg in enumerate(sys.argv):
        if arg == "-p":
            zip_path = sys.argv[i + 1]
            # Checking if the folder is a zip file
            if zip_path.endswith(".zip"):
                break
            else:
                logging.error('\tNot a zip file.')
                logging.error(f'\tZip path={zip_path}')
                sys.exit()

# Getting the zip file full path and removing the .zip
# to extract the files to that folder (folder_path)
folder_path = zip_path[:-4]
logging.info(f"Folder Path = [{folder_path}]")

# Extracting files from the zip file and putting it in folder_path
with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(folder_path)

if os.path.exists(folder_path):
    # Searching for file in directories recursively
    # and then creating a list of all the filenames that ends with .xml
    folder_files = glob.glob(folder_path + "/**/*.xml", recursive=True)
    logging.info(f"Folder path search = [{folder_files}]")

    # Going to the folder with all the xml files
    os.chdir(folder_path)
    logging.info(f"Current Path = [{os.getcwd()}]")
else:
    logging.error('\tFolder path does not exist.')
    logging.error(f'\tPath={folder_path}')
    sys.exit()

amount_of_not_xml_files = 0
amount_of_xml_files_not_well_formed_unfixed = 0
nNF_numbers_list = []
for file in folder_files:
    full_filename = file

    # Checking if file is a .xml
    if not file.endswith('.xml'):
        amount_of_not_xml_files += 1
        logging.warning('Not a xml file.')
        logging.warning(f'\tFILENAME:{full_filename}')
        continue

    # Trying to parse the file
    tree = nNF_script_functions.parse_xml_file(full_filename, tree)
    if tree is None:
        # Changing the file encoding from iso-8859-1 to utf-8
        change_xml_encoding.convert_xml_iso_8859_1_to_xml_utf_8(full_filename)
        # Calling the parser again
        tree = nNF_script_functions.parse_xml_file(full_filename, tree)

        if tree is None:
            # If tree still equals None than the file can't be fixed
            # converting iso-8859-1 to utf-8
            logging.error('Xml file not well-formed.')
            logging.error("Wasn't able to fix it.")
            logging.error(f'\tFILENAME:{full_filename}')
            amount_of_xml_files_not_well_formed_unfixed += 1
            continue

    # Trying to get the nNF id
    nNF_id = nNF_script_functions.get_nnf_id(tree)
    if nNF_id is not None:
        # Putting all nNF ids in a list
        nNF_numbers_list.append(nNF_id)
    else:
        logging.warning("\tCouldn't access the nNF.")
        logging.warning(f'\tFILENAME:{full_filename}')
        continue


missing_nNF_numbers_list = []
smallest_nNF = None
largest_nNF = None

# Checking if list is empty
if nNF_numbers_list:
    smallest_nNF = nNF_numbers_list[0]
    largest_nNF = nNF_numbers_list[-1]
    # Getting a list of missing nNF ids based on a single series
    missing_nNF_numbers_list = nNF_script_functions.get_missing_nnf_ids_based_on_a_single_series(nNF_numbers_list)

end = datetime.datetime.now()

amount_of_xml_files = len(folder_files)
amount_valid_xml = len(nNF_numbers_list)
amount_invalid_xml = amount_of_xml_files - amount_valid_xml
logging.warning(f'\tAmount of xml files: {amount_of_xml_files}')
logging.warning(f'\tAmount of valid xml files: {amount_valid_xml}')
logging.warning(f'\tAmount of invalid xml files: {amount_invalid_xml}')
logging.info(f'\tAmount of unfixed xml files that were not well-formed: {amount_of_xml_files_not_well_formed_unfixed}')

print(f'\n\nTempo de execução:\t{str(end - start)}')
print(f'\n\nPrimeira nota fiscal: {smallest_nNF}')
print(f'Última nota fiscal: {largest_nNF}')
print(f'Notas fiscais faltantes: {missing_nNF_numbers_list}')
print(f'Quantidade de Notas fiscais faltantes: {len(missing_nNF_numbers_list)}\n\n')


