from pprint import pprint
from .ollama.controller import process_entry
from .db import Controller

def cycle_entry_processor():
    """cycles the entry processor once. it
    1) checks to see if there are any entries in need of processing for the main annotation loop
    2) if there are, take the currently focused tasks and check its relevance against them
    3) generate and store new tasks and actions based on the entry and the context
    4) create and store a generation object to save data about this cycle"""
    with Controller() as conn:
        gen_cursor = conn.get_latest_generated_entry_id()
        needs_generation = not conn.is_latest_entry(gen_cursor)

        if not needs_generation:
            return

        gen_cursor += 1

        next_entry = conn.get_entry(gen_cursor)
        focused_tasks = conn.get_focused_tasks()

        next_entry = next_entry.json()
        focused_tasks = [task.json(recurse=2) for task in focused_tasks]

    response = process_entry(next_entry, focused_tasks)
    pprint(response)

    
    
