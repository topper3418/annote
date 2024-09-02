from typing import List, Optional

from sqlalchemy.util import generic_repr

from src.db.controller.actions import create_action, wipe_actions

from .tasks import create_task, focus_task, get_focused_tasks, get_task, wipe_tasks
from .generation import create_generation, get_generations, get_latest_generated_entry_id, wipe_generations
from ..map import Entry, Generation, Session, Task, Action
from .entries import create_entry, get_entry, get_recent_entries, is_latest_entry
from src.db.controller import generation


class Controller:
    """To be used in routes, will store up a buffer of objects and return them as json objects. """

    def __init__(self):
        self.session_factory = Session
        self.session: Session = None

    def _ensure_session(self):
        if self.session is None:
            raise Exception('session not open on __exit__ call')

    def __enter__(self):
        self.session = self.session_factory()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._ensure_session()
        try:
            if exc_type:
                self.session.rollback()
            else:
                self.session.commit()
        finally:
            self.session.close()

    def create_entry(self, prompt) -> Entry:
        self._ensure_session()
        entry = create_entry(self.session, prompt)
        return entry

    def get_entry(self, entry_id) -> Entry | None: 
        self._ensure_session()
        entry = get_entry(self.session, entry_id)
        return entry

    def get_recent_entries(self, 
                           limit: int = 50, 
                           search: Optional[str] = None) -> List[Entry]:
        self._ensure_session()
        entries = get_recent_entries(self.session, limit, search)
        return entries

    def is_latest_entry(self, entry_id: int):
        self._ensure_session()
        return is_latest_entry(self.session, entry_id)

    def create_generation(self, entry: Entry, process: str, data: dict | list) -> Generation:
        self._ensure_session()
        generation = create_generation(self.session, entry, process, data)
        return generation

    def get_generations(self, limit: int = 50) -> List[Generation]:
        self._ensure_session()
        generations = get_generations(self.session, limit)
        return generations

    def get_latest_generated_entry_id(self) -> int | None:
        self._ensure_session()
        return get_latest_generated_entry_id(self.session)

    def create_task(self,
                    task_dict: dict, 
                    parent: Task | None = None, 
                    source: Entry | None = None):
        self._ensure_session()
        task = create_task(self.session, task_dict, parent, source)
        return task

    def get_task(self, task_id: int) -> Task | None:
        self._ensure_session()
        task = get_task(self.session, task_id)
        return task

    def focus_task(self, task_id: int, focus: bool = True):
        self._ensure_session()
        task = focus_task(self.session, task_id, focus)
        return task

    def get_focused_tasks(self):
        self._ensure_session()
        return get_focused_tasks(self.session)

    def create_action(self, 
                  action: str,
                  entry: Entry,
                  task: Task) -> Action:
        self._ensure_session()
        action_obj = create_action(self.session, action, entry, task)
        return action_obj

    def reset_annotations(self):
        self._ensure_session()
        wipe_generations(self.session)
        wipe_actions(self.session)
        wipe_tasks(self.session)
