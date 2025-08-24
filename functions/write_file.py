import os

def write_file(working_directory, file_path, content):
    try:
        full_path = os.path.join(working_directory, file_path)
        abs_working_path = os.path.abspath(working_directory)
        abs_file_path = os.path.abspath(full_path)

        if not abs_file_path.startswith(abs_working_path):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.exists(file_path):
            with open(abs_file_path, 'w') as file:
                file.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        else:
            with open(abs_file_path, 'w') as file:
                file.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        print(f"Error: {str(e)}")
