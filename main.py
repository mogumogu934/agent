import os
import sys
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

    generate_content(client, messages, user_prompt, input_flags)

def generate_content(client, messages, user_prompt, *args):
    resp = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
    )

    print(f"Response: {resp.text}")

    if "--verbose" in args:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {resp.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {resp.usage_metadata.candidates_token_count}")

if __name__ == "__main__":
    main()
