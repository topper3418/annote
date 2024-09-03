from pprint import pprint
from typing import List

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, sessionmaker, object_session
from datetime import datetime



engine = create_engine("sqlite:///data/annotes.db")  # Replace with your database URL

Session = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    def is_connected_to_session(self) -> bool:
        session = object_session(self)
        return session is not None and session.is_active



###################################################################################
#                                  notetaking objects                             #
###################################################################################
# Entries will be what the user creates. 
# All entries will be taken within the scope of a task, which will be the .task
# attribute. 
# The LLM will determine if these entries represent any actions. 
# First they will be considered as a potential action to 
# any other tasks in the scope of the task, and then if it should be used to create
# a new task (should be the first action of any task)


class Entry(Base):
    __tablename__ = 'entries'

    text: Mapped[str] = mapped_column(String)
    create_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    # task_id: Mapped[int] = mapped_column(ForeignKey('tasks.id'), nullable=True)

    # task = relationship("Task", back_populates="entries", foreign_keys=[task_id])
    actions = relationship("Action", back_populates="entry")
    generations = relationship("Generation", back_populates="entry")

    def __repr__(self):
        return f"<Entry(text='{self.text}', create_time='{self.create_time}')>"

    def json(self, recurse=0):
        if recurse > 5:
            raise ValueError(f'max recurse is 4, {recurse} is too high')
        json_value = {
            "id": self.id,
            "text": self.text,
            "create_time": self.create_time.strftime("%D %H:%M"),
        }
        if recurse == 1:
            json_value["actions"] = [action.action for action in self.actions]
            json_value["generations"] = [generation.process for generation in self.generations]
        elif recurse > 1:
            json_value["actions"] = [action.json(recurse-1) for action in self.actions]
            json_value["generations"] = [generation.json(recurse-1) for generation in self.generations]
        return json_value
            


class Task(Base):
    __tablename__ = 'tasks'
    # declare it explicitly here to allow for the recursive relationship
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    text: Mapped[str] = mapped_column(String)
    start: Mapped[datetime | None] = mapped_column(DateTime)
    end: Mapped[datetime | None] = mapped_column(DateTime)
    status: Mapped[str] = mapped_column(String, default="new")
    focus: Mapped[bool] = mapped_column(Boolean, default=False)
    confidence: Mapped[int] = mapped_column(Integer, default=10)
    confirmed: Mapped[bool] = mapped_column(Boolean, default=False)

    parent_id: Mapped[int] = mapped_column(ForeignKey('tasks.id'), nullable=True)
    generation_id: Mapped[int] = mapped_column(ForeignKey('generations.id'), nullable=True)

    # entries = relationship("Entry", back_populates="task", foreign_keys=[Entry.task_id])
    generation = relationship("Generation", back_populates="tasks")
    actions = relationship("Action", back_populates="task")
    parent = relationship("Task", remote_side=[id], back_populates="children")
    children = relationship("Task", back_populates="parent")

    def __repr__(self):
        return f"<Task(text='{self.text}', start='{self.start}', end='{self.end}')>"
    
    def json(self, recurse: int=0, suppress: List = []):
        if recurse > 5:
            raise ValueError(f'max recurse is 4, {recurse} is too high')
        json_value = {
            "id": self.id,
            "text": self.text,
            "start": self.start.strftime("%D %H:%M") if self.start else None,
            "end": self.end.strftime("%D %H:%M") if self.end else None,
            "focus": self.focus,
        }
        if recurse == 1:
            if 'actions' not in suppress:
                json_value["actions"] = [action.action for action in self.actions]
            if 'children' not in suppress:
                json_value["children"] = [child.text for child in self.children]
            if 'parent' not in suppress: 
                json_value["parent"] = self.parent.text if self.parent else None
        elif recurse > 1:
            if 'actions' not in suppress:
                json_value["actions"] = [action.json(recurse-1) for action in self.actions]
            if 'children' not in suppress:
                json_value["children"] = [child.json(recurse-1) for child in self.children]
            if 'parent' not in suppress: 
                json_value["parent"] = self.parent.json(recurse-1) if self.parent else None
        return json_value


class Action(Base):
    __tablename__ = 'actions'

    action: Mapped[str] = mapped_column(String(32))
    confidence: Mapped[int] = mapped_column(Integer, default=10)
    confirmed: Mapped[bool] = mapped_column(Boolean, default=False)

    task_id: Mapped[int] = mapped_column(ForeignKey('tasks.id'), nullable=False)
    entry_id: Mapped[int] = mapped_column(ForeignKey('entries.id'), nullable=False)

    task = relationship("Task", back_populates="actions")
    entry = relationship("Entry", back_populates="actions")

    def json(self, recurse=0):
        if recurse > 5:
            raise ValueError(f'max recurse is 4, {recurse} is too high')
        json_value = {
            "id": self.id,
            "action": self.action
        }
        if recurse == 1:
            json_value["task"] = self.task.text
            json_value["entry"] = self.entry.text
        elif recurse > 1:
            json_value["task"] = self.task.json(recurse-1) 
            json_value["entry"] = self.entry.json(recurse-1)
        return json_value


class Generation(Base):
    __tablename__ = 'generations'

    process: Mapped[str] = mapped_column(String)
    data: Mapped[str] = mapped_column(Text)
    user_comment: Mapped[str | None] = mapped_column(String)
    entry_id: Mapped[int] = mapped_column(ForeignKey('entries.id'), nullable=False)

    entry = relationship("Entry", back_populates="generations")

    def json(self, recurse=0):
        if recurse > 5:
            raise ValueError(f'max recurse is 4, {recurse} is too high')
        json_value = {
            'id': self.id,
            'process': self.process
        }
        if recurse == 1:
            json_value['entry'] = self.entry.text
        elif recurse > 1:
            json_value['entry'] = self.entry.json(recurse-1)
        return json_value


Base.metadata.create_all(engine)

