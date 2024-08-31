from src.db.controller.generation import wipe_generations
from src.db.controller.actions import wipe_actions
from src.db.controller.tasks import wipe_tasks
from src.db.map import Session


with Session() as session: 
    wipe_generations(session)
    wipe_actions(session)
    wipe_tasks(session)
