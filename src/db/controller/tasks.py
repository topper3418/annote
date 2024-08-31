from sqlalchemy.orm import Session
from typing import List
from ..map import Task, Entry, Action


def create_task(session: Session,
                task_dict: dict, 
                parent: Task | None = None, 
                source: Entry | None = None) -> Task:
    """For a dictionary representing a task, generate the database objects"""
    actions = []
    if source is not None:
        actions.append(Action(action="create", entry=source))
    task = Task(
        text=task_dict['text'],
        start=task_dict.get('start'),
        end=task_dict.get('end'),
        parent=parent,
        actions=actions
    )
    for child_task_dict in task_dict.get('children', []):
        child_task = create_task(session, child_task_dict, task, source)
        task.children.append(child_task)
    session.add(task)
    session.commit()
    return task


def get_top_level_tasks(session: Session, 
                             recurse: int = 0, 
                             limit: int = 50) -> List[Task]:
    epics = session.query(Task).filter(Task.parent_id.is_(None)).limit(limit).all()
    return epics


def focus_task(session: Session,
               task_id: int,
               focus: bool = True):
    task = session.query(Task).where(Task.id == task_id).one()
    task.focus = focus
    session.commit()
    return task


def get_focused_tasks(session: Session):
    tasks = session.query(Task).where(Task.focus == True).all()
    return tasks
