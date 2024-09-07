#!/usr/bin/env python3
from src.cli import parse_and_run

if __name__ == "__main__":
    parse_and_run()

# def print_info():
#     print("Annote CLI App v0.5")
#
#
# def run_command(command):
#     print(f"Running command: {command}")
#     # Logic to run a command
#
# def main():
#     parser = argparse.ArgumentParser(description="Annote CLI App")
#     subparsers = parser.add_subparsers(dest="subcommand", help="Subcommand to run")
#
#     # Print program info
#     parser_info = subparsers.add_parser("annote", help="Print program info")
#     parser_info.set_defaults(func=print_info)
#
#     # Create a note
#     parser_create = subparsers.add_parser("note", help="Create a note")
#     parser_create.add_argument("note", help="The note content")
#     parser_create.set_defaults(func=create_entry)
#
#     # Query related subcommands
#     parser_query = subparsers.add_parser("query", help="Query entries, generations, or tasks")
#     parser_query.add_argument("-l", "--limit", type=int, help="Limit the number of results", default=50)
#     parser_query.add_argument("-s", "--search", help="Search filter")
#     
#     parser_query.add_argument("-g", "--generations", action="store_true", help="Query generations")
#     parser_query.add_argument("-t", "--tasks", action="store_true", help="Query tasks")
#     parser_query.add_argument("-f", "--focus", type=str, choices=["true", "false"], help="Filter focused tasks", default="true")
#     parser_query.set_defaults(func=show)
#
#     # dev related subcommands
#     parser_dev = subparsers.add_parser("dev", help="Misc dev utilities")
#     parser_dev.add_argument("--flush-annotations", action="store_true", help="Flush all annotations")
#     # TODO: make it so that this can be done with any database in the future
#     parser_dev.add_argument("--delete-database", action="store_true", help="Flush all annotations")
#     parser_dev.add_argument("--cycle-next-entry", action="store_true", help="Cycle the engine once")
#     parser_dev.add_argument("--load", '-l', type=str, help="upload a list of \\n-separated entries to the db")
#
#     # Run a command
#     parser_command = subparsers.add_parser("command", help="Run a command")
#     parser_command.add_argument("command", help="The command to run")
#
#     args = parser.parse_args()
#
#     if args.subcommand == "annote" or args.subcommand == "note" or args.subcommand == "query":
#         args.func(args)
#     elif args.subcommand == "dev":
#         if args.flush_annotations:
#             flush_annotations()
#         if args.delete_database:
#             delete_database()
#         elif args.cycle_next_entry:
#             associate_entry()
#         elif args.load:
#             load_entries(args.load)
#     elif args.subcommand == "command":
#         run_command(args.command)
#     else:
#         parser.print_help()
#
# if __name__ == "__main__":
#     main()
#
