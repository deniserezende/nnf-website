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

# Creating a not well-formed folder path to store not well formed files
folder_path_not_well_formed = os.path.join(folder_path, "NotWellFormed-Fixed")
os.mkdir(folder_path_not_well_formed)

amount_of_not_xml_files = 0
for filename in folder_files:
    full_filename = filename

    # Checking if file is a .xml
    if not filename.endswith('.xml'):
        amount_of_not_xml_files += 1
        logging.warning('Not a xml file.')
        logging.warning(f'\tFILENAME:{full_filename}')
        continue

    # Read in the file
    try:
        file = open(full_filename, 'r', encoding='iso-8859-1')
        filedata = file.read()

        # Copying the file to another one
        filename_stripped = os.path.basename(full_filename)
        destination_path = os.path.join(folder_path_not_well_formed, filename_stripped)

        # Write the file out again
        destination_file = open(destination_path, 'w', encoding='utf-8')
        destination_file.write(filedata)
        destination_file.close()

    except:
        logging.warning('Problem.')
        logging.warning(f'\tFILENAME:{full_filename}')

end = datetime.datetime.now()

amount_of_xml_files = len(folder_files)
logging.warning(f'\tAmount of xml files: {amount_of_xml_files}')

print(f'\n\nTempo de execução:\t{str(end - start)}')

       