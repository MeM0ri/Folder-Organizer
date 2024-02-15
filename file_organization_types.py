import os
import time
import file_counter

from file_operations import move_file

def organize_by_type(filename, directory, logger, dry_run, move_records, progress_bar = None, root = None, log_table = None):
    if os.path.isfile(os.path.join(directory, filename)):
        file_type = filename.split('.')[-1]
        target_directory = os.path.join(directory, file_type)

        if not os.path.exists(target_directory):
            os.makedirs(target_directory)

        file_path = os.path.join(directory, filename)

        if log_table is not None:
            move_file(file_path, target_directory, logger, dry_run, move_records, log_table)
        else:
            move_file(file_path, target_directory, logger, dry_run, move_records)

        if progress_bar is not None and root is not None:
            progress_bar['value'] = file_counter.curentFileNum * 100 / file_counter.filesCount
            root.update_idletasks()

def organize_by_date(filename, directory, logger, dry_run, move_records, progress_bar = None, root = None, log_table = None):
    
    if os.path.isfile(os.path.join(directory, filename)):
        file_creation_time = os.path.getctime(os.path.join(directory, filename))
        date_folder = time.strftime('%Y-%m-%d', time.localtime(file_creation_time))
        target_directory = os.path.join(directory, date_folder)

        if not os.path.exists(target_directory):
            os.makedirs(target_directory)

        file_path = os.path.join(directory, filename)

        if log_table is not None:
            move_file(file_path, target_directory, logger, dry_run, move_records, log_table)
        else:
            move_file(file_path, target_directory, logger, dry_run, move_records)

        if progress_bar is not None and root is not None:
            progress_bar['value'] = file_counter.curentFileNum * 100 / file_counter.filesCount
            root.update_idletasks()