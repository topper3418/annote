from src.db.controller.actions import wipe_actions
from src.db.map import Session


with Session() as session: 
    wipe_actions(session)
