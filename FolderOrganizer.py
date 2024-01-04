import os
import shutil
import logging
import argparse
import time
import tkinter as tk
import ttkbootstrap as ttk

from tkinter import filedialog, messagebox

def create_logger():
    logging.basicConfig(filename='file_organizer.log', level=logging.INFO, format='%(asctime)s: %(message)s')
    return logging.getLogger()

def move_file(file_path, target_directory, logger, dry_run=False, move_records=None):
    if dry_run:
        logger.info(f"[DRY RUN] Would move file {file_path} to {target_directory}")
    else:
        try:
            shutil.move(file_path, target_directory)
            logger.info(f"Move file {file_path} to {target_directory}")
            if move_records is not None:
                move_records.append((target_directory, file_path))  #Recorde file move for undo feature
        except Exception as e:
            logger.error(f"Error moveing file {file_path} to {target_directory}: {e}")

def undo_last_operation(move_records, logger):
    for target_directory, original_path in reversed(move_records):
        try:
            shutil.move(os.path.join(target_directory, os.path.basename(original_path)), original_path)
            logger.info(f"Reversed move: {original_path} back to {target_directory}")
        except Exception as e:
            logger.error(f"Error reversing file move from {target_directory} to {original_path}: {e}")

def organize_files_recursively(directory, logger, dry_run, move_records, sort_method):
    for item in os.listdir(directory):
        path = os.path.join(directory, item)
        if os.path.isfile(path):
            if sort_method == 'type':
                organize_by_type(directory, logger, dry_run, move_records)
            elif sort_method == 'date':
                organize_by_date(directory, logger, dry_run, move_records)
        elif os.path.isdir(path):
            organize_files_recursively(path, logger, dry_run, move_records, sort_method)

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

def run_terminal_mode(args):
    logger = create_logger()

    move_records = []

    organize_files_recursively(args.directory, logger, args.dry_run, move_records, args.sort)

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

    #Dry run option
    dry_run_choice = input("Do you want to perform a dry run? (y/n): ")
    dry_run = True if dry_run_choice.lower() == 'y' else False

    #Confirm before execution
    print(f"\nYou have chosen to organize files in: {directory_path}")
    sort_method = 'type' if sorting_method_choice == '1' else 'date'
    print(f"Sorting method: {'File Type' if sort_method == 'type' else 'Creation Date'}")
    print(f"Dry run: {'Enabled' if dry_run else 'Disabled'}")

    confirm = input("Procede with file organization? (y/n): ")

    move_records = []

    if confirm.lower() == 'y':
        logger = create_logger()
        organize_files_recursively(directory_path, logger, dry_run, move_records, sort_method)
        print("File organization completed with CLI mode!")
    else:
        print("File organization canceled.")

    if move_records and input("Do you want to undo the last operation? (y/n): ").lower() == 'y':
        undo_last_operation(move_records, logger)
        print("Last operation has been undone.")

def organize_files_gui(chosen_type, progress_bar, root):
    try:
        directory = filedialog.askdirectory()

        if directory:
            logger = create_logger()
            move_records = []

            if chosen_type.get() == 1:
                sort_method = 'type'
            elif chosen_type.get() == 2:
                sort_method = 'date'
            
            organize_files_recursively(directory, logger, False, move_records, sort_method)
            
            progress_bar['value'] = 50
            root.update_idletasks()
            messagebox.showinfo("Success", f"Files have been organized by {sort_method}!")
            progress_bar['value'] = 0
    except Exception as e:
        messagebox.showerror("Error", str(e))

def create_gui():
    root = ttk.Window(themename = 'darkly')
    root.title("File Organizer")
    
    chosen_type = tk.IntVar(value=1)
    
    choose_organize_by_type = tk.Radiobutton(root, text = "Organize files by type", variable=chosen_type, value=1)
    choose_organize_by_type.pack(pady=10)

    choose_organize_by_date = tk.Radiobutton(root, text = "Organize files by date", variable=chosen_type, value=2)
    choose_organize_by_date.pack(pady=10)

    progress_bar = ttk.Progressbar(root, orient=tk.HORIZONTAL, length=300, mode='determinate')
    progress_bar.pack(pady=10)
    
    organize_button = tk.Button(root, text="Organize Files", command=lambda: organize_files_gui(chosen_type, progress_bar, root))
    organize_button.pack(pady=20)

    root.mainloop()

create_gui()

# def main():
#     parser = argparse.ArgumentParser(description='Organize files in a directory.')
#     parser.add_argument('directory', nargs='?', help='Directory to organize')
#     parser.add_argument('--sort', choices=['type', 'date'], default='type', help='Sort by file type or creation date')
#     parser.add_argument('--dry_run', action='store_true', help='Simulate file organization without making changes')

#     args = parser.parse_args()

#     #Determine if runing in CLI mode or in Terminal mode
#     if args.directory:
#         run_terminal_mode(args)
#     else:
#         run_cli_mode()

# if __name__ == "__main__":
#     main()