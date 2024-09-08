from datetime import datetime
from sqlalchemy import desc
from sqlalchemy.orm import Session
from typing import List

from sqlalchemy.sql.operators import ilike_op

from ...util import parse_date
from ..map import Task, Entry, Action


def extract_date(task_dict: dict, key: str) -> datetime | None:
    return parse_date(task_dict.get(key, ''))


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
        start=extract_date(task_dict, 'start'),
        end=extract_date(task_dict, 'end'),        
        parent=parent,
        actions=actions
    )
    for child_task_dict in task_dict.get('children', []):
        child_task = create_task(session, child_task_dict, task, source)
        task.children.append(child_task)
    session.add(task)
    session.commit()
    return task


def get_task(session: Session, task_id: int) -> Task | None:
    task = session.query(Task).where(Task.id == task_id).first()
    return task


def get_latest_task(session: Session) -> Task | None:
    task = session.query(Task).order_by(desc(Task.id)).first()
    return task


def search_task(session: Session, search_str: str) -> Task | None:
    """searches first for focused tasks, then if no match searches all tasks. Either way returns first match or None. """
    task = session.query(Task).filter(Task.text.ilike(f'%{search_str}%')).first()
    return task


def get_top_level_tasks(session: Session, 
                        limit: int = 50,
                        show_completed: bool = False,
                        offset: int = 0) -> List[Task]:
    # epics = session.query(Task).where(Task.status != 'complete').filter(Task.parent_id.is_(None)).limit(limit).all()
    query = session.query(Task)
    if not show_completed: 
        query = query.where(Task.status != 'complete')
    query = query.filter(Task.parent_id.is_(None)).limit(limit).offset(offset)
    epics = query.all()
    return epics


def focus_task(session: Session,
               task_id: int,
               focus: bool = True):
    task = session.query(Task).where(Task.id == task_id).first()
    if not task:
        raise ValueError(f'no task found matching {task_id}')
    session.commit()
    return task


def get_focused_task(session: Session, offset: int = 0) -> Task | None:
    task_match = session.query(Task).all()
    if not len(task_match) > offset:
        return
    task = task_match[offset]
    return task

# TODO: GET ALL TASKS


def wipe_tasks(session: Session):
    """straight up deletes all tasks. I made this for dev purposes only"""
    session.query(Task).delete()
    session.commit()


