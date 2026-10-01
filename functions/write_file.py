import os

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Writes to or overwrites files in a specified directory relative to the working directory",
        "parameters": {
            "type": "object",
            "file_path": {
                "file_path": {
                    "type": "string",
                    "description": "Path to file, relative to the working directory (default is the working directory itself)",
                },
            },
            "properties": {
                "content": {
                    "type": "string",
                    "description": "Content to write to file",
                },
            },
        },
    },
}

def write_file(working_directory: str, file_path: str, content: str) -> str:
    working_dir_abs = os.path.abspath(working_directory)
    target_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
    valid_target_path = os.path.commonpath([working_dir_abs, target_path]) == working_dir_abs

    try:
        if not valid_target_path:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        elif os.path.isdir(target_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        with open(target_path, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"
