import os

def write_file(working_directory, file_path, content):
    if not file_path:
        return "Error: must provide a file path"

    target_path = os.path.abspath(os.path.join(os.path.abspath(working_directory), file_path))
    if not target_path.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(os.path.dirname(target_path)):
        try:
            os.makedirs(os.path.dirname(target_path))
        except Exception as e:
            return f'Error: {e}'

    try:
        with open(target_path, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: {e}'
