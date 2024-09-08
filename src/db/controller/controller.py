from typing import List, Optional

from src.db.controller.actions import create_action, wipe_actions

from .tasks import create_task, focus_task, get_focused_task, get_latest_task, get_task, get_top_level_tasks, search_task, wipe_tasks
from .generation import create_generation, get_generations, get_latest_generated_entry_id, get_latest_generation, wipe_generations
from ..map import Entry, Generation, Session, Task, Action, Base, engine
from .entries import create_entry, get_entry, get_latest_entry, get_recent_entries, is_latest_entry
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

    def create_entry(self, prompt: str, context: Optional[Task] = None) -> Entry:
        self._ensure_session()
        entry = create_entry(self.session, prompt, context)
        return entry

    def get_entry(self, entry_id) -> Entry | None: 
        self._ensure_session()
        entry = get_entry(self.session, entry_id)
        return entry

    def get_latest(self) -> dict:
        self._ensure_session()
        entry = get_latest_entry(self.session)
        generation = get_latest_generation(self.session)
        task = get_latest_task(self.session)
        return {
                'entry': entry.id if entry is not None else None,
                'generation': generation.id if generation is not None else None,
                'task': task.id if task is not None else None
        }

    def get_recent_entries(self, 
                           limit: int = 50, 
                           search: Optional[str] = None,
                           task: Optional[Task] = None,
                           task_id: Optional[int] = None) -> List[Entry]:
        self._ensure_session()
        entries = get_recent_entries(self.session, limit, search, task, task_id)
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

    def get_latest_generated_entry_id(self, process_name: Optional[str] = None) -> int | None:
        self._ensure_session()
        return get_latest_generated_entry_id(self.session, process_name)

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

    def get_top_level_tasks(self, limit: int=50, show_completed: bool=False, offset: int=0) -> List[Task]:
        self._ensure_session()
        tasks = get_top_level_tasks(self.session, limit, show_completed)
        return tasks

    def search_task(self, search_str: str) -> Task | None:
        self._ensure_session()
        task = search_task(self.session, search_str)
        return task

    def focus_task(self, task_id: int, focus: bool = True):
        self._ensure_session()
        task = focus_task(self.session, task_id, focus)
        return task

    def get_focused_task(self, offset: int = 0) -> Task | None:
        self._ensure_session()
        return get_focused_task(self.session, offset)

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

    @classmethod
    def wipe_database(cls):
        Base.metadata.drop_all(engine)
