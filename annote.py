import argparse
from pprint import pprint
from src.db.controller import create_entry, get_recent_entries_json

def execute_command(command):
    print(f"Executing command: {command}")
    # Add logic to execute the command

def main():
    parser = argparse.ArgumentParser(description="Annote CLI App")

    # Flags for different actions
    parser.add_argument("-c", "--command", type=str, help="Execute a command")
    parser.add_argument("-r", "--read", type=str, help="read notes, specify the limit, add a string to search")

    # Default note behavior
    parser.add_argument("default_note", nargs='*', help="Default note to record if no flags are used")

    args = parser.parse_args()

    if not any(vars(args).values()):
        print("TODO implement 'keepopen' later")
    else:
        if args.command:
            execute_command(args.add_command)
        elif args.read:
            limit = args.read
            entries = get_recent_entries_json(limit=limit, search=" ".join(args.default_note))
            pprint(entries)
        else:
            create_entry(" ".join(args.default_note))


if __name__ == "__main__":
    main()
