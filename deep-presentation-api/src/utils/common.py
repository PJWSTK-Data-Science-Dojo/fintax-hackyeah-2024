import pathlib
from openai import OpenAI
import os

def get_ts_from_path(video_frame_file_path):
    return int(str(pathlib.Path(video_frame_file_path).stem).split("_")[1])

os.getenv("OPENAI_KEY")
client = OpenAI()
def llm_query(query: str, system: str = "You are a helpful assistant."):
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system},
            {
                "role": "user",
                "content": query
            }
        ]
    )
    return(completion.choices[0].message)