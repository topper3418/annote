import argparse
from src.db import create_note
import os
import subprocess
import sys


def record_note(note):
    print(f"Recording note: {note}")
    message = create_note(note)
    print(message)

def execute_command(command):
    print(f"Executing command: {command}")
    # Add logic to execute the command

def create_tag(tag, description):
    print(f"Creating tag: {tag} with description: {description}")
    # Add logic to save the tag and description

def main():
    parser = argparse.ArgumentParser(description="Annote CLI App")

    # Flags for different actions
    parser.add_argument("-n", "--note", type=str, help="Record a note")
    parser.add_argument("-c", "--command", type=str, help="Execute a command")
    parser.add_argument("-t", "--tag", type=str, help="Create a tag")
    parser.add_argument("-d", "--description", type=str, help="Description for the tag")

    # Default note behavior
    parser.add_argument("default_note", nargs='*', help="Default note to record if no flags are used")

    args = parser.parse_args()

    if args.note:
        record_note(args.note)
    elif args.command:
        execute_command(args.command)
    elif args.tag:
        create_tag(args.tag, args.description)
    elif args.default_note:
        record_note(' '.join(args.default_note))
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
