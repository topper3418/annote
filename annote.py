import argparse


def record_note(note):
    print(f"Recording note: {note}")
    message = create_note(note)
    print(message)

def execute_command(command):
    print(f"Executing command: {command}")
    # Add logic to execute the command

def main():
    parser = argparse.ArgumentParser(description="Annote CLI App")

    # Flags for different actions
    parser.add_argument("-c", "--command", type=str, help="Execute a command")

    # Default note behavior
    parser.add_argument("default_note", nargs='*', help="Default note to record if no flags are used")

    args = parser.parse_args()

    if args.command:
        execute_command(args.command)
    elif args.default_note:
        record_note(' '.join(args.default_note))
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
