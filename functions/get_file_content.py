import os
from config import MAX_CHARS
from google.genai import types # type: ignore

def get_file_content(working_directory, file_path):
    abs_working_directory = os.path.abspath(working_directory)
    if not os.path.isdir(abs_working_directory):
        return f'Error: {abs_working_directory} is not a directory'

    target_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not target_path.startswith(abs_working_directory):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(target_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        with open(target_path, "r") as f:
            c = f.read(MAX_CHARS)
            if len(c) == MAX_CHARS:
                c += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            return c
    except Exception as e:
        return f'Error: {e}'

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=f'Reads and returns contents of a file within the working directory. Truncated to {MAX_CHARS} characters.',
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file whose content to be read, relative to the working directory.",
            ),
        },
    ),
)
