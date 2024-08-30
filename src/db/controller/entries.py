from sqlalchemy.orm import Session
from ..map import Entry


def create_entry(session: Session, prompt: str) -> Entry:
    """from the user's input, creates and returns an entry"""
    entry = Entry(text=prompt)
    session.add(entry)
    session.commit()
    return entry


