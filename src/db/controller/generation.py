import json
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc
from ..map import Generation, Entry


def create_generation(session: Session, entry: Entry, process: str, data: dict | list) -> Generation:
    generation = Generation(
            process=process,
            data=json.dumps(data),
            entry=entry
    )
    session.add(generation)
    session.commit()
    return generation


def get_generations(session: Session, limit: int = 50) -> List[Generation]:
    generations = session.query(Generation).order_by(desc(Generation.id)).limit(limit).all()
    return generations


def get_latest_generation(session: Session) -> Generation | None:
    """gets the highest entry id that has been processed. not to be confused with the most recently processed entry id"""
    generation = session.query(Generation).order_by(desc(Generation.entry_id)).first()
    return generation


def get_latest_generated_entry_id(session: Session, process_name: Optional[str] = None) -> int | None:
    """gets the highest entry id that has been processed. not to be confused with the most recently processed entry id"""
    query = session.query(Generation)
    if process_name is not None:
        query = query.where(Generation.process == process_name)
    highest_generation = query.order_by(desc(Generation.entry_id)).first()
    return highest_generation.entry_id if highest_generation is not None else None


def wipe_generations(session: Session):
    """straight up deletes all generations. I made this for dev purposes only"""
    session.query(Generation).delete()
    session.commit()

