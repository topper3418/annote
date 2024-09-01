# TODO: add commands for dev purposes
# who, besides you is going to use the cli interface long term anyway? 
# wipe tables
# show data from tables
# maybe even run sql queires? 

import argparse
from pprint import pprint
from typing import Optional
# from src.db.controller import create_entry, get_recent_entries_json
from src.db import Controller

def execute_command(command):
    print(f"Executing command: {command}")
    # Add logic to execute the command

def get_recent_entries_json(limit: int, search: Optional[str] = None):
    with Controller() as db:
        recent_entries = db.get_recent_entries(limit, search)
        return [entry.json() for entry in recent_entries]

def create_entry(text):
    with Controller() as db: 
        new_entry = db.create_entry(text)
        return new_entry.json()

def main():
    parser = argparse.ArgumentParser(description="Annote CLI App")

    # Flags for different actions
    parser.add_argument("-r", "--read", type=str, help="read notes, specify the limit, add a string to search")

    # Default note behavior
    parser.add_argument("default_note", nargs='*', help="Default note to record if no flags are used")

    args = parser.parse_args()

    if not any(vars(args).values()):
        print("TODO implement 'keepopen' later")
    else:
        if args.read:
            limit = args.read
            search = " ".join(args.default_note) if args.default_note else None
            entries = get_recent_entries_json(limit=limit, search=search)
            pprint(entries)
        else:
            entry = create_entry(" ".join(args.default_note))
            pprint(entry)


if __name__ == "__main__":
    main()
