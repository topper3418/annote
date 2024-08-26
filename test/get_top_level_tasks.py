from pprint import pprint
from src.db.controller import get_top_level_tasks_json


tlt = get_top_level_tasks_json()

pprint(tlt)

