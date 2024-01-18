import argparse

from gui_folder_organization import create_gui                      #Imported from gui_folder_organization.py. GUI mode runs in this  code.
from run_modes.terminal_mode import run_terminal_mode               #Imported from terminal_mode.py
from run_modes.cli_mode import run_cli_mode                         #Imported from terminal_mode.py

def main():
    parser = argparse.ArgumentParser(description = 'Organize files in a directory.')
    parser.add_argument('--run_mode', choices = ['gui', 'cli', 'terminal'], default = 'gui', help = 'List of avaliable launch methodes. ')
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