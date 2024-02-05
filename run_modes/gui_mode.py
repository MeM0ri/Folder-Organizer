import os
import file_counter
import tkinter as tk

from logger import create_logger
from tkinter import messagebox
from file_operations import undo_last_operation
from recursive_file_organization import organize_files_recursively

# global filesCount
# filesCount = 0

# global curentFileNum
# curentFileNum = 0

# def get_files_count(directory, include_subdirs):
#     for item in os.listdir(directory):
#         if os.path.isfile(os.path.join(directory, item)):
#             filesCount += 1
#             print(filesCount)
#         elif os.path.isdir(item) and include_subdirs:
#             get_files_count(directory)

def run_gui_mode(chosen_type, progress_bar, undo_button, root, directory_entry, text_widget, include_subdirs_var, dry_run_var):
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
            
            file_counter.get_files_count(directory, include_subdirs)
            
            organize_files_recursively(directory, logger, dry_run, move_records, sort_method, include_subdirs, progress_bar, root)
            
            messagebox.showinfo("Success", f"Files have been organized by {sort_method}!")
            progress_bar['value'] = 0

            if dry_run_var.get() == 0 and text_widget.get("1.0", tk.END).strip():
                undo_button['state'] = 'normal'
                undo_button['command'] = lambda: undo_last_operation(move_records, logger, undo_button)
    except Exception as e:
        messagebox.showerror("Error", str(e))