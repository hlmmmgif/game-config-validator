import os
import requests
from dotenv import load_dotenv

load_dotenv()


def ask(question, system=None):
    key = os.environ["DEEPSEEK_API_KEY"]

    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": question})

    resp = requests.post(
        "https://api.deepseek.com/chat/completions",
        headers={
            "Authorization": "Bearer " + key,
            "Content-Type": "application/json",
        },
        json={
            "model": "deepseek-chat",
            "messages": messages,
        },
        timeout=30,
    )

    if resp.status_code != 200:
        raise RuntimeError(f"HTTP {resp.status_code}: {resp.text}")
    
    return resp.json()["choices"][0]["message"]["content"]
