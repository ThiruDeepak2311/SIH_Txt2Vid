import requests
import json
import os
def GPT(text):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    }

    content = text
    data = {
        "prompt": f"[INST] {content} [/INST]\n",
        "model": "meta/llama-2-70b-chat",
        "systemPrompt": "You are a helpful assistant.",
        "temperature": 0.75,
        "topP": 0.9,
        "maxTokens": 800,
        "image": None,
        "audio": None,
    }

    while True:
        response = requests.post(
            url=os.environ['GPT_ENDPOINT'],  
            json=data,
            headers=headers,
        )

        # Check if the response is in JSON format
        try:
            json_response = response.json()
            return json_response
        except json.JSONDecodeError:
            print("Received response is not in JSON format. Retrying...")
            continue