import tkinter as tk
import ttkbootstrap as ttk

from tkinter import filedialog, messagebox
from run_modes.gui_mode import run_gui_mode

def select_directory(directory_entry):
    try:
        directory = filedialog.askdirectory()
        if directory:
            directory_entry.delete(0, tk.END)
            directory_entry.insert(0, directory)
    except Exception as e:
        messagebox.showerror("Error", str(e))

def create_gui():

    def on_directory_change(*args):
        undo_button['state'] = 'disabled'

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

    directory_var = tk.StringVar()
    directory_var.trace_add('write', on_directory_change)

    directory_entry = tk.Entry(centered_frame, width = 50, textvariable = directory_var)
    directory_entry.pack(side = tk.LEFT, pady = 3, padx = (5, 0))

    browse_button = tk.Button(centered_frame, text = "Browse", command = lambda: select_directory(directory_entry))
    browse_button.pack(side = tk.LEFT, pady = 3, padx = (0, 5))

    #Log text var
    log_frame = ttk.LabelFrame(root, text = "File Organizer Logs")
    log_frame.pack(side = tk.TOP, fill = "both", expand = True, padx = 5, pady = 5)

    log_text = tk.Text(log_frame, height = 5, state = 'disabled')
    log_text.pack(fill = "both", expand = True, padx = 5, pady = 5)

    #Progress bar var
    progress_bar = ttk.Progressbar(root, orient = tk.HORIZONTAL, length = 300, mode = 'determinate')
    progress_bar.pack(side = tk.TOP, pady = 10)
    
    #Button for running organize script
    buttons_frame = ttk.Frame(root)
    buttons_frame.pack(side = tk.TOP, expand = True, padx = 5, pady = 5, ipadx = 3, ipady = 3)
    
    organize_button = tk.Button(buttons_frame, text = "Organize Files", command = lambda: run_gui_mode(chosen_type, progress_bar, undo_button, root, directory_entry, log_text, include_subdirs_var, dry_run_var))
    organize_button.pack(side = tk.LEFT, pady = 3, padx = (5, 0))

    undo_button = tk.Button(buttons_frame, text = "Undo", state = 'disabled')
    undo_button.pack(side = tk.LEFT, pady = 3, padx = (0, 5))

    root.mainloop()