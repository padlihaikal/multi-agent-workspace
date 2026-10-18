import os
from dotenv import load_dotenv
from openai import OpenAI
import time

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

MODEL = "openai/gpt-oss-20b"
MAX_RETRIES = 3

def ask(system_prompt: str, user_prompt: str) -> str:
    for attempt in range(MAX_RETRIES):
        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            if attempt == MAX_RETRIES -1:
                raise
                
            print(f"ask failed ({attempt + 1}/{MAX_RETRIES}), retrying")
            time.sleep(1)

if __name__ == "__main__":
    print(ask("You are a helpful assistant.", "Say hello in one sentence."))