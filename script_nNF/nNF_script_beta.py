import sys
import os
import datetime
import logging
import zipfile
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
    # os.chdir(folder_path)
    # HERE: Added this last because the unzip was creating two folders with the same name
    #files_folder_path = os.path.join(folder_path, os.path.basename(os.path.normpath(folder_path)))

    # Quick fix
    files_folder_path = folder_path
    
    os.chdir(files_folder_path)
    logging.info(f"Current Path = [{os.getcwd()}]")
else:
    logging.error('\tFolder path does not exist.')
    logging.error(f'\tPath={folder_path}')
    sys.exit()

folder_files = []
for (dir_path, dir_names, filenames) in os.walk(files_folder_path):
    folder_files.extend(filenames)
    break

amount_of_not_xml_files = 0
nNF_numbers_list = []
for file in folder_files:
    # Checking if file is a .xml
    if not file.endswith('.xml'):
        amount_of_not_xml_files += 1
        continue

    full_filename = os.path.join(files_folder_path, file)

    tree = ET.parse(full_filename)
    root = tree.getroot()
    # Getting the xml http used to scale down the tree
    xml_http = root.tag[:-len('nfeProc')]

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

end = datetime.datetime.now()

amount_folder_files = len(folder_files)
amount_valid_xml = len(nNF_numbers_list)
amount_invalid_xml = amount_folder_files - amount_valid_xml - amount_of_not_xml_files
logging.warning(f'\tAmount of files: {amount_folder_files}')
logging.warning(f'\tAmount of not xml files: {amount_of_not_xml_files}')
logging.warning(f'\tAmount of xml files: {amount_invalid_xml + amount_valid_xml}')
logging.warning(f'\tAmount of valid xml files: {amount_valid_xml}')
logging.warning(f'\tAmount of invalid xml files: {amount_invalid_xml}')

print(f'\n\nTempo de execução:\t{str(end - start)}')
print(f'\n\nPrimeira nota fiscal: {smallest_nNF}')
print(f'Última nota fiscal: {largest_nNF}')
print(f'Notas fiscais faltantes: {missing_nNF_numbers_list}')
print(f'Quantidade de Notas fiscais faltantes: {len(missing_nNF_numbers_list)}\n\n')
