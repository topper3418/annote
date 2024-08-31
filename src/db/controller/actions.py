from sqlalchemy.orm import Session
from typing import List
from ..map import Task, Entry, Action


def create_action(session: Session,
                  action: str,
                  entry: Entry,
                  task: Task) -> Action:
    action = Action(
            action=action,
            task=task,
            entry=entry
    )
    session.add(action)
    session.commit()
    return action
