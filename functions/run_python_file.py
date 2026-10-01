import os
import subprocess

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Executes python file in a specified directory relative to the working directory with conditional arguements",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to file, relative to the working directory (default is the working directory itself)",
                },
                "args": {
                    "type": "list",
                    "description": "List of arguements passed to the function",
                },
            },
        },
    },
}

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_path = os.path.commonpath([working_dir_abs, target_path]) == working_dir_abs

        if not valid_target_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        elif not os.path.isfile(target_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        elif not target_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        else:
            command = ["python", target_path]
            if args:
                command.extend(args)
            comp_proc = subprocess.run(
                command,
                cwd = working_dir_abs,
                capture_output = True,
                text = True,
                timeout = 30
            )
            output = []
            if comp_proc.returncode != 0:
                output.append(f"Process exited with code {comp_proc.returncode}")
            if not comp_proc.stdout and not comp_proc.stderr:
                output.append("No output produced")
            else:
                if comp_proc.stdout:
                    output.append(f"STDOUT:\n{comp_proc.stdout}")
                if comp_proc.stderr:
                    output.append(f"STDERR:\n{comp_proc.stderr}")
            return "\n".join(output)
    except Exception as e:
        return f"Error: executing Python file: {e}"
