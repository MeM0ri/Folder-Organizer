import os
import shutil

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

def undo_last_operation(move_records, logger, undo_button = None):
    for target_directory, original_path in reversed(move_records):
        try:
            shutil.move(os.path.join(target_directory, os.path.basename(original_path)), original_path)
            logger.info(f"Reversed move: {original_path} back to {target_directory}")

            if undo_button:
                undo_button['state'] = 'disabled'
        except Exception as e:
            logger.error(f"Error reversing file move from {target_directory} to {original_path}: {e}")