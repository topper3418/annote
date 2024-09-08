import json
from pprint import pprint
from typing import Optional

from src.db.map import Entry, Task
from ..ollama.prompt import prompt_ollama, prompt_ollama_json
from ..db import Controller
from .util import get_extraction_context


get_annotations_prompt_template = """\
you are in charge of interpreting the ramblings of a user into an organized notebook. To this end you will view a short note they take in the context of a task they are undertaking. Sometimes the note will be related, sometimes the note will be about something different. I want to know: Does this note relate to the task or any of its subtasks in any of the following ways: 
 - Does it complete, pause or cancel any of them? 
 - Does it add context or any extra thoughts to any of them? 
 - Does it modify the start or end time of any of them? 
 
TASK: 
{task}

ENTRY:
{entry}

Please respond naturally in sentences, with one sentence per relation. """


format_annotations_prompt_template = """\
you are responsible for taking a list of annotations and putting it into
a json format for easy computation. These annotations will be relating 
a note taken by a user to a task (or its subtasks) they are supposed to 
be focusing on. 

Here is the schema for how I would like you to return the data:

// this is the object you will return each time
interface response {{
    actions?: action[];
}}

enum action_str {{
    begin = "begin",
    pause = "pause",
    complete = "complete",
    cancel = "cancel",
    note = "note"
}}

interface action {{
    action: action_str; // what does this entry seem to do to this task?
    taskName: string; // a string matching the name of the parent task it relates to. This cannot be any of the tasks returned, as those will automatically have a "create" action assigned to them. 
}}

CONTEXT TASK: 
{task}

LIST OF ACTIONS
{prev_response}"""



def get_annotations(entry_json: dict, task_json: dict):
    extract_prompt = get_annotations_prompt_template.format(
            task=task_json,
            entry=entry_json
    )
    print('PROMPTING MODEL FOR ORGANIC RETURN:')
    print(extract_prompt)
    annotations_unformatted = prompt_ollama(extract_prompt)
    print('RESULTS:')#\n\n')
    pprint(annotaions_unformatted)
    format_prompt = format_annotations_prompt_template.format(
        task=json.dumps(task_json, indent=4),
        prev_response=annotations_unformatted
    )
    print('PROMPTING MODEL FOR STRUCTURED RETURN:')#\n\n')
    print(format_prompt)
    annotations = prompt_ollama_json(format_prompt)
    print('RESULTS:')#\n\n')
    pprint(annotations)
    return annotations


def get_annotations_from_next_entry():



