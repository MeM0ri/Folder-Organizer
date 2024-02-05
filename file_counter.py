import os

global filesCount
global curentFileNum

def get_files_count(directory, include_subdirs):
    for item in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, item)):
            filesCount += 1
            print(filesCount)
        elif os.path.isdir(item) and include_subdirs:
            get_files_count(directory)