import os
from google.genai import types # type: ignore

def get_files_info(working_directory, directory=None):
    abs_working_directory = os.path.abspath(working_directory)
    if not os.path.isdir(abs_working_directory):
        return f'Error: {abs_working_directory} is not a directory'

    if not directory:
        directory = "."

    target_path = os.path.abspath(os.path.join(working_directory, directory))
    if not target_path.startswith(abs_working_directory):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(target_path):
        return f'Error: "{directory}" is not a directory'

    try:
        info = []
        for f in os.listdir(target_path):
            fp = os.path.join(target_path, f)
            fs = 0
            fs = os.path.getsize(fp)
            info.append(f'- {f}: file_size={fs} bytes, is_dir={os.path.isdir(fp)}')
        return "\n".join(info)
    except Exception as e:
        return f'Error: {e}'

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
        },
    ),
)
