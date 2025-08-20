import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.run_python import run_python_file
from functions.write_file import write_file
from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.get_file_content import schema_get_file_content
from functions.get_files_info import schema_get_files_info
from functions.run_python import schema_run_python
from functions.write_file import schema_write_file

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY") 

client = genai.Client(api_key=api_key)

system_prompt = """
You are an AI coding agent that analyzes code and provides direct answers.

Available functions:
- List files and directories
- Read file contents  
- Execute Python files with optional arguments
- Write or overwrite files

Use these functions to gather information needed to answer questions. Provide factual, technical answers without conversational language like "I've examined" or "Let me check". State findings directly.

Example good response: "The calculator renders results using the render() function in pkg/render.py, which creates a formatted box around the expression and result using ASCII characters."

Example bad response: "Okay, I've examined the code and here's how it works: [explanation]"
Provide your analysis or explanation once when the task is complete. Do not acknowledge with "OK", ask follow-up questions, or continue the conversation unless additional clarification is needed to complete the original request.
Once you have completed the user's request and provided the necessary information or explanation, stop. Do not engage in conversational pleasantries or ask follow-up questions unless the task requires clarification to proceed.
"""

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info, schema_write_file, schema_run_python, schema_get_file_content
    ]
)
working_directory = "./calculator"
func_defs = {
    "run_python_file": run_python_file,
    "get_file_content": get_file_content,
    "get_files_info": get_files_info,
    "write_file": write_file
}
def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")
    try:
        curr_func = func_defs[function_call_part.name]
    except:
        return types.Content(
            role="user",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unknown function: {function_call_part.name}"},
                )
            ],
        )

    func_args = function_call_part.args or {}  # Handle None case
    func_args = dict(func_args)  # Ensure it's a dict we can modify
    func_args['working_directory'] = working_directory
    result = curr_func(**func_args)

    if isinstance(result, str):
        result = {"result": result}
    elif not isinstance(result, dict):
        result = {"result": str(result)}

    return types.Content(
        role="user",
        parts=[
            types.Part.from_function_response(
                name=function_call_part.name,
                response=result,
            )
        ],
    )

def main():
    max_iters = 20
    curr_iter = 0
    if len(sys.argv) < 2:
        print("Need a cmd line argument to use the model!")
        sys.exit(1)

    user_prompt = sys.argv[1]
    verbose = len(sys.argv) > 2 and sys.argv[2] == "--verbose" 
    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]

    while curr_iter < max_iters:
        try:
            response = client.models.generate_content(model="gemini-2.0-flash-001", contents=messages, 
                                                      config=types.GenerateContentConfig(
                                                      tools=[available_functions], system_instruction=system_prompt
                                                      ),
                                                      )

            has_func_call = False
            for item in response.candidates:
                output_content = item.content
                messages.append(output_content)

                for part in output_content.parts:
                    if part.function_call:
                        has_func_call = True
                        try:
                            func_call_result = call_function(function_call_part=part.function_call, verbose=(verbose))
                            messages.append(func_call_result)
                        except Exception as e:
                            print(f"Error running function: {e}")
                            error_content = types.Content(
                                role="user",
                                parts=[types.Part(text=f"Function call error: {e}")]
                            )
                            messages.append(error_content)
                    elif part.text:
                        print(part.text)

            if not has_func_call:
                if verbose:
                    print("User prompt:", user_prompt)
                    print("Prompt tokens:", response.usage_metadata.prompt_token_count) 
                    print("Response tokens:", response.usage_metadata.candidates_token_count) 
                break
            curr_iter += 1
        except Exception as e:
            print(f"Error in generate_content: {e}")
            break

    if curr_iter >= max_iters:
        print("Maximum iterations reached. Stopping.")

if __name__ == "__main__":
    main()
