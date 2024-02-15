import os
import shutil

def move_file(file_path, target_directory, logger, dry_run = False, move_records = None, log_table = None):
    if dry_run:
        logger.info(f"[DRY RUN] Would move file {file_path} to {target_directory}")

        if log_table is not None:
            head, tail = os.path.split(file_path)
            log_table.insert_row('end', ['Move', 'YES', tail, head, target_directory])
            log_table.load_table_data()
    else:
        try:
            shutil.move(file_path, target_directory)
            logger.info(f"Move file {file_path} to {target_directory}")

            if log_table is not None:
                head, tail = os.path.split(file_path)
                log_table.insert_row('end', ['Move', 'NO', tail, head, target_directory])
                log_table.load_table_data()
            
            if move_records is not None:
                move_records.append((target_directory, file_path)) 
        except Exception as e:
            logger.error(f"Error moving file {file_path} to {target_directory}: {e}")

def undo_last_operation(move_records, logger, undo_button = None, log_table = None):
    for target_directory, original_path in reversed(move_records):
        try:
            shutil.move(os.path.join(target_directory, os.path.basename(original_path)), original_path)
            logger.info(f"Reversed move: {original_path} back to {target_directory}")

            if log_table is not None:
                head, tail = os.path.split(original_path)
                log_table.insert_row('end', ['Reversed move', 'NO', tail, target_directory, head])
                log_table.load_table_data()

            if undo_button:
                undo_button['state'] = 'disabled'
        except Exception as e:
            logger.error(f"Error reversing file move from {target_directory} to {original_path}: {e}")