import json
from pprint import pprint
from typing import Optional, Tuple, List

from src.db.map import Entry, Generation, Task
from ..ollama.prompt import prompt_ollama, prompt_ollama_json
from ..db import Controller
from .util import get_extraction_context


PROCESS_NAME = 'extract_tasks'


get_tasks_prompt_template = """\
you are responsible for interpreting the ramblings of a user into an organized notebook. To this end you will view a short note they take in the context of a task they are undertaking. Sometimes the note will be related, sometimes the note will be about something different. I want to know: what new tasks (or subtasks of tasks shown here) are implied by this note, if any? Is a start or end time implied or given?

TASK FOR CONTEXT: 
{task}

ENTRY:
{entry}

Please respond in sentences with one sentence per new task or subtask. Please do not include any duplicates from the context task. If the new task is a subtask of any of the context tasks, it should be mentioned in the sentence. 
"""


format_tasks_prompt_template = """\
you are responsible for taking a list of tasks and subtasks and putting it into
a json format for easy computation. These tasks and subtasks may or may not be
related to an entry provided for context. 

Here is the schema for how I would like you to return the data:

// this is the object you will return each time
interface response {{
    tasks: task[];  // it is okay to return an empty array if there are no tasks given
}}

interface task {{
    text: string; // a concise string representing the task
    parentName?: string; // the name of the task that is the parent of this one, if applicable.
    start?: string; // string in the format of "%m/%d/%y %H:%M" estimating the start time of the task, if applicable
    end?: string; // string in the format of "%m/%d/%y %H:%M" estimating the end time of the task, if applicable
    children?: task[]; // a list of subtasks, if applicable. same shape as this task object, but parent will be implied so do not include it
    focus: boolean; // does this seem like something the user intends to put effort or thought into in the immediate future?
}}    

TASK FOR CONTEXT: 
{task}

TASKS AND SUBTASKS:
{prev_response}

Please respond only in json and do not duplicate any of the tasks or subtasks given for context, except to call them out as the parent for new tasks. I repeat, do not include anything in the task for context in your response besides filling out the parentName field. 
"""


def get_subtasks(entry_json: dict, task_json: dict) -> dict:
    extract_prompt = get_tasks_prompt_template.format(
        task=json.dumps(task_json, indent=4) if task_json is not None else "No context provided",
        entry=json.dumps(entry_json, indent=4)
    )
    print('PROMPTING MODEL FOR ORGANIC RETURN:')#\n\n')
    print(extract_prompt)
    # print('\n\n\n')
    tasks_and_subtasks_unformatted = prompt_ollama(extract_prompt)
    print('RESULTS:')#\n\n')
    pprint(tasks_and_subtasks_unformatted)
    # print('\n\n\n\n')
    format_prompt = format_tasks_prompt_template.format(
        task=json.dumps(task_json, indent=4),
        prev_response=tasks_and_subtasks_unformatted
    )
    print('PROMPTING MODEL FOR STRUCTURED RETURN:')#\n\n')
    print(format_prompt)
    # print('\n\n\n')
    tasks_and_subtasks = prompt_ollama_json(format_prompt)
    print('RESULTS:')#\n\n')
    # print('\n\n\n\n')
    pprint(tasks_and_subtasks)
    return tasks_and_subtasks


# def get_extraction_context(conn: Controller) -> Tuple[Task | None, Entry | None]:
#     task = conn.get_focused_task()
#     target_entry_id = conn.get_latest_generated_entry_id(process_name=PROCESS_NAME) or 0 + 1
#     entry = conn.get_entry(target_entry_id)
#     return task, entry


def create_tasks(conn: Controller, task_dict: dict, entry: Entry) -> Tuple[List[Task], Generation]:
    # record the response
    generation = conn.create_generation(
            entry=entry,
            process=PROCESS_NAME,
            data=task_dict,
    )
    # unpack the response and generate actions and tasks
    new_tasks = task_dict.get('tasks', [])
    new_task_objects = []
    for task_dict in new_tasks:
        # if it gives a parent id, check that. 
        parent_name = task_dict.get('parentName')
        if parent_name:
            parent = conn.search_task(parent_name)
        else:
            parent = None

        # create the task
        task = conn.create_task(
                task_dict=task_dict,
                parent=parent,
                source=entry
        )
        new_task_objects.append(task)
    return new_task_objects, generation
    

def get_tasks_from_next_entry():
    with Controller() as conn: 
        task, entry = get_extraction_context(conn, PROCESS_NAME)
        if entry is None: 
            print("all entries processed")
            return
        task_json = task.json(recurse=1) if task is not None else {}
        entry_json = entry.json()
    tasks_and_subtasks = get_subtasks(entry_json, task_json)
    with Controller() as conn: 
        new_tasks, generation = create_tasks(
                conn, 
                tasks_and_subtasks, 
                entry, 
        )
        new_tasks_json = [task.json(recurse=1) for task in new_tasks]
        generation_json = generation.json()
    print("SUCCESSFULLY CREATED NEW TASKS AND SUBTASKS")
    pprint(new_tasks_json)
    pprint(generation_json)









