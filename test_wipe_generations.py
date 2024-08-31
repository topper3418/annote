from src.db.controller.generation import wipe_generations
from src.db.map import Session


with Session() as session: 
    wipe_generations(session)
