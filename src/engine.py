import os
import traceback
import json
from pprint import pprint
from typing import Tuple, List

from src.db.map import Action, Entry, Task
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


def get_subtasks(entry_id, task_id):
    with Controller() as conn:
        entry=conn.get_entry(entry_id)
        if entry is None:
            raise Exception(f'no entry found matching id {entry_id}')
        task=conn.get_task(task_id)
        if task is None:
            raise Exception(f'no task found matching id {task_id}')
        entry_json = entry.json(recurse=1)
        task_json = task.json(recurse=1)
    extract_prompt = get_tasks_prompt.format(
        task=json.dumps(task_json, indent=4),
        entry=json.dumps(entry_json, indent=4)
    )
    tasks_unformatted = prompt_ollama(extract_prompt, as_json=False)
    print(tasks_unformatted)


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
    


class EntryAssociationContext:
    """just a helper data focused class for cleaning up this script"""
    def __init__(self):
        self.entry: Entry | None = None
        self.context: List[Task] = []
        self.entry_json: dict = {}
        self.context_json: List[dict] = []

    def get_json(self):
        if self.entry is None:
            raise Exception('attempted to get json when there was no entry attached')
        # make sure we are connected to a session
        if not self.entry.is_connected_to_session():
            raise Exception('attempted to get json when session is disconnected')
        self.entry_json = self.entry.json()
        self.context_json = [task.json(recurse=2, suppress=['actions']) for task in self.context]
        


    

def get_entry_association_context() -> EntryAssociationContext:
    context = EntryAssociationContext()
    with Controller() as conn:
        # figure out what the latest entry is to have been generated for
        gen_cursor = conn.get_latest_generated_entry_id()
        if gen_cursor is not None:
            print(f'latest entry id generated: {gen_cursor}')
            # if it's the latest entry, we don't need to look for the next
            needs_generation = not conn.is_latest_entry(gen_cursor)
            if not needs_generation:
                print('no new entries found, terminating')
                return context
            # set the cursor
            gen_cursor += 1
        else:
            gen_cursor = 1
        
        context.entry = conn.get_entry(gen_cursor)
        
        # handles a case with no entries
        if context.entry is None:
            print('no entries found, terminating')
            return context
        
        # context for the entry
        context.context = conn.get_focused_task()

        # convert to json for the generation
        context.get_json()
    return context


def create_objects_from_ollama_response(response: dict, context: EntryAssociationContext):
    # ensure the context is populated
    if context.entry is None:
        raise Exception('no entry provided for the context')
    with Controller() as conn:
        # record the response
        generation = conn.create_generation(
                entry=context.entry,
                process='associate_entry',
                data=response,
        )

        print("\nGeneration results: \n\n")
        pprint(generation.json())

        # unpack the response and generate actions and tasks
        new_tasks = response.get('tasks', [])
        print('DEBUG, NEW TASKS: ')
        pprint(new_tasks)
        new_tasks_json = []
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
                    source=context.entry
            )
            new_tasks_json.append(task.json(recurse=1))
        
        # if no context, no actions. ignore the rest
        new_actions_json = []
        if context.context_json: 
            new_actions = response.get('actions', [])
            for action_dict in new_actions:
                # it has to be linking a task id, so check it
                task = conn.search_task(action_dict.get('taskName'))
                if not task:
                    print(f'ERROR: failed to get task for action: {action_dict}')
                    continue
                action = conn.create_action(
                        action=action_dict.get('action'),
                        task=task,
                        entry=context.entry
                )
                new_actions_json.append(action.json(recurse=1))

    print('\n\n\n\nPROCESSING COMPLETE\n\n\nRESULTS:\n\n')
    pprint({'new_actions': new_actions_json, 'new_tasks': new_tasks_json})



def associate_entry():
    """cycles the entry processor once. it
    1) checks to see if there are any entries in need of processing for the main annotation loop
    2) if there are, take the currently focused tasks and check its relevance against them
    3) generate and store new tasks and actions based on the entry and the context
    4) create and store a generation object to save data about this cycle"""
    context = get_entry_association_context()

    if context.entry is None:
        return

    response = process_entry(context.entry_json, context.context_json)
    if 'response' in response:
        response = response.get('response', {})
    

    try:
        create_objects_from_ollama_response(response, context)
        return
    except Exception as e:
        print("EXCEPTION CAUGHT AND STOPPED PLEASE SEE data/exceptiondump.txt FOR LOGS")
        stack_trace = traceback.format_exc()
    with open(os.path.join('data', 'exceptiondump.txt'), mode='a') as f:
        f.write(stack_trace)
    second_response = attempt_to_fix_entry_processing(context.entry_json,
                                                      context.context_json,
                                                      response,
                                                      stack_trace)
    create_objects_from_ollama_response(second_response, context)

    
    
