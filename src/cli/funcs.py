from src.engine import associate_entry
from ..db import Controller
from pprint import pprint
import os


def print_info():
    print("Annote CLI App v0.5")

def create_entry(args):
    print(f"Creating note: {args.note}")
    with Controller() as db: 
        new_entry = db.create_entry(args.note)
        return new_entry.json()


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

def show_tasks(limit, search=None, focused=True):
    focus_state = "focused" if focused else "unfocused"
    print(f"Showing the latest {limit} {focus_state} tasks")
    if search:
        print(f"Filtering by: {search}")
    with Controller() as conn:
        tasks = conn.get_focused_task()
        pprint([task.json(recurse=2) for task in tasks])

def show(args):
    limit, search = args.limit, args.search
    if args.tasks:
        show_tasks(limit, search, args.focus)
    elif args.generations:
        show_generations(limit, search)
    else:
        show_entries(limit, search)

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
    elif args.cycle_next_entry:
        associate_entry()
    elif args.load:
        load_entries(args.load)

    


