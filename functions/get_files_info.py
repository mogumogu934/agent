import os

def get_files_info(working_directory, directory=None):
    if not directory:
        directory = "."

    target_path = os.path.abspath(os.path.join(os.path.abspath(working_directory), directory))
    if not target_path.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(target_path):
        return f'Error: "{directory}" is not a directory'

    contents = []
    for f in os.listdir(target_path):
        fp = os.path.join(target_path, f)
        try:
            fs = os.path.getsize(fp)
        except Exception as e:
            print(f'Error: {e}')
            continue
        s = f'- {f}: file_size={fs} bytes, is_dir={os.path.isdir(fp)}'
        contents.append(s)

    print(f'Files in {target_path}:')
    return "\n".join(contents)
