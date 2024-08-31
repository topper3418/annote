from pprint import pprint

from src.db.map import Action, Task
from .ollama.controller import process_entry
from .db import Controller

def associate_entry():
    """cycles the entry processor once. it
    1) checks to see if there are any entries in need of processing for the main annotation loop
    2) if there are, take the currently focused tasks and check its relevance against them
    3) generate and store new tasks and actions based on the entry and the context
    4) create and store a generation object to save data about this cycle"""
    with Controller() as conn:
        # figure out what the latest entry is to have been generated for
        gen_cursor = conn.get_latest_generated_entry_id()
        if gen_cursor is not None:
            print(f'latest entry id generated: {gen_cursor}')
            # if it's the latest entry, we don't need to look for the next
            needs_generation = not conn.is_latest_entry(gen_cursor)
            if not needs_generation:
                print('matches latest entry id')
                return
            # set the cursor
            gen_cursor += 1
        else:
            gen_cursor = 1
        
        next_entry = conn.get_entry(gen_cursor)
        
        # handles a case with no entries
        if next_entry is None:
            print('no entries found, terminating')
            return
        
        # context for the entry
        focused_tasks = conn.get_focused_tasks()

        # convert to json for the generation
        next_entry_json = next_entry.json()
        focused_tasks = [task.json(recurse=2) for task in focused_tasks]

    # release the db connection and prompt the model
    response = process_entry(next_entry_json, focused_tasks)

    with Controller() as conn:
        # record the response
        generation = conn.create_generation(
                entry=next_entry,
                process='associate_entry',
                data=response,
        )
        pprint(generation.json())

        # unpack the response and generate actions and tasks
        new_tasks = response.get('tasks', [])
        new_tasks_json = []
        for task_dict in new_tasks:
            # if it gives a parent id, check that. 
            parent_id = task_dict.get('parentId')
            if parent_id:
                parent = conn.get_task(parent_id)
            else:
                parent = None

            # create the task
            task = conn.create_task(
                    task_dict=task_dict,
                    parent=parent,
                    source=next_entry
            )
            new_tasks_json.append(task.json(recurse=1))
        
        # if no context, no actions. ignore the rest
        new_actions_json = []
        if focused_tasks: 
            new_actions = response.get('actions', [])
            for action_dict in new_actions:
                # it has to be linking a task id, so check it
                task = conn.get_task(action_dict.get('taskId'))
                if not task:
                    print(f'ERROR: failed to get task for action: {action_dict}')
                    continue
                action = conn.create_action(
                        action=action_dict.get('action'),
                        task=task,
                        entry=next_entry
                )
                new_actions_json.append(action.json(recurse=1))

    print('\n\n\n\nPROCESSING COMPLETE\n\n\nRESULTS:\n\n')
    pprint({'new_actions': new_actions_json, 'new_tasks': new_tasks_json})
            
            
        

    
    
