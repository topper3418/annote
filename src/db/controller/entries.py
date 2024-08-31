from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import desc
from ..map import Entry


def create_entry(session: Session, prompt: str) -> Entry:
    """from the user's input, creates and returns an entry"""
    entry = Entry(text=prompt)
    session.add(entry)
    session.commit()
    return entry


def get_recent_entries(session: Session,
                       limit: int = 50, 
                       search: Optional[str] = None) -> List[Entry]:
    query = session.query(Entry)
    if search is not None:
        query = query.filter(Entry.text.ilike(search))
    query = query.order_by(desc(Entry.create_time)).limit(limit)
    entries = query.all()
    return entries


def get_latest_entry(session: Session) -> Entry:
    query = session.query(Entry).order_by(desc(Entry.id))
    entry = query.one()
    return entry


def is_latest_entry(session: Session, entry_id: int) -> bool:
    latest_entry = session.query(Entry).order_by(desc(Entry.id)).first()
    return entry_id == latest_entry.id


def get_entry(session: Session, entry_id: int) -> Entry:
    entry = session.query(Entry).where(Entry.id == entry_id).one()
    return entry
