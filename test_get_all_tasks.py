from pprint import pprint
from src.db import Controller

if __name__ == "__main__":
    with Controller() as conn:
        tasks = conn.get_focused_task()
        pprint([task.json(recurse=2) for task in tasks])
