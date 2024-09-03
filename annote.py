#!/usr/bin/env python3
import argparse
import os
from pprint import pprint
from src.db import Controller
from src.engine import associate_entry

def print_info():
    print("Annote CLI App v1.0")

def create_entry(note):
    print(f"Creating note: {note}")
    with Controller() as db: 
        new_entry = db.create_entry(note)
        return new_entry.json()

def load_entries(filename):
    filepath = os.path.join('data', filename)
    print(f"loading entries from {filepath}")
    with open(filepath, r) as file:
        entries = file.readlines()
    with Controller() as db:
        new_entries = [db.create_entry(entry) for entry in entries]
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
        tasks = conn.get_focused_tasks()
        pprint([task.json(recurse=2) for task in tasks])

def flush_annotations():
    confirm = input("Are you sure you want to wipe all tables besides entries? Type 'yes' to confirm: ")
    if confirm.lower() == 'yes':
        print("Flushing annotations...")
        with Controller() as conn:
            conn.reset_annotations()
        print("done")
    else:
        print("Operation canceled.")

def run_command(command):
    print(f"Running command: {command}")
    # Logic to run a command

def main():
    parser = argparse.ArgumentParser(description="Annote CLI App")
    subparsers = parser.add_subparsers(dest="subcommand", help="Subcommand to run")

    # Print program info
    parser_info = subparsers.add_parser("annote", help="Print program info")

    # Create a note
    parser_create = subparsers.add_parser("note", help="Create a note")
    parser_create.add_argument("note", help="The note content")

    # Query related subcommands
    parser_query = subparsers.add_parser("query", help="Query entries, generations, or tasks")
    parser_query.add_argument("-l", type=int, help="Limit the number of results", default=50)
    parser_query.add_argument("-s", help="Search filter")
    
    parser_query.add_argument("-g", action="store_true", help="Query generations")
    parser_query.add_argument("-t", action="store_true", help="Query tasks")
    parser_query.add_argument("-f", type=str, choices=["true", "false"], help="Filter focused tasks", default="true")

    # dev related subcommands
    parser_dev = subparsers.add_parser("dev", help="Misc dev utilities")
    parser_dev.add_argument("--flush-annotations", action="store_true", help="Flush all annotations")
    parser_dev.add_argument("--cycle-next-entry", action="store_true", help="Cycle the engine once")
    parser_dev.add_argument("--load", '-l', action="store_true", help="upload a list of \\n-separated entries to the db")

    # Run a command
    parser_command = subparsers.add_parser("command", help="Run a command")
    parser_command.add_argument("command", help="The command to run")

    args = parser.parse_args()

    if args.subcommand == "annote":
        print_info()
    elif args.subcommand == "note":
        create_entry(args.note)
    elif args.subcommand == "query":
        limit = args.l
        search = args.s
        if args.g:
            show_generations(limit, search)
        elif args.t:
            focused = args.f == "true"
            show_tasks(limit, search, focused)
        else:
            show_entries(limit, search)
    elif args.subcommand == "dev":
        if args.flush_annotations:
            flush_annotations()
        elif args.cycle_next_entry:
            associate_entry()
        elif args.load:
            
            load_entries()
    elif args.subcommand == "command":
        run_command(args.command)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

