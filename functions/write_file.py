import os
import sys
from google.genai import types

def write_file(working_directory, file_path, content):
    working_directory = os.path.abspath(working_directory)
    curr_path = os.path.join(working_directory, file_path)

    if not os.path.commonpath([working_directory])== os.path.commonpath([working_directory, curr_path]):
        print(f'Error: Cannot read "{file_path}" as it is outside the permitted working directory')
        sys.exit(0)

    if not os.path.isfile(curr_path):
        print(f'Error: File not found or is not a regular file: "{file_path}"')

    with open(curr_path, "w") as file:
        file.write(content)

    print(f'Successfully wrote to "{file_path}" ({len(content)} characters written)')

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to the specified file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to write to, which must be present in the current working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file.",
            ),
        },
    ),
)
