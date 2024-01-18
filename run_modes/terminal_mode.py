from logger import create_logger                                    #Imported from logger.py file
from file_operations import undo_last_operation                     #Imported from file_operations.py file
from recursive_file_organization import organize_files_recursively  #Imported from recursive_file_organization.py

def run_terminal_mode(args):
    logger = create_logger()

    move_records = []

    organize_files_recursively(args.directory, logger, args.dry_run, move_records, args.sort, args.include_subdirs)

    print("File organization completed with Terminal mode!")

    if move_records and input("Do you want to undo the last operation? (y/n): ").lower() == 'y':
        undo_last_operation(move_records, logger)
        print("Last operation has been undone.")