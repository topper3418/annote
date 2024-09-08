from typing import List
import json
import ollama


def prompt_ollama(prompt: str, temperature: int = 0) -> str:
    response = ollama.generate(
        prompt=prompt,
        model='llama3.1',
        options={ 'temperature': temperature },
        stream=False
    )
    response_text = response.get('response', '')
    return response_text


def prompt_ollama_json(prompt: str, temperature: int = 0) -> dict:
    response = ollama.generate(
        prompt=prompt,
        format='json',
        model='llama3.1',
        options={ 'temperature': temperature },
        stream=False
    )
    response_text = response.get('response', '')
    return json.loads(response_text)






