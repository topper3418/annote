from typing import List
import json
import ollama


def prompt_ollama(prompt: str, as_json: bool = True) -> str | dict:
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

class OllamaInteraction:

    def __init__(self, prompt, response):
        self.prompt = prompt
        self.repsonse = response


class OllamaProcessor:
    
    def __init__(self,
                 prompt_template,
                 output_schema,
                 subject, 
                 context):
        self.prompt_template = prompt_template
        self.output_schema = output_schema
        self.subject = subject
        self.context = context
        self.interactions: List[OllamaInteraction] = []

    def initial_prompt(self):
        prompt = self.prompt_template.format(
                subject=self.subject,
                context=self.context
        )
        response = prompt_ollama(prompt, as_json=False)
        self.interactions.append(OllamaInteraction(prompt=prompt, response=response))

    def formatting_prompt(self):
        pass
    
    
