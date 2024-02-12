import os

filesCount = 0
curentFileNum = 0

def get_files_count(directory, include_subdirs):
    for item in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, item)):
            global filesCount
            filesCount += 1
            print(filesCount)
        elif os.path.isdir(item) and include_subdirs:
            get_files_count(directory)