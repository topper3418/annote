import argparse
from src.db.controller import create_entry



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

    if not any(vars(args).values()):
        print("TODO implement 'keepopen' later")
    else:
        if args.add_note:
            create_entry(' '.join(args.default_note))
        if args.add_command:
            execute_command(args.add_command)


if __name__ == "__main__":
    main()
