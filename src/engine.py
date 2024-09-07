import os
import traceback
import json
from pprint import pprint
from typing import Tuple, List

from src.db.map import Action, Entry, Session, Task
from .ollama.controller import attempt_to_fix_entry_processing, process_entry
from .ollama.prompt import prompt_ollama
from .db import Controller

# the idea is to make it organized, but just prompt in a reasonable way

# give entry and task for context

# ask it in plain english to list off potential actions and new tasks from a prompt

# ask it to shove it into a format

# if there is an error, show it what it did wrong and request it fix it. 

# finally return the structured response. 


get_tasks_prompt = """\
you are responsible for interpreting the ramblings of a user into an 
organized notebook. To this end you will view a short note they take
in the context of a task they are undertaking. Sometimes the note will
be related, sometimes the note will be about something different. I want
to know: what new tasks (or subtasks of tasks shown here) are implied by 
this note, if any? Is a start or end time implied or given? Please respond
with detail and in list format.

TASK: 
{task}

ENTRY:
{entry}"""


format_tasks_prompt = """\
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

CONTEXT TASK: 
{task}

TASKS AND SUBTASKS:
{prev_response}"""


get_annotations_prompt = """\
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


format_annotations_prompt = """\
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
        self.controller = Controller

    def bind(self, session):
        """binds the objects to a session again"""
        pass

    def _verify_session(self):
        """verifies the objects are attached to a session"""
        pass

    def jsonify(self, entry_recurse=0, task_recurse=1):
        self._verify_session()
        return self.entry.json(recurse=entry_recurse), self.task.json(recurse=task_recurse)


def get_subtasks(entry_json: dict, task_json: dict):
    extract_prompt = get_tasks_prompt.format(
        task=json.dumps(task_json, indent=4),
        entry=json.dumps(entry_json, indent=4)
    )
    tasks_unformatted = prompt_ollama(extract_prompt, as_json=False)
    print(tasks_unformatted)
    # continue developing this


def get_annotations(entry_json: dict, task_json: dict):
    pass



def annotate(entry_id, task_id):
    """This will take an entry and a task and generate a series of new subtasks and notes"""
    # first ask it for any tasks and subtasks that can be inferred from the entry
    # get_tasks = get_tasks_prompt.format(
    # tasks_english = prompt_ollama(
    # OK so this should be the plan: 
    # 1) take the actions of getting the tasks and getting the annotations and 
    #    split them up, so that they can be tested and worked on individually
    # 2) work this into the cli so that testing can be nice and easy
    pass
    


