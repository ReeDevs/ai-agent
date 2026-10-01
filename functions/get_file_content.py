import os
from config import character_limit

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Reads a file and lists the file's content in a specified directory relative to the working directory, truncating response to a set character limit",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}

def get_file_content(working_directory: str, file_path: str) -> str:
    working_dir_abs = os.path.abspath(working_directory)
    target_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
    valid_target_path = os.path.commonpath([working_dir_abs, target_path]) == working_dir_abs

    try:
        if not valid_target_path:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        elif not os.path.isfile(target_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        with open(target_path, "r") as f:
            file_content_string = f.read(character_limit)
            if f.read(1):
                file_content_string += f'[...File "{file_path}" truncated at {character_limit} characters]'
        return file_content_string
    except Exception as e:
        return f"Error: {e}"
