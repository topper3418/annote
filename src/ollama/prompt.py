from typing import List
import json
import ollama


def prompt(prompt: str, as_json: bool = True) -> str | dict:
    response = ollama.generate(
        prompt=prompt,
        format='json' if json else '',
        model='llama3.1',
        options={ 'temperature': 0 },
        stream=False
    )
    response_text = response.get('response', '')
    if as_json:
        return json.loads(response_text)
    else:
        return response_text

