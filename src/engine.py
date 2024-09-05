import os
import traceback
from pprint import pprint
from typing import Tuple, List

from src.db.map import Action, Entry, Task
from .ollama.controller import attempt_to_fix_entry_processing, process_entry
from .db import Controller

# the idea is to make it organized, but just prompt in a reasonable way

# give entry and task for context

# ask it in plain english to list off potential actions and new tasks from a prompt

# ask it to shove it into a format

# if there is an error, show it what it did wrong and request it fix it. 

# finally return the structured response. 



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

    
    
