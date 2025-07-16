import os
import sys
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path):
    working_directory = os.path.abspath(working_directory)
    curr_path = os.path.abspath(os.path.join(working_directory, file_path))
    print(curr_path)


    if not working_directory == os.path.commonpath([working_directory, curr_path]):
        print(f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory')
        #sys.exit(0)
        return

    if not os.path.exists(curr_path) or not os.path.isfile(curr_path):
        print(f'Error: File "{file_path}" not found.')
        #sys.exit(0)
        return

    if not curr_path.endswith(".py"):
        print(f'Error: "{file_path}" is not a Python file.')
        #sys.exit(0)
        return

    try: 
        runpy = subprocess.run(f'uv run {curr_path}', capture_output=True, timeout=30, shell=True, text=True)
        if runpy.stdout:
            print(f'STDOUT: {runpy.stdout}')
        else:
            print("No output produced")

        if runpy.stderr:
            print(f'STDERR: {runpy.stderr}')

        if runpy.returncode != 0:
            print(f'Process exited with code {runpy.stderr}')

    except Exception as e:
        print(f"Error: executing Python file: {e}")


schema_run_python = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs the specified python file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The python file to run, which must be present in the current working directory.",
            ),
        },
    ),
)
