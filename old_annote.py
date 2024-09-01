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

def parse():
    parser = argparse.ArgumentParser(description="Annote CLI tool with subcommands")
    
    # Create a subparser object
    subparsers = parser.add_subparsers(dest='command', help='Subcommands')

    # Subparser for 'create' command
    parser_create = subparsers.add_parser('create', help='Create a new note')
    parser_create.add_argument('note', type=str, help='The content of the note')

    # Subparser for 'read' command
    parser_read = subparsers.add_parser('read', help='Read notes')
    parser_read.add_argument('query', type=str, nargs='?', help='Optional query to filter notes')

    # Parse arguments
    args, unknown = parser.parse_known_args()

    # If no command is provided, assume 'create'
    if args.command is None and unknown:
        args.command = 'create'
        args.note = " ".join(unknown)

    return args

def main():
    args = parse()
    
    print(f'command: {args.command}')

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
