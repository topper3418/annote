from __future__ import annotations
import ollama
from pprint import pprint
import json
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from datetime import datetime


class Base(DeclarativeBase):
        id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)


class Entry(Base):
        __tablename__ = 'entries'

        text: Mapped[str] = mapped_column(String)
        create_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
        user_entry: Mapped[bool] = mapped_column(default=True)
        plan_id: Mapped[int] = mapped_column(ForeignKey('plans.id'), nullable=True)
        task_id: Mapped[int] = mapped_column(ForeignKey('tasks.id'), nullable=True)

        plan: Mapped[Plan] = relationship(back_populates="entries")
        task: Mapped[Task] = relationship(back_populates="entries")
        actions: Mapped[List[Action]] = relationship(back_populates="entry")


class Plan(Base):
        __tablename__ = 'plans'

        entry_id: Mapped[int] = mapped_column(ForeignKey('entries.id'), nullable=False)

        source: Mapped[Entry]
        entries: Mapped[List[Entry]] = relationship("Entry", back_populates="plan")
        tasks: Mapped[Task] = relationship(back_populates="plan")


class Task(Entry):
        __tablename__ = 'tasks'

        actions = relationship("Action", back_populates="task")


class Action(Base):
        __tablename__ = 'actions'

        action: Mapped[str] = mapped_column(String)
        task_id: Mapped[int] = mapped_column(ForeignKey('tasks.id'), nullable=False)
        entry_id: Mapped[int] = mapped_column(ForeignKey('entries.id'), nullable=False)

        task = relationship("Task", back_populates="actions")
        entry = relationship("Entry", back_populates="actions")


plan_generation_intro = """\
Respond to the following prompt using a json structure only. The prompt will be a plan that may be 
in the first person, e.g. I should do this, or we need to do that. Please extract a list of tasks
from the prompt and return them in the following shape: 
{
    tasks: [{
        task: "a concise string representing the task",
        start: "string in the format of HH:MM estimating the start time of the task",
        end: "string in the format of HH:MM estimating the start time of the task",
        children: [a list of tasks, if they are subtasks to that parent]
    }]
}

Here is the prompt:

"""

def generate_plan(text):
    response = ollama.generate(
        prompt=plan_generation_intro + text,
        format='json',
        model='phi3',
        options={ 'temperature': 0 },
        stream=False
    )
    parsed_response = json.loads(response['response'])
    tasks = parsed_response.get('tasks')
    pprint(tasks)


def main():
    generate_plan("""Today I need to work out, finish my coding project, do my class for an hour, and play videogames. To finish my coding project, I need to get it to add time estimates, get it to let you make changes to those time estimates, create a backend to let it run without clogging up the ui, and finally I need to make a webUI. videogames will be AoE""")


if __name__ == "__main__":
    main()
