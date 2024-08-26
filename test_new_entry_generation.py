import json
from pprint import pprint

import ollama
from sqlalchemy import desc, asc

from src.db.map import Action, Entry, Task, Session
# this script will have the top level functions related to ollama


entry_annotation_prompt = """\
Given this context: 
{task}

Please consider this prompt:
{newEntry}

I would like for you to consider the task and nested subtasks shown and think of 
any sub-tasks this adds, as well any actions this might perform upon them out of 
["begin", "pause", "complete", "cancel", "annotate"]. annotate will most likely 
be the most common. 

Your response must be in the following shape: 
**keys with a ?: separator are optional
{
    tasks?: [{
        text: "a concise string representing the task",
        taskId: a number matching the id of the parent task it relates to
        start?: "string in the format of YYYY-MM-DD HH:MM estimating the start time of the task",
        end?: "string in the format of YYYY-MM-DD HH:MM estimating the end time of the task",
        children?: [a list of subtasks, if applicable]
    }],
    actions?: [{
        action: "one of the five given options",
        taskId: a number matching the id of the parent task it relates to
    ]]
}

"""

# for example, when the engine cycles it will be shown the context and the  
def process_entry(entry: Entry, context: Task) -> dict:
    prompt = entry_annotation_prompt.format(task=json.dumps(context.json(recurse=3)),
                                            newEntry=entry.text)
    print("PROMPTING")
    print(prompt)
    response = ollama.generate(
        prompt=prompt,
        format='json',
        model='llama3.1',
        options={ 'temperature': 0 },
        stream=False
    )

    parsed_response = json.loads(response['response'])
    print("\nRESPONSE")
    pprint(parsed_response)
    return parsed_response


if __name__ == "__main__":
    with Session() as session:
        latest_entry = session.query(Entry).order_by(desc(Entry.create_time)).first()
        first_task = session.query(Task).order_by(asc(Task.id)).first()
        process_entry(latest_entry, first_task)
