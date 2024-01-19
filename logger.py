import logging

from text_handler import TextHandler

def create_logger(text_widget = None):
    #Create logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    #File handler for writing to log file
    file_handler = logging.FileHandler('file_organizer.log', mode = 'w', encoding = 'utf-8')
    file_formatter = logging.Formatter('%(asctime)s: %(message)s')
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    #Text widget handler for updating the GUI (only if text_widget is provided)
    if text_widget is not None:
        text_handler = TextHandler(text_widget)
        text_formatter = logging.Formatter('%(asctime)s: %(message)s')
        text_handler.setFormatter(text_formatter)
        logger.addHandler(text_handler)
    
    return logger