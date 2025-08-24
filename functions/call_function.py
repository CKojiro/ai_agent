from google.genai import types
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python import run_python_file

def call_function(function_call_part, verbose=False):
    if verbose == True:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    
    print(f" - Calling function: {function_call_part.name}")

    function_name = function_call_part.name
    function_args = function_call_part.args
    passed_args = {"working_directory": "./calculator", **function_args}

    match function_name:
        case "get_files_info":
            function_result = get_files_info(**passed_args)
        case "get_file_content":
            function_result = get_file_content(**passed_args)
        case "write_file":
            function_result = write_file(**passed_args)
        case "run_python_file":
            function_result = run_python_file(**passed_args)
        case _:
            return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_name,
                        response={"error": f"Unknown function: {function_name}"},
                    )
                ],
            )
    
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )
