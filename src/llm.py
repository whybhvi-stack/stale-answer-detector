import os, json, re
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(
    base_url=os.getenv("BIFROST_BASE_URL"),
    api_key="dummy",
    default_headers={"x-bf-vk": os.getenv("BIFROST_VIRTUAL_KEY")},
)
def ask(model, system, user):
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