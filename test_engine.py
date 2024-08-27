
from sqlalchemy import desc, asc

from src.db.map import Action, Entry, Task, Session




with Session() as session:
    latest_entry = Entry(text="I've worked out")
    session.add(latest_entry)
    first_task = session.query(Task).order_by(asc(Task.id)).first()
    latest_entry_context = latest_entry.json(recurse=3) if latest_entry else None
    first_task_context = first_task.json() if first_task else None

    process_entry(latest_entry_context, first_task_context)


-
