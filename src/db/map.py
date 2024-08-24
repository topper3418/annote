from pprint import pprint

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, sessionmaker
from datetime import datetime



engine = create_engine("sqlite:///annotes.db")  # Replace with your database URL

Session = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)


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
    task_id: Mapped[int] = mapped_column(ForeignKey('tasks.id'), nullable=True)

    task = relationship("Task", back_populates="entries", foreign_keys=[task_id])
    actions = relationship("Action", back_populates="entry")

    def __repr__(self):
        return f"<Entry(text='{self.text}', create_time='{self.create_time}')>"


class Task(Base):
    __tablename__ = 'tasks'
    # declare it explicitly here to allow for the recursive relationship
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    text: Mapped[str] = mapped_column(String)
    start: Mapped[datetime | None] = mapped_column(DateTime)
    end: Mapped[datetime | None] = mapped_column(DateTime)
    focus: Mapped[bool] = mapped_column(Boolean, default=False)

    parent_id: Mapped[int] = mapped_column(ForeignKey('tasks.id'), nullable=True)

    entries = relationship("Entry", back_populates="task", foreign_keys=[Entry.task_id])
    actions = relationship("Action", back_populates="task")
    parent = relationship("Task", remote_side=[id], back_populates="children")
    children = relationship("Task", back_populates="parent")

    def __repr__(self):
        return f"<Task(text='{self.text}', start='{self.start}', end='{self.end}')>"
    
    def pprint(self):
        pprint({
            "text": self.text,
            "start": self.start,
            "end": self.end,
            "entries": [entry.text for entry in self.entries],
            "actions": [action.action for action in self.actions],
            "children": [child.pprint() for child in self.children],
        })


class Action(Base):
    __tablename__ = 'actions'

    action: Mapped[str] = mapped_column(String(32))
    task_id: Mapped[int] = mapped_column(ForeignKey('tasks.id'), nullable=False)
    entry_id: Mapped[int] = mapped_column(ForeignKey('entries.id'), nullable=False)

    task = relationship("Task", back_populates="actions")
    entry = relationship("Entry", back_populates="actions")


Base.metadata.create_all(engine)

