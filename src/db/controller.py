from datetime import datetime
from typing import List

from sqlalchemy import desc

from .map import Entry, Task, Action, Session


# for the most part, this is what the llm will be given access to. 


def create_entry(prompt: str, context: Task | None = None) -> Entry:
    """from the user's input, creates and returns an entry"""
    entry = Entry(text=prompt)
    return entry


def create_task(task_dict: dict, 
                parent: Task | None = None, 
                source: Entry | None = None) -> Task:
    """For a dictionary representing a task, generate the database objects"""
    creation = Action(action="create", entry=source)
    task = Task(
        text=task_dict['text'],
        start=task_dict.get('start'),
        end=task_dict.get('end'),
        parent=parent,
        actions=[creation]
    )
    for child_task_dict in task_dict.get('children', []):
        child_task = create_task(child_task_dict, task, source)
        task.children.append(child_task)
    return task


def get_top_level_tasks_json(recurse: int = 0, limit: int = 50) -> List[dict]:
    with Session() as session:
        epics = session.query(Task).filter(Task.parent_id.is_(None)).limit(limit).all()
        return [epic.json(recurse) for epic in epics]


def get_recent_entries_json(recurse: int = 0, limit: int = 50) -> List[dict]:
    with Session() as session:
        entries = session.query(Entry).order_by(Entry.create_time).limit(limit).all()
        return [entry.json(recurse) for entry in entries]


def is_latest_entry(test_entry_id: int) -> bool:
    with Session() as session:
        latest_entry = session.query(Entry).order_by(desc(Entry.create_time)).one()
        return test_entry_id == latest_entry.id


# "actions":

# change start date


# change end date


# begin task


# complete task


# cancel task


# switch focus


# add action (manually add an action to an entry and task) 
