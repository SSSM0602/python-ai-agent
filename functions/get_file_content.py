import os
import sys
from . import config
def get_file_content(working_directory, file_path):
    working_directory = os.path.abspath(working_directory)
    curr_path = os.path.join(working_directory, file_path)

    if not os.path.commonpath([working_directory])== os.path.commonpath([working_directory, curr_path]):
        print(f'Error: Cannot read "{file_path}" as it is outside the permitted working directory')
        sys.exit(0)

    if not os.path.isfile(curr_path):
        print(f'Error: File not found or is not a regular file: "{file_path}"')
        
    with open(curr_path, "r") as file:
        file_content = file.read(config.FILE_CHAR_LIMIT)

    print(file_content)
    if (os.path.getsize(curr_path) > config.FILE_CHAR_LIMIT):
        print(f'[...File "{file_path}" truncated at 10000 characters]')
