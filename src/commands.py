from .db import Note, Tag, Task, Keyword, Session, Base, engine
import ollama


def evaluate_if_task(note: Note, autocommit: bool = False) -> Note:
    """evaluates if a note is a task, and creates the object if it is"""
    response = ollama.generate(
        model='mistral', 
        prompt=f"""
Please consider the following note: 

{note.content}

please respond with: 
 - an empty json object if this does not appear to be a task
 OR
 - a json object with the following structure as it appears to be a task, 
 leave off of the object if not mentioned:
    "title": "a short title"
    "start_date": "YYYY-MM-DD",
    "due_date": "YYYY-MM-DD",
    "status": "active" | "inactive" | "complete",
    "active": true | false
""",
        format='json'
    )
    print("relevant note:")
    print(response)