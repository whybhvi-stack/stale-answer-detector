import os, json, re
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

# Always read the .env file in the main project folder, wherever we run from
load_dotenv(Path(__file__).resolve().parent.parent / ".env", override=True)

client = OpenAI(
    base_url=os.getenv("BIFROST_BASE_URL"),
    api_key="dummy",
    default_headers={"x-bf-vk": os.getenv("BIFROST_VIRTUAL_KEY")},
)

def ask(model, system, user):
    if not model or "/" not in model:
        raise ValueError(
            f"Model name is '{model}'. Check CHEAP_MODEL and STRONG_MODEL in .env "
            "(format: provider/model, e.g. openrouter/openai/gpt-4o-mini)"
        )
    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        temperature=0,
        max_tokens=800,
    )
    return resp.choices[0].message.content

def ask_json(model, system, user):
    text = ask(model, system, user)
    text = re.sub(r"```json|```", "", text).strip()
    return json.loads(text)

if __name__ == "__main__":
    print(ask(os.getenv("CHEAP_MODEL"), "You are helpful.", "Say hello in 5 words."))