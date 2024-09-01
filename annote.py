import argparse

def print_info():
    print("Annote CLI App v1.0")

def create_note(note):
    print(f"Creating note: {note}")
    # Logic to create a note in the database

def show_entries(limit, search=None):
    print(f"Showing the latest {limit} entries")
    if search:
        print(f"Filtering by: {search}")
    # Logic to query entries from the database

def show_generations(limit, search=None):
    print(f"Showing the latest {limit} generations")
    if search:
        print(f"Filtering by: {search}")
    # Logic to query generations from the database

def show_tasks(limit, search=None, focused=True):
    focus_state = "focused" if focused else "unfocused"
    print(f"Showing the latest {limit} {focus_state} tasks")
    if search:
        print(f"Filtering by: {search}")
    # Logic to query tasks from the database

def flush_annotations():
    confirm = input("Are you sure you want to wipe all tables besides entries? Type 'yes' to confirm: ")
    if confirm.lower() == 'yes':
        print("Flushing annotations...")
        # Logic to wipe annotations tables
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

    # Delete related subcommands
    parser_delete = subparsers.add_parser("delete", help="Delete annotations")
    parser_delete.add_argument("--flush-annotations", action="store_true", help="Flush all annotations")

    # Run a command
    parser_command = subparsers.add_parser("command", help="Run a command")
    parser_command.add_argument("command", help="The command to run")

    args = parser.parse_args()

    if args.subcommand == "annote":
        print_info()
    elif args.subcommand == "note":
        create_note(args.note)
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
    elif args.subcommand == "delete" and args.flush_annotations:
        flush_annotations()
    elif args.subcommand == "command":
        run_command(args.command)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

