import os
import sys
from google.genai import types

def get_files_info(working_directory, directory=None):
    working_directory = os.path.abspath(working_directory)


    if not directory:
        curr_path = working_directory
        display_path = "."
    else:
        curr_path = os.path.abspath(os.path.join(working_directory, directory))
        display_path = directory

    if not working_directory == os.path.commonpath([working_directory, curr_path]):
        error_msg = f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        print(error_msg)
        return {"error": error_msg}
    
    if not os.path.isdir(curr_path):
        error_msg = f'Error: "{directory or "working directory"}" is not a directory'
        print(error_msg)
        return {"error": error_msg}
    
    try:
        files = []
        directories = []
        
        for item in os.listdir(curr_path): 
            item_path = os.path.join(curr_path, item)
            is_path_dir = os.path.isdir(item_path)
            
            if is_path_dir:
                dir_size = get_dirsize(item_path)
                directories.append({
                    'name': item,
                    'size': dir_size,
                    'is_dir': True,
                    'type': 'directory'
                })
                print(f'{item}: file_size={dir_size} bytes, is_dir={is_path_dir}')
            else:
                file_size = os.path.getsize(item_path)
                files.append({
                    'name': item,
                    'size': file_size,
                    'is_dir': False,
                    'type': 'file'
                })
                print(f'{item}: file_size={file_size} bytes, is_dir={is_path_dir}')
        
        # Return structured data for the AI
        return {
            'working_directory': working_directory,
            'listed_directory': curr_path,
            'relative_path': display_path,
            'files': files,
            'directories': directories,
            'total_files': len(files),
            'total_directories': len(directories),
            'all_items': files + directories  # Combined list for easier access
        }
        
    except PermissionError:
        error_msg = f'Error: Permission denied accessing "{curr_path}"'
        print(error_msg)
        return {"error": error_msg}
    except Exception as e:
        error_msg = f'Error listing files in "{curr_path}": {str(e)}'
        print(error_msg)
        return {"error": error_msg}

def get_dirsize(start_path = '.'):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)

    return total_size

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),

            "working_directory": types.Schema(
                type=types.Type.STRING,
                description="The working directory that contains the directory specified to search. If the directory to search is not specified, return the contents of the working directory.",
            ),
        },
        required=["working_directory"]
    ),
)
