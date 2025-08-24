import os
import sys
import argparse
from google import genai
from dotenv import load_dotenv
from google.genai import types
from functions.call_function import call_function
from functions.schema import schema_get_files_info, schema_get_file_content, schema_write_file, schema_run_python

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python,
    ]
)

parser = argparse.ArgumentParser(description="AI Agent that takes CLI prompts with flags.")
parser.add_argument("prompt", type=str, help="The user prompt for the AI agent.")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output.")

args = parser.parse_args()

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

if (len(sys.argv) < 2):
    print("No prompt provided")
    sys.exit(1)

messages = [
    types.Content(role="user", parts=[types.Part(text=args.prompt)])
]

counter = 20

while counter > 0:
    counter -= 1

    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash-001',
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions], system_instruction=system_prompt
            )
        )

        output = response.text
        function_call_list = response.function_calls
        prompt_tokens = response.usage_metadata.prompt_token_count
        response_tokens = response.usage_metadata.candidates_token_count
    
        if output and not function_call_list:
            print("Final response: ")
            print(output)
            break

        for candidate in response.candidates:
            if candidate.content:
                messages.append(candidate.content)

                for part in candidate.content.parts:
                    if part.function_call:
                        
                        function_result = call_function(part.function_call, verbose=args.verbose)

                        if (
                            not function_result.parts
                            or not function_result.parts[0].function_response
                            or function_result.parts[0].function_response.response is None
                        ):
                            raise RuntimeError("Fatal: Function call did not return a response")

                        messages.append(function_result)

                        if args.verbose:
                            print(f"-> {function_result.parts[0].function_response.response}")

    except Exception as e:
        print(f"Error: {e}")
        break
