import os
import file_counter

from file_organization_types import organize_by_type, organize_by_date

def organize_files_recursively(directory, logger, dry_run, move_records, sort_method, include_subdirs, progress_bar = None, root = None):    
    for item in os.listdir(directory):
        path = os.path.join(directory, item)

        if os.path.isfile(path):
            file_counter.curentFileNum += 1     #Update this variable for correct progress bar work
            
            if sort_method == 'type':
                organize_by_type(path, directory, logger, dry_run, move_records, progress_bar, root)
            elif sort_method == 'date':
                organize_by_date(path, directory, logger, dry_run, move_records, progress_bar, root)
        elif os.path.isdir(path) and include_subdirs:
            organize_files_recursively(path, logger, dry_run, move_records, sort_method, include_subdirs)