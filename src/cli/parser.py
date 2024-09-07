import argparse
from .funcs import print_info, create_entry, show, route_dev_command

parser = argparse.ArgumentParser(description="Annote CLI App")
subparsers = parser.add_subparsers(dest="subcommand", help="Subcommand to run")

# Print program info
parser_info = subparsers.add_parser("annote", help="Print program info")
parser_info.set_defaults(func=print_info)

# Create a note
parser_create = subparsers.add_parser("note", help="Create a note")
parser_create.add_argument("note", help="The note content")
parser_create.set_defaults(func=create_entry)

# Query related subcommands
parser_query = subparsers.add_parser("query", help="Query entries, generations, or tasks")
parser_query.add_argument("-l", "--limit", type=int, help="Limit the number of results", default=50)
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
