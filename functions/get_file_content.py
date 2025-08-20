import os
import sys
from . import config
from google.genai import types
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

    return file_content


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Displays content of the specified file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to retrieve content from, which must be present in the current working directory.",
            ),

            "working_directory": types.Schema(
                type=types.Type.STRING,
                description="The current working directory that contains the relevant file.",
            ),
        },
        required=["working_directory", "file_path"]
    ),
)
