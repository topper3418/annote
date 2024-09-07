from .db import Controller as Controller
import os


def create_entry(note):
    print(f"Creating note: {note}")
    with Controller() as conn: 
        new_entry = conn.create_entry(note)
        return new_entry.json()

def load_entries(filename):
    filepath = os.path.join('data', filename)
    print(f"loading entries from {filepath}")
    with open(filepath, 'r') as file:
        entries = file.readlines()
    with Controller() as conn:
        new_entries = [conn.create_entry(entry.strip('\n')) for entry in entries]
        entries_json = [entry.json() for entry in new_entries]
    pprint(entries_json)

