import file_counter
import tkinter as tk

from logger import create_logger
from tkinter import messagebox
from file_operations import undo_last_operation
from recursive_file_organization import organize_files_recursively

def run_gui_mode(chosen_type, progress_bar, undo_button, root, directory_entry, include_subdirs_var, dry_run_var, log_table):
    try:
        directory = directory_entry.get()

        if directory:
            logger = create_logger()
            move_records = []

            if chosen_type.get() == 1:
                sort_method = 'type'
            elif chosen_type.get() == 2:
                sort_method = 'date'

            dry_run = dry_run_var.get()
            include_subdirs = include_subdirs_var.get()
            
            file_counter.get_files_count(directory, include_subdirs)
            
            organize_files_recursively(directory, logger, dry_run, move_records, sort_method, include_subdirs, progress_bar, root, log_table)
            
            messagebox.showinfo("Success", f"Files have been organized by {sort_method}!")
            progress_bar['value'] = 0

            if dry_run_var.get() == 0:
                undo_button['state'] = 'normal'
                undo_button['command'] = lambda: undo_last_operation(move_records, logger, undo_button, log_table)

            file_counter.filesCount = 0
            file_counter.curentFileNum = 0
    except Exception as e:
        messagebox.showerror("Error", str(e))