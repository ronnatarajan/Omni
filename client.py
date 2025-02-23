import argparse
import modal
from openai import OpenAI
from datetime import datetime
import pytz


def get_completion(client, model_id, messages, args):
    completion_args = {
        "model": model_id,
        "messages": messages,
        "frequency_penalty": args.frequency_penalty,
        "max_tokens": args.max_tokens,
        "n": args.n,
        "presence_penalty": args.presence_penalty,
        "seed": args.seed,
        "stop": args.stop,
        "stream": args.stream,
        "temperature": args.temperature,
        "top_p": args.top_p,
    }

    completion_args = {k: v for k, v in completion_args.items() if v is not None}

    response = client.chat.completions.create(**completion_args)
    return response


def analyze_text(user_input):
    parser = argparse.ArgumentParser(description="OpenAI Client CLI")
    
    parser.add_argument(
        "--model",
        type=str,
        default=None,
        help="The model to use for completion, defaults to the first available model",
    )
    parser.add_argument(
        "--workspace",
        type=str,
        default=None,
        help="The workspace where the LLM server app is hosted, defaults to your current Modal workspace",
    )
    parser.add_argument(
        "--environment",
        type=str,
        default=None,
        help="The environment in your Modal workspace where the LLM server app is hosted, defaults to your current environment",
    )
    parser.add_argument(
        "--app-name",
        type=str,
        default="example-vllm-openai-compatible",
        help="A Modal App serving an OpenAI-compatible API",
    )
    parser.add_argument(
        "--function-name",
        type=str,
        default="serve",
        help="A Modal Function serving an OpenAI-compatible API. Append `-dev` to use a `modal serve`d Function.",
    )
    parser.add_argument(
        "--api-key",
        type=str,
        default="super-secret-key",
        help="The API key to use for authentication, set in your api.py",
    )

    # Completion parameters
    parser.add_argument("--max-tokens", type=int, default=None)
    parser.add_argument("--temperature", type=float, default=0.7)
    parser.add_argument("--top-p", type=float, default=0.9)
    parser.add_argument("--top-k", type=int, default=0)
    parser.add_argument("--frequency-penalty", type=float, default=0)
    parser.add_argument("--presence-penalty", type=float, default=0)
    parser.add_argument(
        "--n",
        type=int,
        default=1,
        help="Number of completions to generate. Streaming and chat mode only support n=1.",
    )
    parser.add_argument("--stop", type=str, default=None)
    parser.add_argument("--seed", type=int, default=None)

    parser.add_argument(
        "--system-prompt",
        type=str,
        default="You are a poetic assistant, skilled in writing satirical doggerel with creative flair.",
        help="The system prompt for the chat completion",
    )

    parser.add_argument(
        "--no-stream",
        dest="stream",
        action="store_false",
        help="Disable streaming of response chunks",
    )

    args = parser.parse_args()

    client = OpenAI(api_key=args.api_key)

    workspace = args.workspace or modal.config._profile
    environment = args.environment or modal.config.config["environment"]
    prefix = workspace + (f"-{environment}" if environment else "")

    client.base_url = f"https://{prefix}--{args.app_name}-{args.function_name}.modal.run/v1"
    model = client.models.list().data[0]
    model_id = model.id

    # Default structured prompt
    default_prompt = (
        "Given a set of text, can you identify the name of the event, "
        "the location of the event, and the start and end time of the event, where the start time and end time "
        "are given in a 24 hour time format, with time only in hours and minutes , along with the date in YYYY-MM-DD format, If there is no explicit date given "
        "assume that the start and end time are today if the start time listed is after our current date time of " + datetime.now(pytz.timezone('America/New_York')).strftime('%Y-%m-%dT%H:%M:%S') + 
        ", otherwise assume the start and end time are the next day. Always make sure the start and end date are the same day if no explicit end date was given. If there is no explicit end time "
        "given then guess the amount of time the event would take place, with it being usually in increments of 30 minutes to an hour, and the end time has to be after the start time"
        "Then output everything in the following format and don't include your reasoning:\nName=\nLocation=\nStartTime=\nEndTime=\nStartDate=\nEndDate=\n"
        "Here is the text I want you to analyze:\n"
    )

    #Analyzing text
    # user_input = ("( Oo Madhav Valiyaparambil <vpmadhav@gmail.com>"
    #             "ee tome +"
    #             "Yo Saket,"
    #             "Wanna meet up at 12:00 at Krach to Study for a little bit")

    # Combine structured prompt with user input or use placeholder
    final_prompt = default_prompt + user_input

    messages = [
        {"role": "system", "content": args.system_prompt},
        {"role": "user", "content": final_prompt},
    ]

    response = get_completion(client, model_id, messages, args)

    formatted_output = ""
    
    if response:
        if args.stream:
            for chunk in response:
                if chunk.choices[0].delta.content:
                    formatted_output += str(chunk.choices[0].delta.content)
    
    return formatted_output
