from sqlalchemy.orm import Session
from sqlalchemy import desc
from ..map import Generation


def get_latest_generated_entry_id(session: Session) -> int | None:
    """gets the highest entry id that has been processed. not to be confused with the most recently processed entry id"""
    highest_generation = session.query(Generation).order_by(desc(Generation.entry_id)).first()
    return highest_generation.entry_id if highest_generation is not None else None


