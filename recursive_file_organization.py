import os

from file_organization_types import organize_by_type, organize_by_date

def get_files_count(directory):
    filesCount = 0

    for item in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, item)):
            filesCount += 1
        
    return filesCount

def organize_files_recursively(directory, logger, dry_run, move_records, sort_method, include_subdirs, progress_bar = None, root = None):    
    for item in os.listdir(directory):
        path = os.path.join(directory, item)

        if os.path.isfile(path):
            if sort_method == 'type':
                organize_by_type(directory, logger, dry_run, move_records, progress_bar, root)
            elif sort_method == 'date':
                organize_by_date(directory, logger, dry_run, move_records, progress_bar, root)
        elif os.path.isdir(path) and include_subdirs:
            organize_files_recursively(path, logger, dry_run, move_records, sort_method, include_subdirs)