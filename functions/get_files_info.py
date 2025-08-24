import os
from google.genai import types

def get_files_info(working_directory, directory="."):
    try:
        full_path = os.path.join(working_directory, directory)

        abs_working_dir = os.path.abspath(working_directory)
        abs_target_dir = os.path.abspath(full_path)

        if not abs_target_dir.startswith(abs_working_dir):
            return f'    Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
        if not os.path.isdir(abs_target_dir):
            return f'    Error: "{directory}" is not a directory'
    
        result_lines = []
        for entry in os.listdir(abs_target_dir):
            entry_path = os.path.join(abs_target_dir, entry)
            try:
                file_size = os.path.getsize(entry_path)
                is_dir = os.path.isdir(entry_path)
                result_lines.append(f"- {entry}: file_size={file_size} bytes, is_dir={is_dir}")
            except Exception as e:
                result_lines.append(f"- {entry}: Error: {e}")

        return "\n".join(result_lines)
    
    except Exception as e:
        return f"Error: {e}"
