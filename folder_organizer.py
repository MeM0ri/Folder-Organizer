import os
import argparse
import time
import tkinter as tk
import ttkbootstrap as ttk

from logger import create_logger                                    #Imported from logger.py file
from file_operations import move_file, undo_last_operation          #Imported from file_operations.py file
from recursive_file_organization import organize_files_recursively  #Imported from recursive_file_organization.py
from gui_folder_organization import create_gui                      #Imported from gui_folder_organization.py
from tkinter import filedialog, messagebox

def run_terminal_mode(args):
    logger = create_logger()

    move_records = []

    organize_files_recursively(args.directory, logger, args.dry_run, move_records, args.sort, args.include_subdirs)

    print("File organization completed with Terminal mode!")

    if move_records and input("Do you want to undo the last operation? (y/n): ").lower() == 'y':
        undo_last_operation(move_records, logger)
        print("Last operation has been undone.")
            
def run_cli_mode():
    print("I'll help you to organize your directory.")

    #Path for directory
    print("Enter the path for the directory. Example: C:\Documents\Folder to organize")
    directory_path = input("The path for the directory to organize: ")

    #Choose sorting method
    print("Choose sorting method:")
    print("1: Sort by file type")
    print("2: Sort by creation date")
    sorting_method_choice = input("Enter your choice (1 or 2): ")

    #Include subdirs option
    include_subdirs_choice = input("Do you want to include subdirectories for a file organizer run? (y/n): ")
    include_subdirs = True if include_subdirs_choice.lower() == 'y' else False

    #Dry run option
    dry_run_choice = input("Do you want to perform a dry run? (y/n): ")
    dry_run = True if dry_run_choice.lower() == 'y' else False

    #Confirm before execution
    print(f"\nYou have chosen to organize files in: {directory_path}")
    sort_method = 'type' if sorting_method_choice == '1' else 'date'
    print(f"Sorting method: {'File Type' if sort_method == 'type' else 'Creation Date'}")
    print(f"Organize files in subdirs: {'Enabled' if include_subdirs else 'Disabled'}")
    print(f"Dry run: {'Enabled' if dry_run else 'Disabled'}")

    confirm = input("Procede with file organization? (y/n): ")

    move_records = []

    if confirm.lower() == 'y':
        logger = create_logger()
        organize_files_recursively(directory_path, logger, dry_run, move_records, sort_method, include_subdirs)
        print("File organization completed with CLI mode!")
    else:
        print("File organization canceled.")

    if move_records and input("Do you want to undo the last operation? (y/n): ").lower() == 'y':
        undo_last_operation(move_records, logger)
        print("Last operation has been undone.")

def main():
    parser = argparse.ArgumentParser(description = 'Organize files in a directory.')
    parser.add_argument('--run_mode', choices = ['gui', 'cli', 'terminal'], default = 'gui')
    parser.add_argument('directory', nargs = '?', help = 'Directory to organize')
    parser.add_argument('--sort', choices = ['type', 'date'], default = 'type', help = 'Sort by file type or creation date')
    parser.add_argument('--dry_run', action = 'store_true', help = 'Simulate file organization without making changes')
    parser.add_argument('--include_subdirs', action = 'store_true', help = 'Include subdirs to file organizer run')

    args = parser.parse_args()

    #Determine if runing in CLI mode or in Terminal mode
    if args.run_mode == 'terminal' and args.directory:
        run_terminal_mode(args)
    elif args.run_mode == 'cli':
        run_cli_mode()
    elif args.run_mode == 'gui':
        create_gui()

if __name__ == "__main__":
    main()