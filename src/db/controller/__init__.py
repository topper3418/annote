

from src.db.map import Session
from .entries import create_entry


class Controller:

    def __init__(self):
        self.Session = Session
        self.data = []

    def data_to_dict(self, recurse=0):
        """take the currently buffered data and converts it to a dict"""
        return [item.json(recurse) for item in self.data]

    def create_entry(self, prompt):
        entry = create_entry(prompt)
        self.data.append(entry) 
