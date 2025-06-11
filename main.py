import os
import sys
from prompts import system_prompt
from call_function import call_function, available_functions
from google import genai # type: ignore
from google.genai import types # type: ignore
from dotenv import load_dotenv # type: ignore

def main():
    load_dotenv()

    input = sys.argv[1:]
    if not input:
        print("usage: python3 main.py <prompt>")
        sys.exit(1)

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    flags = ["--verbose"]
    input_flags = ""
    first_flag_idx = float('inf')
    for idx, i in enumerate(input):
        for f in flags:
            if i == f:
                if first_flag_idx > idx:
                    first_flag_idx = idx

    if first_flag_idx != float('inf'):
        input, input_flags = input[:first_flag_idx], " ".join((input[first_flag_idx:]))
    user_prompt = " ".join(input)
    messages = [
            types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    generate_content(client, user_prompt, messages, input_flags)

def generate_content(client, user_prompt, messages, *args):
    resp = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )

    verbose = "--verbose" in args
    if verbose:
        print(f'Prompt tokens: {resp.usage_metadata.prompt_token_count}')
        print(f'Response tokens: {resp.usage_metadata.candidates_token_count}')

    if not resp.function_calls:
        print(f'Response: {resp.text}')

    f_resp = []
    for f in resp.function_calls:
        r = call_function(f, verbose)
        if (not r.parts or not r.parts[0].function_response.response):
            raise Exception(f'Failed to call function {f.name}({f.args})')
        if verbose:
            print(f"-> {r.parts[0].function_response.response}")
        f_resp.append(r.parts[0])

    if not f_resp:
        raise Exception("No function responses generated")

if __name__ == "__main__":
    main()
