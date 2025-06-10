import os

def get_file_content(working_directory, file_path):
    if not file_path:
        return "Error: must provide a file path"

    target_path = os.path.abspath(os.path.join(os.path.abspath(working_directory), file_path))
    if not target_path.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(target_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    MAX_CHARS = 10000
    with open(target_path) as f:
        s = f.read(MAX_CHARS) + f'\n[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        print(f'Content in {file_path}:')
        return s
