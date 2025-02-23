import argparse
import modal
from openai import OpenAI
import datetime
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

    est_time = datetime.datetime.now(pytz.timezone('America/New_York')).strftime('%Y-%m-%dT%H:%M:%S')

    today = datetime.datetime.today()
    weekday_number = today.weekday()
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    est_timezone = pytz.timezone('America/New_York')
    date_today = datetime.datetime.now(est_timezone)
    date_tomorrow = (date_today + datetime.timedelta(days=1)).date()
    date_today = date_today.date()


    # Default structured prompt
    default_prompt = (
        "Given a set of text which will be at the bottom of this request, can you identify the title of the event, "
        "the location of the event, and the start and end time of the event. Give the start time and end time "
        "in a 24 hour time format, with time only in hours and minutes. If there is no explicit end time "
        "given then guess the amount of time the event would take place, with it being in increments "
        "of 30 minutes to an hour. The end time also has to always be after the start time. "
        "Give the start and end date in YYYY-MM-DD format. " 
        "If a specific date in some formate of YYYY, MM, and DD then immeaditely use that date and format it in the YYYY-MM-DD format. "
        "If a specific date is NOT listed but a day of the week is listed, use the current day of the week as a base, which is " + days[weekday_number] + ", "
        "and then if the given weekday is the same as the current weekday, then simply use the current date in YYYY-MM-DD format. Otherwise "
        "find the next closest proceeding weekday and give its specific date in YYYY-MM-DD format. If key words such as next are used, increment the specific date by the amount of time listed, " +
        "i.e. stating 'next week' corresponds to 7 days later from the found date and 'next month' is the next month over on the same weekday. "
        "If there is no explicit date and no explicit weekday stated, assume that the start and end date are today, which is " + est_time +
        ". If the given start time listed is after our current date time of " + est_time +
        " use the current date of " + date_today + ", otherwise assume the start and end time occur on the next day which is " + date_tomorrow + 
        # "Always make sure the start and end date are the same day if no explicit end date was given."
        "Then output everything in the following format and don't include your reasoning:\nName=\nLocation=\nStartTime=\nEndTime=\nStartDate=\nEndDate=\n"
        "Here is the text I want you to analyze:\n"
    )

    #Analyzing text

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
