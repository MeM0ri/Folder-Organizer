import os
import time

from file_operations import move_file

def organize_by_type(directory, logger, dry_run, move_records):
    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)):
            file_type = filename.split('.')[-1]
            target_directory = os.path.join(directory, file_type)

            if not os.path.exists(target_directory):
                os.makedirs(target_directory)

            file_path = os.path.join(directory, filename)
            move_file(file_path, target_directory, logger, dry_run, move_records)

def organize_by_date(directory, logger, dry_run, move_records):
    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)):
            file_creation_time = os.path.getctime(os.path.join(directory, filename))
            date_folder = time.strftime('%Y-%m-%d', time.localtime(file_creation_time))
            target_directory = os.path.join(directory, date_folder)

            if not os.path.exists(target_directory):
                os.makedirs(target_directory)

            file_path = os.path.join(directory, filename)
            move_file(file_path, target_directory, logger, dry_run, move_records)