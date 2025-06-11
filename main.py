import os
import sys
from prompts import system_prompt
from config import MAX_ITERATIONS
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

    i = 0
    while True:
        i += 1
        if i > MAX_ITERATIONS:
            print(f'Max iterations ({MAX_ITERATIONS} reached.')
            sys.exit(1)

        try:
            final_resp = generate_content(client, user_prompt, messages, input_flags)
            if final_resp:
                print(f'Final response: {final_resp}')
                break
        except Exception as e:
            print(f'Error: {e}')

def generate_content(client, user_prompt, messages, *args):
    resp = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )

    if resp.candidates:
        for c in resp.candidates:
            messages.append(c.content)

    verbose = "--verbose" in args
    if verbose:
        print(f'Prompt tokens: {resp.usage_metadata.prompt_token_count}')
        print(f'Response tokens: {resp.usage_metadata.candidates_token_count}')

    if not resp.function_calls:
        return resp.text

    func_resp = []
    for func in resp.function_calls:
        r = call_function(func, verbose)
        if (not r.parts or not r.parts[0].function_response.response):
            raise Exception(f'Failed to call function {func.name}({func.args})')
        if verbose:
            print(f"-> {r.parts[0].function_response.response}")
        func_resp.append(r.parts[0])

    if not func_resp:
        raise Exception("No function responses generated")

    messages.append(types.Content(role="tool", parts=func_resp))

if __name__ == "__main__":
    main()
