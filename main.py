from __future__ import annotations
from pprint import pprint
import time
from datetime import datetime

from src.db.map import Entry, Task, Action, Session
from src.db.controller import create_task
from src.ollama.generate import generate_tasks


test_prompt = """Today I need to work out, finish my coding 
project, do my class for an hour, and play videogames. 
To finish my coding project, I need to get it to add 
time estimates, get it to let you make changes to those 
time estimates, create a backend to let it run without 
clogging up the ui, and finally I need to make a webUI. 
videogames will be AoE"""


def main():
    start = time.perf_counter()
    with Session() as session:
        seed = Entry(text=test_prompt)
        parent = create_task({"text": "Plan for the day",
                              "start": datetime.now(),
                              "children": []},
                             parent=None,
                             source=seed)

        session.add(seed)
        session.add(parent)
        session.commit()
        session.refresh(seed)
        session.refresh(parent)
    tasks = generate_tasks(seed.text)
    with Session() as session:
        parent = session.query(Task).filter_by(id=parent.id).one()
        for task_dict in tasks:
            task = create_task(task_dict, parent=parent, source=seed)
            session.add(task)
        session.commit()
        session.refresh(parent)
        print('children')
        pprint([child.text for child in parent.children])
        parent.pprint()
    
    end = time.perf_counter()
    elapsed = end - start
    print(f"Time taken: {elapsed:.6f} seconds")


if __name__ == "__main__":
    main()

