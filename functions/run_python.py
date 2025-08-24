import os
import subprocess

def run_python_file(working_directory, file_path, args=[]):
    try:
        full_path = os.path.join(working_directory, file_path)
        abs_working_dir = os.path.abspath(working_directory)
        abs_file_path = os.path.abspath(full_path)

        if not abs_file_path.startswith(abs_working_dir):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.exists(abs_file_path):
            return f'Error: File "{file_path}" not found.'
        
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'
        
        try:
            result = subprocess.run(["python", file_path], cwd=abs_working_dir, capture_output=True, text=True, timeout=30)
            output = f"STDOUT: {result.stdout}STDERR: {result.stderr}"
            
            if result.stdout == None and result.stderr == None:
                return "No output produced."
            else:
                return output
        except subprocess.CalledProcessError as e:
            return f"Process exited with code {e.returncode}"
    
    except Exception as e:
        return f"Error: executing Python file: {e}"
