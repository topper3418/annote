from datetime import datetime

from .map import Entry, Task, Action, Session


# for the most part, this is what the llm will be given access to. 


def create_entry(prompt: str, parent: Task | None = None) -> Entry:
    """from the user's input, creates and returns an entry"""
    entry = Entry(text=prompt, task=parent)
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


# "actions":

# change start date


# change end date


# begin task


# complete task


# cancel task


# switch focus


# add action (manually add an action to an entry and task) 
