from typing import Tuple
from ..db import Controller, Task, Entry

def get_extraction_context(conn: Controller, process_name: str) -> Tuple[Task | None, Entry | None]:
    task = conn.get_focused_task()
    target_entry_id = conn.get_latest_generated_entry_id(process_name=process_name) or 0 + 1
    entry = conn.get_entry(target_entry_id)
    return task, entry


