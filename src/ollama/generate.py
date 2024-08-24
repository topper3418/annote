from typing import List
from datetime import datetime
import json

import ollama

# configuration values
OLLAMA_MODEL = 'llama3.1'


plan_generation_intro = """\
Respond to the following prompt using a json structure only. The prompt will be a plan that may be 
in the first person, e.g. I should do this, or we need to do that. Please extract a list of tasks
from the prompt and return them in the following shape: 
{
    tasks: [{
        text: "a concise string representing the task",
        start: "string in the format of YYYY-MM-DD HH:MM estimating the start time of the task",
        end: "string in the format of YYYY-MM-DD HH:MM estimating the end time of the task",
        children: [a list of subtasks, if applicable]
    }]
}

Here is the prompt:

"""

class GenerationError(Exception):
    pass

def parse_time(time_str: str) -> datetime:
    try:
        return datetime.strptime(time_str, "%Y-%m-%d %H:%M")
    except Exception as e:
        raise GenerationError(f'Error parsing time string given, expected "%Y-%m-%d %H:%M" but got {time_str}')


def generate_tasks(prompt: str) -> List[dict]:
    response = ollama.generate(
        prompt=plan_generation_intro + prompt,
        format='json',
        model=OLLAMA_MODEL,
        options={ 'temperature': 0 },
        stream=False
    )
    def clean_task(task_dict: dict) -> dict:
        new_dict = task_dict.copy()
        new_dict['start'] = parse_time(task_dict['start'])
        new_dict['end'] = parse_time(task_dict['end'])
        new_dict['children'] = [clean_task(child) for child in task_dict.get('children', [])]
        return new_dict
    parsed_response = json.loads(response['response'])
    tasks = parsed_response.get('tasks')
    return [clean_task(task) for task in tasks]
