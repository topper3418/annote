import argparse
from src.db import create_note
import os
import subprocess
import sys

def run_script_in_background():
    if sys.platform == "win32":
        # For Windows
        subprocess.Popen(["start", "/B", "python", "other_script.py"], shell=True)
    else:
        # For Unix-like systems
        subprocess.Popen(["nohup", "python3", "other_script.py", "&"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, preexec_fn=os.setpgrp)

if __name__ == "__main__":
    run_script_in_background()
    print("Script started in the background.")


def main():
    # Create an argument parser
    parser = argparse.ArgumentParser(description='Type in a note to have it annotated by Ollama')

    # Add an argument for the string input
    parser.add_argument('input_string', type=str, help='The input string')

    # Parse the command line arguments
    args = parser.parse_args()

    # Access the input string
    input_string = args.input_string

    create_note(input_string)

if __name__ == '__main__':
    main()