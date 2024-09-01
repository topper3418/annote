import json
from pprint import pprint

import ollama
# this script will have the top level functions related to ollama


entry_annotation_prompt = """\
Given this context: 
{task}

Please consider this prompt:
{newEntry}

I would like for you to consider the task and nested subtasks shown and think of 
any sub-tasks this adds, as well any actions this might perform upon them out of 
["begin", "pause", "complete", "cancel", "note"]. "create" is not an action 
you are allowed to generate, as any tasks you create will implicitly be created
by that entry. note will most likely be the most common, as it is essentially 
just a thought

Do not speculate on what other actions might be required based on the context 
and prompt, only deal with what the prompt directly implies. 

Your response must be in the following shape: 
**keys with a ?: separator are optional
{{
    tasks?: [{{
        text: "a concise string representing the task",
        parentId?: a number matching the id of the parent task it relates to
        start?: "string in the format of YYYY-MM-DD HH:MM estimating the start time of the task",
        end?: "string in the format of YYYY-MM-DD HH:MM estimating the end time of the task",
        children?: [a list of subtasks, if applicable. same shape as this task object, but parentId will be implied so do not include it]
        focus: "true or false, does this seem like something the user intends to put effort or thought into in the immediate future?"
    }}],
    actions?: [{{
        action: "one of the five given options",
        taskId: a number matching the id of the parent task it relates to. This cannot be any of the tasks returned above, as those will automatically have a "create" action assigned to them. 
    }}]
}}

"""

# for example, when the engine cycles it will be shown the context and the  
def process_entry(entry: dict, context: dict | list | None) -> dict:
    prompt = entry_annotation_prompt.format(
        task=json.dumps(context or "no context provided"),
        newEntry=json.dumps(entry)
    )
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


