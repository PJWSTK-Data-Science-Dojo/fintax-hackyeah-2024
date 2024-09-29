import functools
import os

from dotenv import load_dotenv
import openai
from openai.types.chat import ChatCompletion


@functools.cache
def _get_openai_client():
    load_dotenv()
    return openai.OpenAI(
        api_key=os.environ.get("OPENAI_KEY"),
    )


def _extract_model_respone(completion: ChatCompletion) -> str:
    finish_reason = completion.choices[0].finish_reason

    if finish_reason == "stop":
        response: str | None = completion.choices[0].message.content
        if response:
            return response.strip()
        else:
            return ""
    else:
        print("Wraning: finish_reason is not 'stop'.")
        return ""


def extract_boolean_model_response(model_responce: str) -> bool:
    match model_responce:
        case "0":
            return False
        case "1":
            return True
        case _:
            print("Error the model did not return neither true or false. Counting that as false")
            return False


def get_openai_response(system_prompt: str, input: str, model: str="gpt-4o-mini") -> str:
    client = _get_openai_client()

    completion: ChatCompletion = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": f"Presentation excerpt: {input}" ,
            }
        ],
    )

    return _extract_model_respone(completion)
