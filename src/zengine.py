import json
from pprint import pprint
from typing import List, Optional

from src.db.map import Entry, Task
from .ollama.prompt import prompt_ollama
from .db import Controller


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


get_annotations_prompt_template = """\
you are in charge of interpreting the ramblings of a user into an 
organized notebook. To this end you will view a short note they take
in the context of a task they are undertaking. Sometimes the note will
be related, sometimes the note will be about something different. I want
to know: Does this note relate to the task or any of its subtasks? if so, 
how? Please respond with detail and in list format. 

TASK: 
{task}

ENTRY:
{entry}"""


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

class AnnotationContext:
    def __init__(self, entry: Entry, task: Task):
        self.entry = entry
        self.task = task

    def bind(self, session):
        """binds the objects to a session again"""
        self.entry = session.merge(self.entry)
        self.task = session.merge(self.task)

    def _verify_session(self):
        """verifies the objects are attached to a session"""
        pass

    def jsonify(self, entry_recurse=0, task_recurse=1):
        self._verify_session()
        return self.entry.json(recurse=entry_recurse), self.task.json(recurse=task_recurse)


# TODO: run these on linux and actually test. also hook up to cli
def get_subtasks(entry_json: dict, task_json: dict) -> dict:
    extract_prompt = get_tasks_prompt_template.format(
        task=json.dumps(task_json, indent=4) if task_json is not None else "No context provided",
        entry=json.dumps(entry_json, indent=4)
    )
    print('PROMPTING MODEL FOR ORGANIC RETURN:')#\n\n')
    print(extract_prompt)
    # print('\n\n\n')
    tasks_and_subtasks_unformatted = prompt_ollama(extract_prompt, as_json=False)
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
    tasks_and_subtasks = prompt_ollama(format_prompt)
    print('RESULTS:')#\n\n')
    # print('\n\n\n\n')
    pprint(tasks_and_subtasks)
    return tasks_and_subtasks


def get_annotations(entry_json: dict, task_json: dict):
    extract_prompt = get_annotations_prompt_template.format(
            task=task_json,
            entry=entry_json
    )
    annotations_unformatted = prompt_ollama(extract_prompt, as_json=False)
    format_prompt = format_annotations_prompt_template.format(
        task=json.dumps(task_json, indent=4),
        prev_response=annotations_unformatted
    )
    annotations = prompt_ollama(format_prompt)
    pprint(annotations)
    return annotations


def annotate(entry: Entry, task: Optional[Task] = None):
    """This will take an entry and a task and generate a series of new subtasks and notes"""
    entry_json = entry.json()
    task_json = task.json(recurse=1) if task is not None else None
    subtask_dict = get_subtasks(entry_json, task_json)

    print('wow you actually made it')


def cycle_next_entry():
    with Controller() as conn: 
        task = conn.get_focused_task()
        target_entry_id = conn.get_latest_generated_entry_id() or 0 + 1
        entry = conn.get_entry(target_entry_id)
        if entry is None:
            print('Entries have all been processed')
            return
    new_tasks = annotate(entry, task)
    with Controller() as conn: 










