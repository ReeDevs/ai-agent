import os
from dotenv import load_dotenv
from openai import OpenAI
import argparse
from prompts import system_prompt
from call_function import available_functions, call_function
import sys


def main():
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if api_key == None:
        raise RuntimeError("no api key found")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [
        {"role": "system",  "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]

    is_finished = False
    for _ in range(20):

        response = client.chat.completions.create(
            model="openrouter/free",
            messages=messages,
            tools=available_functions,
        )

        if response.usage is not None:
            if args.verbose == True:
                print(f"User prompt: {args.user_prompt}")
                print(f"Prompt tokens: {response.usage.prompt_tokens}")
                print(f"Response tokens: {response.usage.completion_tokens}")
        else:
            raise RuntimeError("Failed API request")
        message = response.choices[0].message
        messages.append(message)
        if message.tool_calls != None:
            for tool_call in message.tool_calls:
                result_message = call_function(tool_call, args.verbose)
                if not result_message["content"]:
                    raise Exception("Empty content")
                if args.verbose == True:
                    print(f"-> {result_message['content']}")
                messages.append(result_message)
        else:
            is_finished = True
            print(message.content)
            break
    if is_finished == False:
        print("Out of iterations with no solutions")
        sys.exit(1)


if __name__ == "__main__":
    main()
