from sqlalchemy.orm import Session
from typing import List
from ..map import Task, Entry, Action


def create_action(session: Session,
                  action_str: str,
                  entry: Entry,
                  task: Task) -> Action:
    action= Action(
        action=action_str,
        task=task,
        entry=entry
    )
    session.add(action)
    session.commit()
    return action


def wipe_actions(session: Session):
    """straight up deletes all actions. I made this for dev purposes only"""
    session.query(Action).delete()
    session.commit()

