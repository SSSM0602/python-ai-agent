import os
import sys

def get_files_info(working_directory, directory=None):
    working_directory = os.path.abspath(working_directory)
    curr_path = os.path.join(working_directory, directory)

    if not os.path.commonpath([working_directory])== os.path.commonpath([working_directory, curr_path]):
        print(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
        sys.exit(0)

    if not (os.path.isdir(curr_path)):
        print(f'Error: "{directory}" is not a directory')
        sys.exit(0)
    
    for item in os.listdir(curr_path): 
        item_path = os.path.join(curr_path, item)
        is_path_dir = os.path.isdir(item_path)
        if is_path_dir:
            print(f'{item}: file_size={get_dirsize(item_path)} bytes, is_dir={is_path_dir}')
        else:
            print(f'{item}: file_size={os.path.getsize(item_path)} bytes, is_dir={is_path_dir}')
        

def get_dirsize(start_path = '.'):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)

    return total_size
