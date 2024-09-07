from ..db import Controller


def create_entry(note):
    print(f"Creating note: {note}")
    with Controller() as db: 
        new_entry = db.create_entry(note)
        return new_entry.json()

