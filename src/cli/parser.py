import argparse
from .funcs import print_info, create_entry, show, route_dev_command, create_task

parser = argparse.ArgumentParser(description="Annote CLI App")
subparsers = parser.add_subparsers(dest="subcommand", help="Subcommand to run")

# Print program info
parser_info = subparsers.add_parser("annote", help="Print program info")
parser_info.set_defaults(func=print_info)

# Create a note
parser_create_entry = subparsers.add_parser("note", help="Create a note")
parser_create_entry.add_argument("note", help="The note content")
parser_create_entry.set_defaults(func=create_entry)

# Create a task
parser_create_task = subparsers.add_parser("task", help="Create or modify a task")
parser_create_task.add_argument("task", help="The task name")
parser_create_task.add_argument("-f", "--focus", action="store_true", help="Focuses the task on creation")
parser_create_task.add_argument("-p", "--parent-id", type=int, help="the id of the parent task that this is a subtask to")
parser_create_task.set_defaults(func=create_task)

# Query related subcommands
parser_query = subparsers.add_parser("query", help="Query entries, generations, or tasks")
parser_query.add_argument("-l", "--limit", type=int, help="Limit the number of results", default=50)
parser_query.add_argument("-o", "--offset", type=int, help="offset where to start searching", default=0)
parser_query.add_argument("--id", type=int, help="search specifically for an object by id")
parser_query.add_argument("-s", "--search", help="Search filter")

parser_query.add_argument("-g", "--generations", action="store_true", help="Query generations")
parser_query.add_argument("-t", "--tasks", action="store_true", help="Query tasks")
parser_query.add_argument("-f", "--focus", type=str, choices=["true", "false"], help="Filter focused tasks", default="true")
parser_query.set_defaults(func=show)

# dev related subcommands
parser_dev = subparsers.add_parser("dev", help="Misc dev utilities")
parser_dev.add_argument("--flush-annotations", action="store_true", help="Flush all annotations")
# TODO: make it so that this can be done with any database in the future
parser_dev.add_argument("--delete-database", action="store_true", help="Flush all annotations")
parser_dev.add_argument("--cycle-next-entry", action="store_true", help="Cycle the engine once")
parser_dev.add_argument("--load", '-l', type=str, help="upload a list of \\n-separated entries to the db")
parser_dev.set_defaults(func=route_dev_command)

parser.set_defaults(func=parser.print_help)
