import os

def get_file_content(working_directory, file_path):
    try:
        full_path = os.path.join(working_directory, file_path)

        abs_working_path = os.path.abspath(working_directory)
        abs_file_path = os.path.abspath(full_path)

        if not abs_file_path.startswith(abs_working_path):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(abs_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
    
        MAX_CHARS = 10000
        with open(abs_file_path, "r") as file:
            content = file.read()

        if len(content) > MAX_CHARS:
            content = content[:MAX_CHARS] + f' [...File "{file_path}" truncated at {MAX_CHARS} characters]'

        return content
    
    except Exception as e:
        return f"Error: {str(e)}"
