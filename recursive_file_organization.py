import os

from file_organization_types import organize_by_type, organize_by_date

def organize_files_recursively(directory, logger, dry_run, move_records, sort_method, include_subdirs):
    for item in os.listdir(directory):
        path = os.path.join(directory, item)
        if os.path.isfile(path):
            if sort_method == 'type':
                organize_by_type(directory, logger, dry_run, move_records)
            elif sort_method == 'date':
                organize_by_date(directory, logger, dry_run, move_records)
        elif os.path.isdir(path) and include_subdirs:
            organize_files_recursively(path, logger, dry_run, move_records, sort_method, include_subdirs)