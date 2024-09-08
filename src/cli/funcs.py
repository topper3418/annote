from src.engine import cycle_task_extraction
from ..db import Controller
from pprint import pprint
import os


def print_info():
    print("Annote CLI App v0.5")

def create_entry(args):
    print(f"Creating note: {args.note}")
    with Controller() as db: 
        parent = db.get_task(args.context_id) if args.context_id else None
        new_entry = db.create_entry(args.note, context=parent)
        return new_entry.json()

def create_task(args):
    print(f"Creating task: {args.task}")
    with Controller() as conn:
        parent = conn.get_task(args.parent_id) if args.parent_id else None
        new_task = conn.create_task({"text": args.task,
                                     "focus": args.focus},
                                    parent=parent)
        return new_task.json()

def load_entries(filename):
    filepath = os.path.join('data', filename)
    print(f"loading entries from {filepath}")
    with open(filepath, 'r') as file:
        entries = file.readlines()
    with Controller() as db:
        new_entries = [db.create_entry(entry.strip('\n')) for entry in entries]
        entries_json = [entry.json() for entry in new_entries]
    pprint(entries_json)

def show_entries(limit, search=None):
    print(f"Showing the latest {limit} entries")
    if search:
        print(f"Filtering by: {search}")
    with Controller() as db:
        recent_entries = db.get_recent_entries(limit, search)
        entries_json = [entry.json() for entry in recent_entries]
    pprint(entries_json)

def show_generations(limit, search=None):
    print(f"Showing the latest {limit} generations")
    if search:
        print(f"Filtering by: {search}")
    with Controller() as conn:
        generations = conn.get_generations()
        pprint([generation.json(recurse=1) for generation in generations])

def show_tasks(limit, search=None, task_id=None, offset=0):
    print(f"Showing {limit} top-level tasks")
    with Controller() as conn:
        if task_id:
            print(f"getting task by id {task_id}")
            task = conn.get_task(task_id)
        elif search:
            print(f'searching for task with search "{search}"')
            task = conn.search_task(search_str=search)
        else:
            task = conn.get_top_level_tasks(limit=limit, offset=offset)
        if task is None:
            print("No task found")
        elif isinstance(task, list):
            pprint([task_inst.json(recurse=2) for task_inst in task])
        else:
            pprint(task.json(recurse=2))

def show(args):
    if args.tasks:
        show_tasks(args.limit, 
                   args.search, 
                   task_id=args.id,
                   offset=args.offset)
    elif args.generations:
        show_generations(args.limit, args.search)
    else:
        show_entries(args.limit, args.search)

def flush_annotations():
    confirm = input("Are you sure you want to wipe all tables besides entries? Type 'yes' to confirm: ")
    if confirm.lower() == 'yes':
        print("Flushing annotations...")
        with Controller() as conn:
            conn.reset_annotations()
        print("done")
    else:
        print("Operation canceled.")

def delete_database():
    confirm = input("Are you sure you want to delete the database? Type 'yes' to confirm: ")
    if confirm.lower() == 'yes':
        print("deleting database...")
        Controller.wipe_database()
        print("done")
    else:
        print("Operation canceled.")

def route_dev_command(args):
    if args.flush_annotations:
        flush_annotations()
    elif args.delete_database:
        delete_database()
    elif args.cycle_task_extraction:
        cycle_task_extraction()
    elif args.load:
        load_entries(args.load)

    


