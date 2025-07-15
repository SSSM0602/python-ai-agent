import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY") 

client = genai.Client(api_key=api_key)

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

def main():
    if len(sys.argv) < 2:
        print("Need a cmd line argument to use the model!")
        sys.exit(1)

    user_prompt = sys.argv[1]
    messages = types.Content(role="user", parts=[types.Part(text=user_prompt)])
    response = client.models.generate_content(model="gemini-2.0-flash-001", contents=messages, config=types.GenerateContentConfig(system_instruction=system_prompt),)
    print(response.text)
    if (len(sys.argv) > 2):
        if (sys.argv[2] == "--verbose"):
            print("User prompt:", user_prompt)
            print("Prompt tokens:", response.usage_metadata.prompt_token_count) 
            print("Response tokens:", response.usage_metadata.candidates_token_count) 

if __name__ == "__main__":
    main()
