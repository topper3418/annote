from typing import List
import json
import ollama


def prompt_ollama(prompt: str, as_json: bool = True, temperature: int = 0) -> str | dict:
    response = ollama.generate(
        prompt=prompt,
        format='json' if as_json else '',
        model='llama3.1',
        options={ 'temperature': temperature },
        stream=False
    )
    response_text = response.get('response', '')
    if as_json:
        return json.loads(response_text)
    else:
        return response_text

