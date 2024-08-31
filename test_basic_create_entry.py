from src.db import Controller

if __name__ == "__main__":
    with Controller() as conn:
        entry = conn.create_entry("Do stuff today")
        print(entry.json())

