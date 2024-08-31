from pprint import pprint
from src.db import Controller

if __name__ == "__main__":
    with Controller() as conn:
        generations = conn.get_generations()
        pprint([generation.json(recurse=1) for generation in generations])
        
