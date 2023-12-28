import os
import shutil
import logging

def create_logger():
    logging.basicConfig(filename='file_organizer.log', level=logging.INFO, format='%(asctime)s: %(message)s')
    return logging.getLogger()

def move_file(file_path, target_directory):
    try:
        shutil.move(file_path, target_directory)
        logger.info(f"Move file {file_path} to {target_directory}")
    except Exception as e:
        logger.error(f"Error moveing file {file_path} to {target_directory}: {e}")

def organize_files(directory, logger):
    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)):
            file_type = filename.split('.')[-1]
            target_directory = os.path.join(directory, file_type)

            if not os.path.exists(target_directory):
                os.makedirs(target_directory)

            file_path = os.path.join(directory, filename)
            move_file(file_path, target_directory)

def list_files(directory):
    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)):
            print(filename)

logger = create_logger()
directory_path = "F:\Folder For Python Practice"
list_files(directory_path)
organize_files(directory_path, logger)