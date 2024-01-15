import os
import shutil
import logging
import argparse
import time
import tkinter as tk
import ttkbootstrap as ttk

from tkinter import filedialog, messagebox
from text_handler import TextHandler

def create_logger(text_widget):
    #Create logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    #File handler for writing to log file
    file_handler = logging.FileHandler('file_organizer.log', encoding = 'utf-8')
    file_formatter = logging.Formatter('%(asctime)s: %(message)s')
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)    

    #Text widget handler for updating the GUI
    text_handler = TextHandler(text_widget)
    text_formatter = logging.Formatter('%(asctime)s: %(message)s')
    text_handler.setFormatter(text_formatter)
    logger.addHandler(text_handler)
    
    return logger

def move_file(file_path, target_directory, logger, dry_run = False, move_records = None):
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

def select_directory(directory_entry):
    try:
        directory = filedialog.askdirectory()
        if directory:
            directory_entry.delete(0, tk.END)
            directory_entry.insert(0, directory)
    except Exception as e:
        messagebox.showerror("Error", str(e))

def organize_files_gui(chosen_type, progress_bar, root, directory_entry, text_widget, include_subdirs_var, dry_run_var):
    try:
        directory = directory_entry.get()

        if directory:
            logger = create_logger(text_widget)
            move_records = []

            if chosen_type.get() == 1:
                sort_method = 'type'
            elif chosen_type.get() == 2:
                sort_method = 'date'

            dry_run = dry_run_var.get()
            include_subdirs = include_subdirs_var.get()
            
            organize_files_recursively(directory, logger, dry_run, move_records, sort_method, include_subdirs)
            
            progress_bar['value'] = 50
            root.update_idletasks()
            messagebox.showinfo("Success", f"Files have been organized by {sort_method}!")
            progress_bar['value'] = 0
    except Exception as e:
        messagebox.showerror("Error", str(e))

def create_gui():
    root = ttk.Window(themename = 'darkly')
    root.title("File Organizer")
    
    all_options_frame = ttk.Frame(root)
    all_options_frame.pack(side = tk.TOP, fill = "both", expand = True, padx = 5, pady = 5)

    #Choose type var and radiobuttons
    sorting_type_frame = ttk.LabelFrame(all_options_frame, text = "Sorting Options")
    sorting_type_frame.pack(side = tk.LEFT, fill = "both", expand = True, padx = 5, pady = 5, ipadx = 3, ipady = 3)

    chosen_type = tk.IntVar(value = 1)
    
    choose_organize_by_type = tk.Radiobutton(sorting_type_frame, text = "Organize files by type", variable = chosen_type, value = 1)
    choose_organize_by_type.pack(pady = 3)

    choose_organize_by_date = tk.Radiobutton(sorting_type_frame, text = "Organize files by date", variable = chosen_type, value = 2)
    choose_organize_by_date.pack(pady = 3)

    #Checkbox for recursive organization
    settings_frame = ttk.LabelFrame(all_options_frame, text = "Settings")
    settings_frame.pack(side = tk.LEFT, fill = "both", expand = True, padx = 5, pady = 5, ipadx = 3, ipady = 3)

    include_subdirs_var = tk.BooleanVar()
    include_subdirs_check = tk.Checkbutton(settings_frame, text = "Include Subdirectories", variable = include_subdirs_var)
    include_subdirs_check.pack(pady = 3)

    #Checkbox for dry run
    dry_run_var = tk.BooleanVar()
    dry_run_check = tk.Checkbutton(settings_frame, text = "Dry Run", variable = dry_run_var)
    dry_run_check.pack(pady = 3)

    #Var for directory path and button for search folder through browser
    directory_path_frame = ttk.LabelFrame(root, text = "Directory Selection")
    directory_path_frame.pack(side = tk.TOP, fill = "both", expand = True, padx = 5, pady = 5)

    centered_frame = ttk.Frame(directory_path_frame)
    centered_frame.pack(side = tk.TOP, expand = True, padx = 5, pady = 5)

    directory_entry = tk.Entry(centered_frame, width = 50)
    directory_entry.pack(side = tk.LEFT, pady = 3, padx = (5, 0))

    browse_button = tk.Button(centered_frame, text = "Browse", command = lambda: select_directory(directory_entry))
    browse_button.pack(side = tk.LEFT, pady = 3, padx = (0, 5))

    #Log text var
    log_frame = ttk.LabelFrame(root, text = "File Organizer Logs")
    log_frame.pack(side = tk.TOP, fill = "both", expand = True, padx = 5, pady = 5)

    log_text = tk.Text(log_frame, height = 5, state = 'disabled')
    log_text.pack(padx = 5, pady = 5)

    #Progress bar var
    progress_bar = ttk.Progressbar(root, orient = tk.HORIZONTAL, length = 300, mode = 'determinate')
    progress_bar.pack(side = tk.TOP, pady = 10)
    
    #Button for running organize script
    organize_button = tk.Button(root, text = "Organize Files", command = lambda: organize_files_gui(chosen_type, progress_bar, root, directory_entry, log_text, include_subdirs_var, dry_run_var))
    organize_button.pack(side = tk.TOP, pady = 20)

    root.mainloop()

create_gui()

# def main():
#     parser = argparse.ArgumentParser(description = 'Organize files in a directory.')
#     parser.add_argument('directory', nargs = '?', help = 'Directory to organize')
#     parser.add_argument('--sort', choices = ['type', 'date'], default = 'type', help = 'Sort by file type or creation date')
#     parser.add_argument('--dry_run', action = 'store_true', help = 'Simulate file organization without making changes')
#     parser.add_argument('--include_subdirs', action = 'store_true', help = 'Include subdirs to file organizer run')

#     args = parser.parse_args()

#     #Determine if runing in CLI mode or in Terminal mode
#     if args.directory:
#         run_terminal_mode(args)
#     else:
#         run_cli_mode()

# if __name__ == "__main__":
#     main()