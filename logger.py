import logging

def create_logger():
    #Create logger
    logger = logging.getLogger("file_organizer_logger")
    logger.setLevel(logging.INFO)

    #File handler for writing to log file
    file_handler = logging.FileHandler('file_organizer.log', mode = 'w', encoding = 'utf-8')
    file_formatter = logging.Formatter('%(asctime)s: %(message)s')
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    
    return logger