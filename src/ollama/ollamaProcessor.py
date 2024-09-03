import ollama


def prompt_ollama(prompt: str, json: bool = True) -> str:
    return ollama.generate(
        prompt=prompt,
        format='json' if json else '',
        model='llama3.1',
        options={ 'temperature': 0 },
        stream=False
    )


# class OllamaProcessor:
#     """two stage processing, takes in an output schema, 
#     prompt_func = prompt_ollama
#     
#     
#     def process_entry(self, entry: str, context):
#         prompt = 
