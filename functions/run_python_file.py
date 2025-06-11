import os
import subprocess
from google.genai import types # type: ignore

def run_python_file(working_directory, file_path, args=None):
    abs_working_directory = os.path.abspath(working_directory)
    if not os.path.isdir(abs_working_directory):
        return f'Error: {abs_working_directory} is not a directory'

    target_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not target_path.startswith(abs_working_directory):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(target_path):
        return f'Error: File "{file_path}" not found.'
    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'


    try:
        commands = ["python", target_path]
        if args:
            commands.extend(args)

        r = subprocess.run(
            commands,
            capture_output=True,
            text=True,
            timeout=30,
            cwd=abs_working_directory,
        )

        output = []
        if r.stdout:
            output.append(f'STDOUT:\n{r.stdout}')
        if r.stderr:
            output.append(f'STDERR:\n{r.stderr}')
        if r.returncode:
            output.append(f'Process exited with code {r.returncode}')
        if not output:
            return "No output produced."
        return "\n".join(output)
    except Exception as e:
        return f"Error: executing Python file: {e}"

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file within the working directory and returns the output.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the Python file to be executed, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.STRING,
                description="The optional arguments to pass to the Python file.",
            ),
        },
    ),
)
