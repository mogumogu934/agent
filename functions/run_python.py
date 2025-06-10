import os
import subprocess

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

        print(f'\nExecuting {target_path}...')
        p = subprocess.run(
            commands,
            capture_output=True,
            text=True,
            timeout=30,
            cwd=os.path.abspath(working_directory)
        )

        output = []
        if p.stdout:
            output.append(f'STDOUT:\n{p.stdout}')
        if p.stderr:
            output.append(f'STDERR:\n{p.stderr}')
        if p.returncode:
            output.append(f'Process exited with code {p.returncode}')

    except Exception as e:
        return f"Error: executing Python file: {e}"

    if not output:
        return "No output produced."

    return "\n".join(output)
