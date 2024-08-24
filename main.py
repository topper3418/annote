from __future__ import annotations
from typing import List
import ollama
from pprint import pprint
import json
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, sessionmaker
from datetime import datetime
import time

# Step 2: Create an engine
engine = create_engine("sqlite:///annotes.db")  # Replace with your database URL

# Step 3: Configure sessionmaker
Session = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)


class Entry(Base):
    __tablename__ = 'entries'

    text: Mapped[str] = mapped_column(String)
    create_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    user_entry: Mapped[bool] = mapped_column(Boolean, default=True)
    plan_id: Mapped[int] = mapped_column(ForeignKey('plans.id'), nullable=True)
    task_id: Mapped[int] = mapped_column(ForeignKey('tasks.id'), nullable=True)

    plan = relationship("Plan", back_populates="entries", foreign_keys=[plan_id])
    task = relationship("Task", back_populates="entries", foreign_keys=[task_id])
    actions = relationship("Action", back_populates="entry")

    def __repr__(self):
        return f"<Entry(text='{self.text}', create_time='{self.create_time}', user_entry='{self.user_entry}')>"


class Plan(Base):
    __tablename__ = 'plans'

    seed_id: Mapped[int] = mapped_column(ForeignKey('entries.id'), nullable=False)

    seed = relationship("Entry", foreign_keys=[seed_id])
    entries = relationship("Entry", back_populates="plan", foreign_keys=[Entry.plan_id])
    tasks = relationship("Task", back_populates="plan")

    def __repr__(self):
        return f"<Plan(seed='{self.seed}')>"
    
    def pprint(self):
        pprint({
            "seed": self.seed.text,
            "tasks": [task.pprint() for task in self.tasks],
            "entries": [entry.text for entry in self.entries]
        })


class Task(Base):
    __tablename__ = 'tasks'
    # declare it explicitly here to allow for the recursive relationship
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    text: Mapped[str] = mapped_column(String)
    start: Mapped[datetime | None] = mapped_column(DateTime)
    end: Mapped[datetime | None] = mapped_column(DateTime)
    planned: Mapped[bool] = mapped_column(Boolean, default=False)

    source_id: Mapped[int] = mapped_column(ForeignKey('entries.id'), nullable=False)
    plan_id: Mapped[int] = mapped_column(ForeignKey('plans.id'), nullable=False)
    parent_id: Mapped[int] = mapped_column(ForeignKey('tasks.id'), nullable=True)

    entries = relationship("Entry", back_populates="task", foreign_keys=[Entry.task_id])
    source = relationship("Entry", foreign_keys=[source_id])
    plan = relationship("Plan", back_populates="tasks", foreign_keys=[plan_id])
    actions = relationship("Action", back_populates="task")
    parent = relationship("Task", remote_side=[id], back_populates="children")
    children = relationship("Task", back_populates="parent")

    def __repr__(self):
        return f"<Task(text='{self.text}', start='{self.start}', end='{self.end}', planned='{self.planned}')>"
    
    def pprint(self):
        pprint({
            "text": self.text,
            "start": self.start,
            "end": self.end,
            "planned": self.planned,
            "entries": [entry.text for entry in self.entries],
            "actions": [action.action for action in self.actions],
            "children": [child.pprint() for child in self.children]
        })


class Action(Base):
    __tablename__ = 'actions'

    action: Mapped[str] = mapped_column(String(32))
    task_id: Mapped[int] = mapped_column(ForeignKey('tasks.id'), nullable=False)
    entry_id: Mapped[int] = mapped_column(ForeignKey('entries.id'), nullable=False)

    task = relationship("Task", back_populates="actions")
    entry = relationship("Entry", back_populates="actions")


Base.metadata.create_all(engine)


plan_generation_intro = """\
Respond to the following prompt using a json structure only. The prompt will be a plan that may be 
in the first person, e.g. I should do this, or we need to do that. Please extract a list of tasks
from the prompt and return them in the following shape: 
{
    tasks: [{
        task: "a concise string representing the task",
        start: "string in the format of YYYY-MM-DD HH:MM estimating the start time of the task",
        end: "string in the format of YYYY-MM-DD HH:MM estimating the end time of the task",
        children: [a list of tasks, if they are subtasks to that parent]
    }]
}

Here is the prompt:

"""

def generate_tasks(prompt: str) -> List[dict]:
    response = ollama.generate(
        prompt=plan_generation_intro + prompt,
        format='json',
        model='phi3',
        options={ 'temperature': 0 },
        stream=False
    )
    parsed_response = json.loads(response['response'])
    tasks = parsed_response.get('tasks')
    return tasks


def create_task(task_dict: dict, source: Entry) -> Task:
    task = Task(
        text=task_dict['task'],
        start=datetime.strptime(task_dict.get('start', ''), "%Y-%m-%d %H:%M") if task_dict.get('start') else None,
        end=datetime.strptime(task_dict.get('end', ''), "%Y-%m-%d %H:%M") if task_dict.get('end') else None
    )
    for child_task_dict in task_dict.get('children', []):
        child_task = create_task(child_task_dict)
        task.source = source
        task.children.append(child_task)
    return task


test_prompt = """Today I need to work out, finish my coding 
project, do my class for an hour, and play videogames. 
To finish my coding project, I need to get it to add 
time estimates, get it to let you make changes to those 
time estimates, create a backend to let it run without 
clogging up the ui, and finally I need to make a webUI. 
videogames will be AoE"""

def main():
    start = time.perf_counter()
    with Session() as session:
        seed = Entry(text=test_prompt)
        plan = Plan(seed=seed)
        session.add(seed)
        session.add(plan)
        session.commit()
        session.refresh(seed)
    tasks = generate_tasks(seed.text)
    with Session() as session:
        for task_dict in tasks:
            task = create_task(task_dict, source=seed)
            task.source = seed
            task.plan = plan
            session.add(task)
        session.commit()
        plan.pprint()
    
    end = time.perf_counter()
    elapsed = end - start
    print(f"Time taken: {elapsed:.6f} seconds")


if __name__ == "__main__":
    main()

